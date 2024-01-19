# -*- coding: utf-8 -*-
"""数独関係の処理を行うためのモジュール。
"""
import itertools

def check_index(n:any, name:str="") -> None:
	"""与えられた引数がマスのインデックスとして有効か判定する。

	Args:
		n (any): 判定の対象。
		name (str): 判定の対象の変数名。

	Raises:
		TypeError: n が int でない場合に発生。
		ValueError: n が0以上9未満の範囲にない場合に発生。

	"""
	if type(n) != int:
		raise TypeError(f"The argument '{name}' must be of type int.")

	if not n in range(9):
		raise ValueError(f"The argument '{name}' must be an integer in the range of 0 to 8.")


class Cell:
	def __init__(self,n:int) -> None:
		self._value = n

	@property
	def value(self):
		return self._value
	
	@value.setter
	def value(self, n):
		if type(n) != int:
			raise TypeError(f"The cell value must be of type int.")

		if not n in range(10):
				raise ValueError(f"The cell value must be an integer in the range of 0 to 9.")

		self._value = n

class Grid:
	"""数独の盤面を扱うためのクラス。
	"""

	def __init__(self, grid: list[list[int]]) -> None:
		"""数独の盤面を生成する。

		9x9の2次元リストを数独の盤面として生成する。数字が書かれていないマスは0として扱う。

		Args:
			grid (list[list[int]]): cell を要素に持つサイズ9x9のリスト。

		Raises:
			TypeError: grid が2次元リストでない場合に発生。
			ValueError: grid のサイズが9x9でない場合に発生。

		Note:
			初期盤面が矛盾を含んでいるケース、および解決不可能なケースは想定していない。

		"""
		if type(grid) != list or not sum([type(l) == list for l in grid]):
			raise TypeError("The 'grid' argument must be a two-dimensional list.")

		if [len(l) for l in grid] != [9] * 9 or not sum([sum([n in range(9) for n in l]) for l in grid]):
			raise ValueError("The 'grid' argument must be a 9x9 list.")

		self.grid = [[Cell(n) for n in row] for row in grid]


	def get_grid(self) -> None:
		"""現在の盤面を取得する。

		Returns:
			現在の盤面として取得された、0-9の整数を要素に持つ、サイズ9x9の2次元リスト。
		"""
		return [[cell.value for cell in row] for row in self.grid]

	def get_row(self, i: int) -> list[int]:
		"""i行目を取得する。

		Args:
			i (int): 指定する行。0以上9未満の整数。

		Returns:
			現在の盤面のi行目として取得された、0-9の整数を要素に持つ、要素数9のリスト。

		"""
		check_index(i,"i")

		return [cell.value for cell in self.grid[i]]

	def get_column(self,j: int) -> list[int]:
		"""j列目を取得する。

		Args:
			j (int): 指定する列。0以上9未満の整数。

		Returns:
			現在の盤面のj行目として取得された、0-9の整数を要素に持つ、要素数9のリスト。

		"""
		check_index(j,"j")

		return [row[j].value for row in self.grid]

	def get_subgrid(self, index: tuple[int,int]) -> list[int]:
		"""指定された座標のマスが含まれるブロックを取得する。

		Args:
			index (tuple[int,int]): 指定するマスの行番号と列番号。0以上9未満の整数。

		Returns:
			マス(index)を含むブロックとして取得された、0-9の整数を要素に持つ、要素数9のリスト。

		"""
		i,j = index
		check_index(i,"i")
		check_index(j,"j")

		i_ = i//3 * 3
		j_ = j//3 * 3
		return [cell.value for l in self.grid[i_:i_+3] for cell in l[j_:j_+3]]

	def get_cell(self, index: tuple[int,int]) -> int:
		"""i列目のj列目を取得する。

		Args:
			index (tuple[int,int]): 指定するマスの行番号と列番号。0以上9未満の整数。

		Returns:
			0以上9以下の整数。

		"""
		i,j = index
		check_index(i,"i")
		check_index(j,"j")

		return self.grid[i][j].value

	def check_duplicate(self) -> list[tuple[int,...]]:
		"""盤面にルール違反があるかを調べる。

		Returns:
			ルールに違反しているマスの座標(タプル)のリスト。例:
				違反がない場合: []
				(0,0)と(1,1)と(0,2)が重複している場合: [(0,0),(0,2),(1,1)]

		"""
		duplicates = []

		for i,j in itertools.product(range(9), range(9)):
			value = self.grid[i][j].value

			if value != 0 and (self.get_row(i).count(value) > 1 or self.get_column(j).count(value) > 1 or self.get_subgrid((i,j)).count(value) > 1):
				duplicates.append((i,j))

		return duplicates


	def edit_number(self, index:tuple[int,int], n:int) -> None:
		"""指定されたマスに指定された数字を追加/変更/削除する。

		Args:
			index (tuple[int,int]): 指定するマスの行番号と列番号。0以上9未満の整数。
			n (int): 指定されたマスに入れる数字。0以上9以下の整数。0の場合は削除する。

		"""
		i,j = index
		check_index(i,"i")
		check_index(j,"j")

		self.grid[i][j].value = n

if __name__=="__main__":
	input_list = [[0, 1, 8, 0, 0, 0, 3, 2, 0],
                 [2, 5, 0, 0, 0, 0, 0, 4, 6],
                 [0, 0, 4, 6, 5, 2, 1, 0, 0],
                 [0, 0, 6, 0, 7, 0, 2, 0, 0],
                 [0, 2, 0, 0, 4, 0, 0, 5, 0],
                 [0, 0, 3, 1, 0, 8, 7, 0, 0],
                 [0, 0, 2, 5, 3, 9, 4, 0, 0],
                 [4, 9, 0, 0, 0, 0, 0, 8, 3],
                 [0, 7, 0, 0, 0, 0, 0, 9, 0]]
                          
 
	quiz_grid = Grid(input_list)
	quiz_grid.edit_number((0,8),1)
	print(quiz_grid.get_grid())
	print(quiz_grid.check_duplicate())

