# 总结
可以理解为<br>
通过溢出一字节，修改chunk大小<br>
对这种有headchunk存在的情况<br>
让一块同时被free两个部分<br>
实现内存的串用<br>