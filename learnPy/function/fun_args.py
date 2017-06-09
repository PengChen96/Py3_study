
def power(x, n=2):
    s = 1;
    while n>0:
        n = n - 1
        s = s * x
    return s

print(power(3))         # 3^2   9
print(power(3,3))       # 3^3   27
# 一是必选参数在前，默认参数在后，否则Python的解释器会报错
# （思考一下为什么默认参数不能放在必选参数前面） 因为会产生歧义
# 二是如何设置默认参数。
# 当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数。

def reg(name, gender, age=18, city="hangzhou"):
    print("name:",name)
    print("gender:",gender)
    print("age:",age)
    print("city:"+city)

reg('pc','boy')
# name: pc
# gender: boy
# age: 18
# city:hangzhou
reg('pc','boy',city='linan')
# name: pc
# gender: boy
# age: 18
# city:linan


def calc(nums):
    sum = 0
    for n in nums:
        sum += n*n
    return  sum

print(calc([1,2,3]))        # 14

# 可变参数     list or tuple()
def calc(*nums):
    sum = 0
    for n in nums:
        sum += n * n
    return sum

print(calc(1,2,3))          # 14

# *nums表示把nums这个list的所有元素作为可变参数传进去。
nums = [1,2,3]
print(calc(*nums))          # 14

# 关键字参数    dict
def person(name,age,**kw):
    print("name:",name)
    print("age:",age)
    print('other:',kw)

person('pc',16,gender='boy')
# name: pc
# age: 16
# other: {'gender': 'boy'}
extra = {'gender':'girl', 'city':'hangzhou'}
person('pc',18,**extra)
# name: pc
# age: 18
# other: {'gender': 'girl', 'city': 'hangzhou'}

# 命名关键字参数
def person(name,age,*,gender,city):
    print("name:",name)
    print("age:",age)
    print("gender:",gender)
    print("city:",city)

person('pc',18,gender='boy',city="hangzhou")
# name: pc
# age: 18
# gender: boy
# city: hangzhou
