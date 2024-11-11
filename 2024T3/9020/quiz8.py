from math import comb

def find_n():
    # 尝试不同的n值
    for n in range(1, 10):  # 从小到大尝试n的值
        total_books = 2*n + 1  # 总书数
        ways = 0
        
        # 计算选择1到n本书的所有可能方式
        for r in range(1, n+1):
            # 使用组合公式C(2n+1, r)计算从2n+1中选择r本书的方式数
            ways += comb(total_books, r)
        
        # 检查总和是否等于63
        if ways == 63:
            return n
            
    return None

result = find_n()
print(f"n = {result}")

# 验证结果
if result:
    n = result
    total_books = 2*n + 1
    ways = 0
    print(f"\n验证过程:")
    print(f"总书数 = {total_books}")
    for r in range(1, n+1):
        combination = comb(total_books, r)
        ways += combination
        print(f"选择{r}本书的方式数: C({total_books},{r}) = {combination}")
    print(f"总方式数: {ways}")