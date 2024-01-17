# -*- coding: utf-8 -*-
"""数独関係の処理を行うためのモジュール。
"""

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


def check_number(n:any, name:str="") -> None:
	"""与えられた引数がマスに書き込む数字として有効か判定する。

	Args:
		n (any): 判定の対象。
		name (str) = "": 判定の対象の変数名。

	Raises:
		TypeError: n が int でない場合に発生。
		ValueError: n が0以上9以下の範囲にない場合に発生。

	"""
	if type(n) != int:
		raise TypeError(f"The argument '{name}' must be of type int.")

	if not n in range(10):
			raise ValueError(f"The argument '{name}' must be an integer in the range of 0 to 9.")



class Grid:
	"""数独の盤面を扱うためのクラス。
	"""

	def __init__(self, grid: list[list[int]]) -> None:
		"""数独の盤面を生成する。

		9x9の2次元リストを数独の盤面として生成する。数字が書かれていないマスは0として扱う。

		Args:
			grid (list[list[int]]): 0-9の整数のみを要素に持つ、サイズ9x9の、盤面に置かれた数字のリスト。

		Raises:
			TypeError: grid が2次元リストでない、または2次元配列の要素がintではない場合に発生。
			ValueError: grid のサイズが9x9でない、または要素に0-9の範囲にない整数が含まれる場合に発生。

		Note:
			初期盤面が矛盾を含んでいるケース、および解決不可能なケースは想定していない。

		"""
		if type(grid) != list or not sum([type(l) == list for l in grid]) or not sum([sum([type(n) == int for n in l]) for l in grid]):
			raise TypeError("The 'grid' argument must be a two-dimensional list containing only elements of type int.")

		if [len(l) for l in grid] != [9] * 9 or not sum([sum([n in range(9) for n in l]) for l in grid]):
			raise ValueError("The 'grid' argument must be a 9x9 list containing only digits from 0 to 9 as elements.")

		self.grid = grid


	def get_grid(self) -> None:
		"""現在の盤面を取得する。

		Returns:
			現在の盤面として取得された、0-9の整数を要素に持つ、サイズ9x9の2次元リスト。
		"""
		return self.grid

	def get_row(self, i: int) -> list[int]:
		"""i行目を取得する。

		Args:
			i (int): 指定する行。0以上9未満の整数。

		Returns:
			現在の盤面のi行目として取得された、0-9の整数を要素に持つ、要素数9のリスト。

		"""
		check_index(i,"i")

		return self.grid[i]

	def get_column(self,j: int) -> list[int]:
		"""j列目を取得する。

		Args:
			j (int): 指定する列。0以上9未満の整数。

		Returns:
			現在の盤面のj行目として取得された、0-9の整数を要素に持つ、要素数9のリスト。

		"""
		check_index(j,"j")

		return [l[j] for l in self.grid]

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
		return sum([l[j_:j_+3] for l in self.grid[i_:i_+3]], [])

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

		return self.grid[i][j]

	def check_duplicate(self) -> list[tuple[int,...]]:
		"""盤面にルール違反があるかを調べる。

		Returns:
			ルールに違反しているマスの座標(タプル)のリスト。例:
				違反がない場合: []
				(0,0)と(1,1)と(0,2)が重複している場合: [(0,0),(0,2),(1,1)]

		"""
		return [(i,j) for i, l in enumerate(self.grid)for j,n in enumerate(l) if n != 0 and (self.get_row(i).count(n) > 1 or self.get_column(j).count(n) > 1 or self.get_subgrid((i,j)).count(n) > 1)]


	def edit_number(self, index:tuple[int,int], n:int) -> None:
		"""指定されたマスに指定された数字を追加/変更/削除する。

		Args:
			index (tuple[int,int]): 指定するマスの行番号と列番号。0以上9未満の整数。
			n (int): 指定されたマスに入れる数字。0以上9以下の整数。0の場合は削除する。

		"""
		i,j = index
		check_index(i,"i")
		check_index(j,"j")
		check_number(n,"n")

		self.grid[i][j] = n
