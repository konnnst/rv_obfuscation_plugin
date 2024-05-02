import pytest
from obfuscator_riscv.riscv_configuration import RiscvArch
from obfuscator_core.common import JmpCommand
from obfuscator_riscv.riscv_common import (
    RiscvObjectDirective,
    RiscvGlobalDirective,
    RiscvDataDirective,
    RiscvSectionDirective,
    RiscvDirective,
    RiscvCodeSection,
    RiscvDataSection,
)


@pytest.mark.parametrize(
    "line,mnemonic,args,dirtype",
    [
        (".section	.rodata", ".section", [".rodata"], RiscvSectionDirective),
        (".globl main", ".globl", ["main"], RiscvGlobalDirective),
        (".bss #ololols # .section", ".section", [".bss"], RiscvSectionDirective),
        (
            ".type	print, @function",
            ".type",
            ["print", "@function"],
            RiscvObjectDirective,
        ),
        (".word 30", ".word", ["30"], RiscvDataDirective),
        (".align 1", ".align", ["1"], RiscvDirective),
        ('.string "#: abc " #cde', ".string", ['"#: abc "'], RiscvDirective),
    ],
)
def test_get_directive(line: str, mnemonic: str, args: list[str], dirtype):
    dir = RiscvArch.get_directive(line)
    assert dir.get_mnemonic() == mnemonic
    assert dir.get_args() == args
    assert isinstance(dir, dirtype)


@pytest.mark.parametrize(
    "line,mnemonic,args,is_jump",
    [
        ("addi	sp,sp,-32", "addi", ["sp", "sp", "-32"], False),
        ("jr ra", "jr", ["ra"], True),
        ("blt s1,s2,branch", "blt", ["s1", "s2", "branch"], True),
        ("sw	zero,-20(s0)", "sw", ["zero", "-20(s0)"], False),
    ],
)
def test_get_command(line: str, mnemonic: str, args: list[str], is_jump: bool):
    cmd = RiscvArch.get_command(line)
    print(type(cmd))
    assert cmd.get_mnemonic() == mnemonic
    assert cmd.get_args() == args
    assert isinstance(cmd, JmpCommand) == is_jump


@pytest.mark.parametrize(
    "line, mnemonic", [("main:", "main"), (".LC1: # random comment", ".LC1")]
)
def test_get_label(line: str, mnemonic: str):
    label = RiscvArch.get_label(line)
    assert label.get_mnemonic() == mnemonic
    assert len(label.get_args()) == 0


@pytest.mark.parametrize(
    "start_directive_line, dir_lines, type",
    [
        (".bss", [], RiscvDataSection),
        (".section .text", [], RiscvCodeSection),
        (".text", [], RiscvCodeSection),
        (".data", [], RiscvDataSection),
    ],
)
def test_get_section(start_directive_line: str, dir_lines: list, type):
    dir = RiscvArch.get_directive(start_directive_line)
    dirs = list(map(RiscvArch.get_directive, dir_lines))
    section = RiscvArch.get_section(dir, dirs)
    assert isinstance(section, type)
