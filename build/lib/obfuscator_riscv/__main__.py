from obfuscator_core.obfuscator import ObfuscatorApp
from .riscv_configuration import get_target


def main():
    print("Obfuscator plugin for RISC-V running")
    ObfuscatorApp({"risc-v": get_target}).run()


if __name__ == "__main__":
    main()
