import tkinter as tk
import tkinter.filedialog
import math

# tkinter の filedialog だけを利用する例

# root ウィンドウ： withdrow() メソッドを呼んで隠す
root = tk.Tk()
root.withdraw()

# 書き出し用の filedialog を読んでファイル名を得る
filename = tkinter.filedialog.asksaveasfilename()

# tkinter を終了
root.destroy()

# ファイル名がもらえなければ終了
if filename:
	pass
else:
	print("No file specified")
	exit()
	
# 正弦波の重ね合わせで鋸波を近似
# w = sin(t) + sin(2t)/2 + sin(3t)/3 + ...
# ２周期分、全体は1000ステップで、高調波は5番目まで
cycles = 2
steps = 1000
harmonics = 5
# ファイルを開く、開けない場合のエラー対応も
try:
	with open(filename, 'w') as file:
		for i in range(steps):
			angle_in_degree = 360 * cycles * i/steps
			angle = math.radians(angle_in_degree)
			s = str(angle_in_degree)
			w = 0
			
			for j in range(1, harmonics+1):
				w += math.sin(angle*j)/j
				s = s + ", " + str(w)
				
			file.write(s + "\n")
			
		print(f"Writing to file {filename} is finished")
		
except IOError:
	print("Unable to open file")
