
# list 有序集合，可以随时添加删除其中的元素；

p_list = ['a', 'b', 'c']
print(p_list)           # ['a', 'b', 'c']
print(len(p_list))      # 3
print(p_list[0])        # a
print(p_list[-1])       # c     倒数第一个元素

p_list.append('d')      # 末尾追加元素
print(p_list)           # ['a', 'b', 'c', 'd']

p_list.insert(1, 'e')   # 插入到索引为1的位置
print(p_list)           # ['a', 'e', 'b', 'c', 'd']

p_list.pop()            # 删除末尾元素
print(p_list)           # ['a', 'e', 'b', 'c']

p_list.pop(1)           # 删除索引为1的元素
print(p_list)           # ['a', 'b', 'c']


# tuple元组 有序列表，初始化后就不能修改

p_tuple_fake = ('a')    # 这时（）表示了数学公式中的小括号
print(p_tuple_fake)     # a
p_tuple_true = ('a',)   # 要表示元组，后面加个逗号，避免歧义
print(p_tuple_true)     # ('a',)

p_tuple = ('a', 'b', ['A', 'C'])
print(p_tuple)          # ('a', 'b', ['A', 'C'])
# p_tuple[0] = 'c'      TypeError: 'tuple' object does not support item assignment
p_tuple[2][1] = 'B'     # “可变”的元组？？
print(p_tuple)          # ('a', 'b', ['A', 'B'])

