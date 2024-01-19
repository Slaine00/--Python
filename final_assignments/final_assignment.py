import sudoku
import sys
import csv

args = sys.argv

if len(args) == 1:
	input_list = [[0, 1, 8, 0, 0, 0, 3, 2, 0],
                 [2, 5, 0, 0, 0, 0, 0, 4, 6],
                 [0, 0, 4, 6, 5, 2, 1, 0, 0],
                 [0, 0, 6, 0, 7, 0, 2, 0, 0],
                 [0, 2, 0, 0, 4, 0, 0, 5, 0],
                 [0, 0, 3, 1, 0, 8, 7, 0, 0],
                 [0, 0, 2, 5, 3, 9, 4, 0, 0],
                 [4, 9, 0, 0, 0, 0, 0, 8, 3],
                 [0, 7, 0, 0, 0, 0, 0, 9, 0]]
                          
else:
	with open(args[1]) as f:
		reader = csv.reader(f)
		input_list = [[int(s) for s in row] for row in reader]
		print(input_list)
 
quiz_grid = sudoku.Grid(input_list)


# GUI
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

def is_input_valid(s:str) -> bool:
	"""入力が数独の入力として有効かを判定する。
	
	1から9までの整数または空白が有効。

	Args:
		s(str): 入力された文字列。

	Returns:
		bool: 有効なら True, 不正なら False 。

	"""
	try:
		if s == "":
			pass

		else:
			n = int(s)
			sudoku.check_number(n)

	except (TypeError, ValueError):
		return False

	return True

val_cmd = root.register(is_input_valid)

STATE_ERROR = "user1"
STATE_NOT_ERROR = "!user1"

style = ttk.Style()
style.theme_use("default")
style.map("TEntry",foreground=[(STATE_ERROR,"red"),(STATE_NOT_ERROR,"black")],)
style.map("Odd.TEntry", fieldbackground = [("!disabled","#f2e6ff"),("disabled","#f2ecf9")])
style.map("Even.TEntry",fieldbackground = [("!disabled","#e6fee6"),("disabled","#ecf9ec")])


class CellEntry(ttk.Entry):
	""" ttk.Entry を継承した、数独のマスとして数字を入力するためのクラス。

	初期値が設定されているマスはユーザー側で変更することはできない。
	また、一桁の整数または空白以外の入力は受け付けない。
	"""
	def __init__(self, index:tuple[int,int], n:int, sv:tk.StringVar, *args, **kwargs) -> None:
		"""マスを GUI の Entry として生成する。
		
		Args:
			index(tuple[int,int]): マスのインデックス、行数と列数。
			n(int): マスの初期値。空きマスの場合は0。
			sv(tk.StringVar): 入力値を保持するための変数。

		"""
		self._INDEX = index
		self._SV = sv

		is_odd_subgrid = (index[0]//3 + index[1]//3) % 2 == 1

		super().__init__(width=2, font=('Helvetica', 14), justify="center", style="Odd.TEntry" if is_odd_subgrid else "Even.TEntry",
				   validate="key", validatecommand=(val_cmd,'%P'), textvariable=sv,
				   *args, **kwargs,)

		if n==0:
			text = ""
			is_editable = True
		else:
			text = str(n)
			is_editable = False
			
		self.insert(0,text)
		self.state(["!disabled" if is_editable else "disabled"])

	@property
	def index(self):
		return self._INDEX
	
	@property
	def sv(self):
		return self._SV

	def edit(self,*_):
		"""マスの数字の変更を内部の盤面に反映させる。
		
		反映させたのち、盤面全体についてルール違反のマスが存在するかの確認を行う。"""
		s = self.sv.get()
		quiz_grid.edit_number(self.index, 0 if s == "" else int(s))

		duplicates = quiz_grid.check_duplicate()

		for row in cells:
			for cell in row:
				cell.state([STATE_ERROR if cell.index in duplicates else STATE_NOT_ERROR])

tk.Frame(root, bg = "#ffffff").grid()

cells = [[CellEntry((i,j), quiz_grid.get_cell((i,j)), tk.StringVar()) for j in range(9)] for i in range(9)]

for i,row in enumerate(cells):
	for j,cell in enumerate(row):
		cell.grid(row=i, column=j,)
		cell.sv.trace_add("write", cell.edit)


root.mainloop()
