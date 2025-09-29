# 总结
就是在free完后notelist仍然有free掉的堆块地址<br>
先创建两个32大小堆块的<br>
然后就会有两个0x10的header,两个0x30的content<br>
所以free两次，把这四个堆块都free掉<br>
再创建一个内容是0x10的块，那么就能写入之前后free的那个header<br>
实现UAF<br>