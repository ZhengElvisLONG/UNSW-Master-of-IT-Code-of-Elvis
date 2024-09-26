#include <stdio.h>
#include <stdlib.h>

// 冒泡排序函数
void bubbleSort(int *arr, int size) {
    // 外层循环控制排序的轮数，每次将最大的元素移动到末尾
    for (int i = 0; i < size - 1; i++) {
        int swapped = 0; // 标记是否发生了交换，如果没有交换则提前结束排序
        // 内层循环进行相邻元素的比较和交换
        for (int j = 0; j < size - i - 1; j++) {
            // 如果当前元素大于下一个元素，交换它们
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];    // 使用临时变量保存当前元素
                arr[j] = arr[j + 1];  // 将下一个元素赋值给当前元素
                arr[j + 1] = temp;    // 将临时变量中的值赋值给下一个元素
                swapped = 1;          // 标记已经发生了交换
            }
        }
        // 如果一轮排序中没有发生交换，数组已经是有序的，可以提前结束
        if (!swapped) {
            return;
        }
    }
}

int main(void) {
    int *arr = NULL;  // 初始化指针为 NULL，表示数组尚未分配内存
    int capacity = 0; // 当前数组的容量，初始为 0
    int size = 0;     // 当前数组的实际大小，初始为 0
    int input;        // 存储用户输入的整数

    printf("请输入整数，输入任意非数字字符以停止：\n");

    // 读取用户输入的整数直到输入非整数字符为止
    while (scanf("%d", &input) == 1) {
        // 检查数组是否需要扩展
        if (size >= capacity) {
            // 如果当前容量为 0，则设置初始容量为 2
            // 否则，容量增加 1（动态扩展）
            capacity = (capacity == 0) ? 2 : capacity + 1;
            // 动态分配或重新分配内存
            arr = realloc(arr, capacity * sizeof(int));
            // 检查内存分配是否成功
            if (arr == NULL) {
                printf("内存分配失败\n");
                return 1; // 返回 1 表示发生错误
            }
        }
        // 将输入的整数存入数组，并增加数组的实际大小
        arr[size++] = input;
    }

    // 打印用户输入的数组元素
    printf("您输入的数组元素是：\n");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // 对数组进行冒泡排序
    bubbleSort(arr, size);

    // 打印排序后的数组元素
    printf("经排序的数组元素是：\n");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // 释放动态分配的内存
    free(arr);

    return 0; // 返回 0 表示程序成功结束
}
