from capstone import *

def disassemble_file(filename):
    result = ""
    with open(filename, 'rb') as f:
        content = f.read()

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True

    for insn in md.disasm(content, 0x0):
        result += "0x%x:\t%s\t%s\n" % (insn.address, insn.mnemonic, insn.op_str)
    
    return result
