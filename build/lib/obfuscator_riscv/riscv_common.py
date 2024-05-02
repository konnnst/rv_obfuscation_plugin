from obfuscator_core.common import (
    Source,
    Section,
    Label,
    Directive,
    SourceLine,
    JmpCommand,
    Command,
)
from obfuscator_core.code import Function
from obfuscator_core.data import Data


class RiscvDirective(Directive):
    def __init__(self, mnemonic: str, args: list[str]):
        self.type = None
        super().__init__(mnemonic, args)


class RiscvGlobalDirective(RiscvDirective):
    directives = [".globl"]


class RiscvDataDirective(RiscvDirective):
    directives = [
        ".byte",
        ".2byte",
        ".half",
        ".short",
        ".4byte",
        ".word",
        ".long",
        ".8byte",
        ".dword",
        ".quad",
        ".float",
        ".double",
        ".dtprelword",
        ".dtpreldword",
        ".sleb128",
        ".uleb128",
    ]

    def __init__(self, mnemonic: str, args: list[str]):
        super().__init__(mnemonic, args)


class RiscvSectionDirective(RiscvDirective):
    section_start = [".section", ".bss", ".rodata", ".data", ".text"]

    def _prepare_type(self, section_type):
        return section_type.split(".")[1]

    def __init__(self, mnemonic: str, args: list[str]):
        if mnemonic == ".section":
            self.section_type = None
            for el in args[:1]:
                self.section_type = self._prepare_type(el)
            super().__init__(".section", args)
        else:
            self.section_type = self._prepare_type(mnemonic)
            super().__init__(".section", [mnemonic])

    def get_type(self):
        return self.section_type

    @staticmethod
    def is_section_directive(directive: str):
        return directive.strip() in RiscvSectionDirective.section_start


class RiscvSection(Section):
    def __init__(self, directive: RiscvDirective):
        super().__init__(directive)
        self.lines = []

    def _not_printable(self, directive: RiscvDirective) -> bool:
        for key in self.objects.keys():
            if (
                directive in self.objects[key].elements
                or directive in self.objects[key].directives
                or directive.get_mnemonic() == ".size"
                or isinstance(directive, RiscvObjectDirective)
            ):
                return True
        return False

    def __str__(self):
        result: str = ""
        for directive in self.directives:
            if not self._not_printable(directive):
                result += str(directive) + "\n"
        result += str(self.start_directive) + "\n"
        for object_name in self.objects.keys():
            result += str(self.objects[object_name])
        return result

    def add_element(self, element: SourceLine):
        self.lines.append(element)

    def get_lines(self) -> list:
        return self.lines

    def get_type(self) -> str:
        return self.get_start_directive().get_type()

    def is_empty(self) -> bool:
        return len(self.lines) == 0

    @staticmethod
    def get_section(dir: RiscvSectionDirective) -> Section:
        if dir.get_type() and dir.get_type() == ".text":
            return RiscvCodeSection(dir)
        elif dir.get_type() and dir.get_type() in [
            ".bss",
            ".data",
            ".rodata",
            ".sbss",
            ".sdata",
            ".srodata",
        ]:
            return RiscvDataSection(dir)
        else:
            return RiscvSection(dir)


class RiscvSource(Source):
    def __init__(self, name: str):
        super().__init__(name)
        self.text_sections = []
        self.data_sections = []
        self.rodata_sections = []

    def add_section(self, section: RiscvSection) -> None:
        if not isinstance(section, RiscvSection):
            raise ValueError("Expected section for RISC-V architecture")
        super().add_section(section)


class RiscvObjectDirective(RiscvDirective):
    directives = [".type"]

    def __init__(self, mnemonic: str, args: list[str]):
        super().__init__(mnemonic, args)
        self.name = args[0]
        for str in args[1:]:
            if str == "@function":
                self.type = "function"
            elif str == "@object":
                self.type = "data"

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name


class RiscvDataSection(RiscvSection):
    def is_code_section(self):
        return False

    def is_data_section(self):
        return True


class RiscvCodeSection(RiscvSection):
    def is_code_section(self):
        return True

    def is_data_section(self):
        return False


class RiscvData(Data):
    def __init__(self, name: str):
        super().__init__(name)

    def add_directive(self, directive: Directive):
        if isinstance(directive, RiscvDataDirective):
            self.add_element(directive)
        else:
            super().add_directive(directive)

    def __str__(self):
        result = ""
        for directive in self.directives:
            if directive not in self.elements:
                result += str(directive) + "\n"
        result += str(Label(self.name)) + "\n"
        for element in self.elements:
            result += str(element) + "\n"
        return result


class RiscvFunction(Function):
    def __init__(self, name: str):
        self.size_directive = None
        super().__init__(name)

    def __str__(self):
        result = ""
        for directive in self.directives:
            if directive not in self.elements:
                result += str(directive) + "\n"
        result += str(RiscvDirective(".type", [self.name, "@function"])) + "\n"
        for linear_section in self.lin_sections:
            result += str(linear_section)
        if self.size_directive is not None:
            result += str(self.size_directive) + "\n"
        return result


class RiscvJmpCommand(JmpCommand):
    def get_jump_label(self):
        return self.get_args()[-1]


class RiscvCommand(Command):
    def _get_save_address(self):
        arg = self.args[1]
        for i in range(len(arg)):
            if arg[i] == "(":
                left_bracket = i
            elif arg[i] == ")":
                right_bracket = i
        return arg[left_bracket + 1: right_bracket]

    def get_affected_registers(self):
        if len(self.args) > 0:
            # 32-bit basic arithmetic operations
            if self.mnemonic in [
                "addi",
                "andi",
                "xori",
                "ori",
                "slri",
                "srai",
                "slli",
                "add",
                "sub",
                "sll",
                "slt",
                "sltu",
                "srl",
                "sra",
                "xor",
                "or",
                "and",
            ]:
                return [self.args[0]]
            # 64-bit basic arithmetic operations
            if self.mnemonic in [
                "addiw",
                "slliw",
                "srliw",
                "sraiw",
                "addw",
                "subw",
                "sllw",
                "srlw",
                "sraw",
            ]:
                return [self.args[0]]
            # load from memory to register
            elif self.mnemonic in [
                "la",
                "lb",
                "lh",
                "lw",
                "lbu",
                "lwu",
                "lhu",
                "li",
                "lui",
                "ld",
                "lla",
            ]:
                return [self.args[0]]
            # multiplication extension
            elif self.mnemonic in [
                "mul",
                "mulh",
                "mulhsu",
                "mulhu",
                "div",
                "divu",
                "rem",
                "remu",
            ]:
                return [self.args[0]]
            # save to register
            elif self.mnemonic in ["sb", "sh", "sw", "sd"]:
                return [self._get_save_address()]
            # jump and link commands
            elif self.mnemonic in ["jl", "jalr"]:
                return [self.args[0]]
        return []
