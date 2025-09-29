#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp;
    char buffer[32];

    fp = fopen("test", "r");
    if (!fp) {
        perror("fopen");
        return 1;
    }

    // 尝试读 1 个元素，每个元素大小 31 字节
    size_t n = fread(buffer, 1, 31, fp);
    buffer[n] = '\0';  // 确保字符串结尾

    printf("Read %zu bytes: %s\n", n, buffer);

    fclose(fp);
    return 0;
}
