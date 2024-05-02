import pytest
from obfuscator_riscv.riscv_configuration import RiscvArch


@pytest.mark.parametrize(
    "line,result",
    [
        (
            ".attribute arch,"
            + '"rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"',
            True,
        ),
        (".type	a, @object", True),
        (".LC0:", False),
        ("addi sp,sp,32", False),
        ("jr ra", False),
        ("....jfjksfksdjfk: #comment ololo", False),
        ("F1:", False),
    ],
)
def test_is_directive(line: str, result: bool):
    assert RiscvArch.is_directive(line) == result


@pytest.mark.parametrize(
    "line,result",
    [
        (
            ".attribute arch,"
            + '"rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"',
            False,
        ),
        (".type	a, @object", False),
        (".LC0:", False),
        ("addi sp,sp,32 #comment: 30 and mm top #", True),
        ("jr ra", True),
        ("....jfjksfksdjfk: #comment ololo", False),
        ("F1:", False),
    ],
)
def test_is_command(line: str, result: bool):
    assert RiscvArch.is_command(line) == result


@pytest.mark.parametrize(
    "line,result",
    [
        (
            ".attribute arch,"
            + '"rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"',
            False,
        ),
        (".type	a, @object", False),
        (".LC0:", True),
        ("addi sp,sp,32", False),
        ("jr ra", False),
        ("....jfjksfksdjfk: #comment ololo", True),
        ("F1:", True),
    ],
)
def test_is_label(line: str, result: bool):
    assert RiscvArch.is_label(line) == result


@pytest.mark.parametrize(
    "line,result",
    [
        (
            ".attribute arch,"
            + '"rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"',
            False,
        ),
        (".type	a, @object", False),
        (".LC0:", False),
        ("addi sp,sp,32", False),
        ("jr ra", False),
        ("....jfjksfksdjfk: #comment ololo", False),
        ("F1:", False),
        (".section", True),
        (".section .bss", True),
        (".text", True),
    ],
)
def test_is_section_start(line: str, result: bool):
    assert RiscvArch.is_section_start(line) == result


@pytest.mark.parametrize(
    "line,result",
    [
        ("call	printf@plt # ololo m228, m1337 ", False),
        ("ololo m228, m1337", True),
        (".LC0:", False),
        ("main:", False),
        (".null_pointer:", True),
        (".size	main, .-main", False),
        (".ident", True),
    ],
)
def test_skip_object(line: str, result: bool):  # requires testing
    RiscvArch.skip_mnemonics.extend([".null_pointer", "ololo"])
    if RiscvArch.is_command(line):
        obj = RiscvArch.get_command(line)
    elif RiscvArch.is_directive(line):
        obj = RiscvArch.get_directive(line)
    elif RiscvArch.is_label(line):
        obj = RiscvArch.get_label(line)
    assert RiscvArch.skip_object(obj) == result
