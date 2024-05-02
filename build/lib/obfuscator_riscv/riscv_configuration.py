import random
from obfuscator_core.configuration import (
    ArchetectureInterface,
    ParserInterface,
    PrinterInterface,
    Target,
)
from obfuscator_core.common import (
    Command,
    Label,
    Directive,
    SourceLine,
    Source,
    SourcePart,
)

from .riscv_common import (
    RiscvCommand,
    RiscvSource,
    RiscvSection,
    RiscvDirective,
    RiscvGlobalDirective,
    RiscvObjectDirective,
    RiscvDataDirective,
    RiscvSectionDirective,
    RiscvData,
    RiscvFunction,
    RiscvJmpCommand,
)


class RiscvArch(ArchetectureInterface):
    arch_name = "RISC-V"
    abs_jump_mnemonic = "j"
    jump_commands = [
        "j",
        "jr",
        "jal",
        "jalr",
        "bne",
        "beq",
        "ble",
        "blt",
        "bge",
        "bltu",
        "bgeu",
    ]
    skip_mnemonics = [".ident"]
    skip_cfi_flag = True

    @staticmethod
    def get_abs_jump_mnemonic():
        return RiscvArch.abs_jump_mnemonic

    @staticmethod
    def is_command(line: str) -> bool:
        clear_line = RiscvParser.remove_comment(line).strip()
        return (
            not clear_line.startswith(".")
            and len(clear_line) > 0
            and clear_line.split()[0][-1] != ":"
        )

    @staticmethod
    def get_command(line: str) -> Command:
        (a, b) = RiscvParser.prepare_string(line)
        if a in RiscvArch.jump_commands:
            return RiscvJmpCommand(a, b)
        return RiscvCommand(a, b)

    @staticmethod
    def is_directive(line: str) -> bool:
        clear_line = RiscvParser.remove_comment(line).strip()
        return clear_line.startswith(".") and not clear_line.endswith(":")

    @staticmethod
    def get_directive(line: str) -> Directive:
        (a, b) = RiscvParser.prepare_string(line)
        if a.strip() in RiscvSectionDirective.section_start:
            return RiscvSectionDirective(a, b)
        if a.strip() in RiscvGlobalDirective.directives:
            return RiscvGlobalDirective(a, b)
        if a.strip() in RiscvObjectDirective.directives:
            return RiscvObjectDirective(a, b)
        if a.strip() in RiscvDataDirective.directives:
            return RiscvDataDirective(a, b)
        return RiscvDirective(a, b)

    @staticmethod
    def is_label(line: str) -> bool:
        return RiscvParser.prepare_string(line)[0].endswith(":")

    @staticmethod
    def get_label(line: str) -> Label:
        return Label(RiscvParser.prepare_string(line)[0][:-1])

    @staticmethod
    def is_section_start(line: str) -> bool:
        if RiscvArch.is_directive(line):
            return RiscvSectionDirective.is_section_directive(line.split()[0])
        return False

    @staticmethod
    def get_section(start_directive: Directive, dirs: list) -> RiscvSection:
        result = RiscvSection.get_section(start_directive)
        for dir in dirs:
            result.add_directive(dir)
        return result

    @staticmethod
    def _is_cfi_directive(obj: SourceLine) -> bool:
        return obj.get_mnemonic().startswith(".cfi")

    @staticmethod
    def skip_object(obj: SourceLine) -> bool:
        return (
            obj.get_mnemonic() in RiscvArch.skip_mnemonics
            or RiscvArch._is_cfi_directive(obj)
            and RiscvArch.skip_cfi_flag
        )

    @staticmethod
    def get_source() -> Source:
        return RiscvSource(RiscvArch.arch_name)

    @staticmethod
    def get_command_for_dead_code(free_registers) -> Command:
        commands = ["addi", "xori", "ori", "andi"]
        random_command = random.choice(commands)
        if len(free_registers) > 0:
            random_register = random.choice(free_registers)
            random_number = f"${random.randint(-65535, 65536)}"
            return Command(
                random_command, [f"%{random_register.lower()}", random_number]
            )

    @staticmethod
    def get_initial_registers() -> list[str]:
        return ["t1", "t2", "t3", "t4", "t5", "t6"]


class RiscvParser(ParserInterface):
    @staticmethod
    def parse(src: RiscvSource) -> None:
        types: dict[str, str] = {}
        sections = src.get_sections()
        for section in sections:
            types.update(RiscvParser._read_types(section))
        for section in sections:
            RiscvParser._read_objects(section, types)

    @staticmethod
    def _read_types(section: RiscvSection) -> dict[str, str]:
        result = {}
        for line in section.get_directives():
            if isinstance(line, RiscvObjectDirective):
                result[line.get_name()] = line.get_type()
        return result

    def _read_objects(section: RiscvSection, objects: dict[str, str]) -> None:
        directives = []
        lines = section.get_lines()
        ptr = 0
        if section.get_type() == "rodata" or section.get_type() == "srodata":
            RiscvParser._read_rodata(section)
        else:
            while ptr < len(lines):
                line = lines[ptr]
                if isinstance(line, RiscvObjectDirective):
                    ptr += 1
                elif isinstance(line, RiscvDirective):
                    directives.append(line)
                    ptr += 1
                elif isinstance(line, Label):
                    label_text = line.get_mnemonic()
                    if label_text in objects:
                        if objects[label_text] == "function":
                            length, obj = RiscvParser._read_function(
                                lines[ptr:], label_text, directives
                            )
                            obj.set_arch(RiscvArch)
                        elif objects[label_text] == "data":
                            length, obj = RiscvParser._read_data(
                                lines[ptr:], directives, label_text
                            )
                        directives = []
                        obj.add_label(line)
                        section.add_object(obj)
                        obj = None
                        ptr += length

    def _read_rodata(section: RiscvSection) -> None:
        ptr = 0
        lines = section.get_lines()
        dirs = []
        while ptr < len(lines):
            if isinstance(lines[ptr], Label):
                count, obj = RiscvParser._read_data(
                    lines[ptr + 1:], dirs, lines[ptr].get_mnemonic()
                )
                dirs = []
                section.add_object(obj)
                ptr += count + 1
            else:
                dirs.append(lines[ptr])
                ptr += 1

    def _read_data(
        lines: list[str], directives: list[RiscvDirective], name: str = ""
    ) -> (int, RiscvData):
        result = RiscvData(name)
        for directive in directives:
            result.add_directive(directive)
        result.add_element(lines[0])
        ptr = 1
        for line in lines[1:]:
            if isinstance(line, (RiscvObjectDirective, Label, RiscvGlobalDirective)):
                break
            result.add_element(line)
            ptr += 1
        return ptr, result

    @staticmethod
    def _read_function(
        lines: list[SourceLine], name: str, directives: list[RiscvDirective]
    ) -> (int, RiscvFunction):
        result = RiscvFunction(name)
        result.architecture = RiscvArch
        for directive in directives:
            result.add_directive(directive)
        # labels = []
        # ptr = 1
        # for line in lines[ptr:]:
        #     if isinstance(line, Label):
        #         labels.append(line)
        #     else:
        #         break
        # ptr += len(labels)
        ptr = RiscvParser.read_single_obj(result, lines)
        return ptr, result

    @staticmethod
    def read_data(lines: list[SourceLine]):
        result = RiscvData(lines[0].get_name())
        return RiscvParser.read_single_obj(result, lines[1:]) + 1, result

    @staticmethod
    def read_single_obj(obj: SourcePart, lines: list[SourceLine]):
        count = 0
        for line in lines:
            # if RiscvParser._end_object(line):
            #     return count
            count += 1
            if line.mnemonic == ".size" and isinstance(obj, RiscvFunction):
                obj.size_directive = line
                return count
            else:
                obj.add_element(line)
        return count

    # @staticmethod
    # def _end_object(line: SourceLine) -> bool:
    #     if isinstance(line, RiscvObjectDirective):
    #         return True
    #     if isinstance(line, Directive):
    #         if line.get_mnemonic() == ".cfi_endproc":
    #             return True
    #     return False

    @staticmethod
    def remove_comment(line: str) -> str:
        quote_flag = False
        escape_flag = False
        for i in range(len(line)):
            if line[i] == "\\":
                escape_flag = True
            if line[i] == '"' and not escape_flag:
                quote_flag = not quote_flag
            if line[i] == "#" and not quote_flag:
                return line[:i].strip()
            if line[i] != escape_flag:
                escape_flag = False
        return line.strip()

    @staticmethod
    def prepare_string(line: str) -> (str, list[str]):
        clear_string = RiscvParser.remove_comment(line)
        if len(clear_string) == 0:
            raise ValueError("expected non-empty string")
        arr = clear_string.split(maxsplit=1)
        if len(arr) > 1:
            result = [s.strip() for s in arr[1].split(",")]
        else:
            result = []
        return arr[0].strip(), result

    @staticmethod
    def get_initial_registers() -> list[str]:
        raise Exception("Realizovatb nado")


class RiscvPrinter(PrinterInterface):
    def print(source: RiscvSource, file):
        result = ""
        for section in source.get_sections():
            result += str(section)
        file.write(result)


class RiscvTarget(Target):
    @staticmethod
    def get_arch() -> ArchetectureInterface:
        return RiscvArch

    @staticmethod
    def get_parser() -> ParserInterface:
        return RiscvParser

    @staticmethod
    def get_printer() -> PrinterInterface:
        return RiscvPrinter


def get_target():
    return RiscvTarget
