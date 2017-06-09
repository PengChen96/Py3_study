
# dictionary 字典（其他语言中的map） 使用key-value存储
# dict中的 key 必须是不可变对象

dict = {'a':1 , 'b':2, 'c':3}
print(dict)         # {'a': 1, 'b': 2, 'c': 3}
print(dict['b'])    # 2

dict['d'] = 4
print(dict)         # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
print(dict['d'])    # 4

print('a' in dict)  # True  判断 key 'a' 是否存在
print('e' in dict)  # False

print(dict.get('e'))    # None  如果 key 'e' 不存在，返回None
print(dict.get('e', -1))    # -1  如果 key 'e' 不存在，输出自己指定value为-1
print(dict)             # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

dict.pop('d')       # 删除key 'd' 和 value
print(dict)         # {'a': 1, 'b': 2, 'c': 3}

# 和list比较，dict有以下几个特点：
#   查找和插入的速度极快，不会随着key的增加而变慢；
#   需要占用大量的内存，内存浪费多。


# set 一组key的集合，但不存储value, 由于key不能重复，所以set是无序不重复元素的序列
# 不可放入可变对象

s = set([1,2,3,1,2,3])
print(s)            # {1, 2, 3}   重复元素会自过滤

s.add('a')          # 添加元素到set中
print(s)            # {1, 2, 3, 'a'}
s.remove('a')       # 删除元素 key 'a'
print(s)            # {1, 2, 3}

# set集合运算
a = {'a','b','c'}
b = {'a','b','d'}
print(a-b)      # a和b的差集 {'c'}
print(a|b)      # a和b的并集 {'b', 'd', 'a', 'c'}
print(a&b)      # a和b的交集 {'b', 'a'}
print(a^b)      # a和b中不同时存在的元素 {'c', 'd'}

