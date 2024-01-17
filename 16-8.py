# Numpy のデータを plot する

import matplotlib
matplotlib.use('tkagg')

import matplotlib.pyplot as plt
import numpy as np

# 使用機は Windows
matplotlib.rc('font', **{'family':'Yu Gothic'})

# x の 1乗から4乗までをプロットする
steps = 100
order = 4
maxx = 2

# steps 行、order 列の零行列を作成
datalist = np.zeros((steps,order))

# 凡例用のリスト
legend_label = []

# x の値を linspace で作成
x = np.linspace(0,maxx,steps)

# 各列について計算
for j in range(1,order+1):
    datalist[:,j-1] = x**j
    legend_label.append(str(j)+"乗")

# プロット
plt.plot(x,datalist)
plt.title('x のべき乗')
plt.xlabel('x')
plt.ylabel('x**n')
plt.legend(legend_label)
plt.show()