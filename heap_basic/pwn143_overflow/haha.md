# 这道题有两种解法
## 第一种是house of force
简而言之就是通过修改topchunk<br>
之后再free很大的一个堆块，输入负数转化成0XFFFFFxxx，之后就可以实现任意迁移topchunk<br>
之后开chunk就可以任意位置读写<br>
使用条件<br>
- 可以堆溢出
- 可以开辟很大堆块（input_leangth的参数类型是int而不是unsigned）
## 第二种是unlink
首先要有一个chunklist<br>
然后构造伪堆块，假free，之后可以实现通过unlink对bss段的chunklist进行修改<br>
其实也就是任意位置读写，当然你要知道在哪里读写<br>
使用条件<br>
- 可以堆溢出（1byte）