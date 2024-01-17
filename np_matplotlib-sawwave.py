#
#
# Numpy のデータを plot する例題
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np
#
# For Windows
#
matplotlib.rc('font', **{'family':'Yu Gothic'})
#
# For Mac
#
#matplotlib.rc('font', **{'family':'Hiragino Maru Gothic Pro'})
#
# x の 1乗 ~ 4 乗をプロットする
#
cycles = 2
steps = 1000
harmonics = 8
maxx = cycles*2*np.pi
#
# 要素の値 0 で steps 行、 order 列の行列を作成
#
datalist = np.zeros((steps, harmonics))
#
# 凡例用のリスト
#
legend_label=[]
#
# x の値を linspace で作成
#
x = np.linspace(0,maxx,steps)
x_in_degree = np.linspace(0,360*cycles,steps)
#
# 各列について、一気に計算する
# 
for j in range(1,harmonics+1):
   print(j)
#
# 以下の作業をする
#
# 右辺を j に応じて書き換える，まず最終項を作る
   datalist[:,j-1] =  np.sin(j*x)/j

#  j が 1 より大きければ，一つ手前の列を加えて総和にする
   if j!=1:
      datalist[:,j-1] += datalist[:,j-2]
   legend_label.append(str(j)+"項までの和")
#
# プロット
#
plt.plot(x_in_degree, datalist)
plt.title('鋸歯状波の近似')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(legend_label)
plt.show()

        
