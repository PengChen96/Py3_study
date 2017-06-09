
# 递归函数

def fact(n):
    if n==1:
        return 1
    return n*fact(n-1)

print(fact(3))          # 1x2x3 = 6

# 尾递归
def fact(n):
    return fact_iter(n,1)
def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num-1,num*product)

print(fact(5))          # 1x2x3x4x5 = 120