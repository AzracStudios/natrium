from asm import *
import os

class Compiler:

    def __init__(self, code, file_name, props):
        self.code = code
        self.file_name = file_name
        self.props = props

    def generate_final(self):
        return ASM_BASE + self.code + ASM_EXIT

    def write_out(self):
        file_name = f"{self.file_name}.asm"
        os.system(f"touch {file_name}")

        with open(file_name, "w") as f:
            f.write(self.code)

    def compile(self):
        self.code = self.generate_final()
        self.write_out()

        os.system(f"nasm -f elf64 -o {self.file_name}.o {self.file_name}.asm")
        os.system(f"ld -o {self.file_name} {self.file_name}.o")
        
        if self.props["keep"]: return
        os.system(f"rm {self.file_name}.o {self.file_name}.asm")