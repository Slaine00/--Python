import tkinter as tk

# 計算機能のための変数とイベント用の関数定義

# ２項演算のモデル
# 入力中の数字
current_number = 0
# 第一項
first_term = 0
# 第二項
second_term = 0
#演算
CALCS = {"plus":lambda x,y: x+y, "minus":lambda x,y: x-y, "times":lambda x,y: x*y, "div":lambda x,y: x//y}
operate = lambda:"error"
# 結果
result = 0

def do_operators(op):
	"演算子キーが押されたときの計算動作、第一項の設定と入力中の数字のクリア"
	global current_number
	global first_term
	global operate
	
	first_term = current_number
	operate = CALCS[op]

	current_number = 0
	
def do_eq():
	"＝キーが押されたときの計算動作、第二項の設定、加算の実施、入力中の数字のクリア"
	global second_term
	global result
	global current_number
	
	second_term = current_number
	result = operate(first_term, second_term)
	
	current_number = 0
	
# 数字キーの Call Back 関数
num_keys = [lambda x=i: key(x) for i in range(10)]

# 数字キーを一括処理する関数
def key(n):
	global current_number
	
	current_number = current_number * 10 + n
	show_number(current_number)
	
# クリアキーの処理
def clear():
	global current_number
	
	current_number = 0
	show_number(current_number)
	
# + キーの処理
def plus():
	do_operators("plus")
	show_number(current_number)
# - キーの処理
def minus():
	do_operators("minus")
	show_number(current_number)
# * キーの処理
def times():
	do_operators("times")
	show_number(current_number)
# /キーの処理
def div():
	do_operators("div")
	show_number(current_number)
	
# ＝キーの処理
def eq():
	do_eq()
	show_number(result)
	
#数値をエントリーに表示
def show_number(num):
	e.delete(0, tk.END)
	e.insert(0, str(num))
	
# tkinterでの画面の構成
root = tk.Tk()
f = tk.Frame(root, bg="#ffffc0")
f.grid()

# ウィジェットの作成
class calcButton(tk.Button):
	def __init__(self, *args, **kwargs):
		super().__init__(width=2, font=('Helvetica', 14), *args, **kwargs,)


num_b = [calcButton(f, text=f'{i}', command=num_keys[i], bg="#ffffff") for i in range(10)]
bc = calcButton(f, text='c', command=clear, bg="#ff0000")
bp = calcButton(f, text='+', command=plus, bg="#00ff00")
bm = calcButton(f, text="-", command=minus, bg="#00ff00")
bt = calcButton(f, text="×", command=times, bg="#00ff00")
bd = calcButton(f, text="÷", command=div, bg="#00ff00")
be = calcButton(f, text='=', command=eq, bg="#00ff00")

# Grid 型ジオメトリマネージャによるウィジェットの割付
buttons = [
	[num_b[7], num_b[8], num_b[9], bd],
	[num_b[4], num_b[5], num_b[6], bt],
	[num_b[1], num_b[2], num_b[3], bm],
	[num_b[0], bc, be, bp],
]

for i , row in enumerate(buttons):
	for j, button in enumerate(row):
		button.grid(row=i+1, column=j, )

# 数値を表示するウィジェット
e = tk.Entry(f)
e.grid(row=0, column=0, columnspan=4)
clear()

# GUI スタート
root.mainloop()
