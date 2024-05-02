from setuptools import setup

BASE_VERSION = "0.0.0"

setup(
    name="obfuscator-riscv",
    entry_points={
        "arch": ["risc-v = obfuscator_riscv.__main__:get_target"],
        "console_scripts": ["risc-v = obfuscator_riscv.__main__:main"],
    },
    package_dir={"": "src"},
    version=BASE_VERSION,
)
