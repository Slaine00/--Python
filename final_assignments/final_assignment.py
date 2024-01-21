import sudoku
import sys
import csv
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
			if not n in range(1,10):
				return False

	except (TypeError, ValueError):
		return False

	return True

val_cmd = root.register(is_input_valid)

STATE_ERROR = "user1"
STATE_NOT_ERROR = "!user1"

style = ttk.Style()
style.theme_use("default")
style.map("Odd.TEntry", fieldbackground = [(STATE_ERROR,"red"),("!disabled","#f2e6ff"),("disabled","#f2ecf9")])
style.map("Even.TEntry",fieldbackground = [(STATE_ERROR,"red"),("!disabled","#e6fee6"),("disabled","#ecf9ec")])
style.map("TEntry",foreground=[(STATE_ERROR,"white"),(STATE_NOT_ERROR,"black")])


class CellEntry(ttk.Entry,sudoku.Cell):
	""" ttk.Entry および sudoku.Cell を継承した、数独のマスとして数字を入力するためのクラス。

	初期値が設定されているマスはユーザー側で変更することはできない。
	また、一桁の整数または空白以外の入力は受け付けない。
	マスの背景色は、そのマスが属するブロックの場所によって変更される。ブロックが奇数番目なら緑系、偶数番目なら紫系となる。
	また、文字色は独自フラグ user1 によって赤または黒にトグルされる。
 
	"""
	def __init__(self, master_grid, index:tuple[int,int], n:int, sv:tk.StringVar, *args, **kwargs) -> None:
		"""マスを GUI の Entry として生成する。

		Args:
			master_grid(EntryGrid): 自分の親である盤面。
			index(tuple[int,int]): マスのインデックス、行数と列数。
			n(int): マスの初期値。空きマスの場合は0。
			sv(tk.StringVar): 入力値を保持するための変数。

		"""
		self._INDEX = index
		self._SV = sv
		self.master_grid = master_grid

		is_odd_subgrid = (index[0]//3 + index[1]//3) % 2 == 1

		ttk.Entry.__init__(self,width=2, font=('Helvetica', 14), justify="center", style="Odd.TEntry" if is_odd_subgrid else "Even.TEntry",
				   validate="key", validatecommand=(val_cmd,'%P'), textvariable=sv,
				   *args, **kwargs,)
			
		self.insert(0,n)
		self.state(["!disabled" if n==0 else "disabled"])

		sudoku.Cell.__init__(self,n)

	@property
	def index(self):
		return self._INDEX
	
	@property
	def sv(self):
		return self._SV

	def on_user_input(self,*_) -> None:
		"""ユーザーからの入力を受け付ける。
		
		入力を数字に変換したうえで、親盤面のedit_numberメソッドを呼び出す。"""
		s = self.sv.get()
		self.master_grid.edit_number(self.index, 0 if s == "" else int(s))

class EntryGrid(sudoku.Grid):
	"""数独のGUI盤面を扱うクラス。
	
	Attributes: 
		grid(list[list[CellEntry]]): CellEntry で構成された盤面。"""
	def __init__(self, grid: list[list[int]]) -> None:
		"""数独のGUI盤面を呼び出す。
		
		Args:
			grid(list[list[int]]): 0以上9以下の整数を要素に持つ、初期盤面の数字の2次元リスト。空きマスは0で表す。"""
		super().__init__(grid)

		self.grid = [[CellEntry(master_grid=self, index=(i,j), n=grid[i][j], sv=tk.StringVar()) for j in range(9)] for i in range(9)]

		for i,row in enumerate(self.grid):
			for j,cell in enumerate(row):
				cell.grid(row=i, column=j,)
				cell.sv.trace_add("write", cell.on_user_input)

	def edit_number(self, index:tuple[int,int], n:int) -> None:
		"""指定されたマスに指定された数字を追加/変更/削除する。

		盤面の変更を行ったのち、盤面の数字の重複を確認し、ルール違反のマスについては state を変更する（文字色を変化させるため）。

		Args:
			index (tuple[int,int]): 指定するマスの行番号と列番号。0以上9未満の整数。
			n (int): 指定されたマスに入れる数字。0以上9以下の整数。0の場合は削除する。

		"""
		super().edit_number(index,n)

		duplicates = self.check_duplicate()

		for row in self.grid:
			for cell in row:
				cell.state([STATE_ERROR if cell.index in duplicates else STATE_NOT_ERROR])

tk.Frame(root, bg = "#ffffff").grid()

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

EntryGrid(input_list)

root.mainloop()
