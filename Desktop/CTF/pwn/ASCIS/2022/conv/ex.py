from pwn import *
bin = './convert'
elf = ELF(bin)
r= elf.process()
r.interactive()
