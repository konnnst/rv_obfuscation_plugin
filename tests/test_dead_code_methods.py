import pytest

from obfuscator_riscv.riscv_configuration import RiscvArch


@pytest.mark.parametrize(
    "raw_command,affected_registers",
    [
        ("addi sp,sp,-32", ["sp"]),
        ("sw zero,-20(s0)", ["s0"]),
        ("lla a0,.LC0", ["a0"]),
        ("j .L2", []),
        ("lw a5,-20(s0)", ["a5"]),
    ],
)
def test_get_command(raw_command: str, affected_registers: list[str]):
    command = RiscvArch.get_command(raw_command)
    assert command.get_affected_registers() == affected_registers
