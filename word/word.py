from os import path
# 安装scipy模块前，先安装numpy+mkl
from scipy.misc import imread
import matplotlib.pyplot as plt
# import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)
# print(path.join(d, 'Py_study.txt'))
# 读取文本 alice.txt 在包文件的example目录下

text = open(path.join(d, 'word.txt'),encoding='utf8').read()
# text = " ".join(jieba.cut(open(path.join(d, 'word.txt'),encoding='utf8').read()))
# print(text)

# read the mask / color image
# taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
# 设置背景图片
alice_coloring = imread(path.join(d, "word.png"))

wc = WordCloud(background_color="white", #背景颜色
max_words=2000,# 词云显示的最大词数
font_path='./ttf/simhei.ttf',
mask=alice_coloring,#设置背景图片
stopwords=STOPWORDS.add("said"),
max_font_size=40, #字体最大值
random_state=42)
# 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(alice_coloring)

# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
# 绘制词云
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(alice_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
# wc.to_file(path.join(d, "cp.png"))