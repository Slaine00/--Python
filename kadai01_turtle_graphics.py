from turtle import *
import math
import time

class Bird:
	# 鳥の歩幅を設定
	__STRIDE = 100
	# 鳥の肩幅（右足と左足の y 軸方向の距離）を設定
	__WIDTH = 20

	def __init__(self) -> None:

		# 自動生成される turtle オブジェクトを隠す
		ht()

		# 足を生やす
		self.f_left = Turtle()
		self.f_right = Turtle()
		self.feet = [self.f_left, self.f_right]
		self.next_foot = self.f_right

		# 足跡の形のデータを "foot" という名称で登録
		foot__step = ((8,0), (0,10), (8,0), (8,20),(8,0), (16,10))
		getscreen().register_shape("foot", foot__step)

		# 足の形を設定し、ペンを上げ、スピードを設定
		for foot in self.feet:
			foot.ht()
			foot.up()
			foot.shape("foot")
			foot.color("black")
			foot.speed(1)

		self.f_left.goto(-self.__STRIDE/4, self.__WIDTH/2)
		self.f_right.goto(self.__STRIDE/4, -self.__WIDTH/2)

	# 現在位置を返す
	@property
	def position(self) -> tuple:
		return (self.f_left.pos() + self.f_right.pos()) * 0.5
	
	# 現在の角度を返す
	@property
	def heading(self):
		return self.f_left.heading()
		
	# スピードを 0 から 10 までの範囲の整数に設定。引数が与えられない場合は現在のスピードを返す
	def speed(self, speed=None):
		if speed==None:
			return self.f_left.speed()
		
		for foot in self.feet:
			foot.speed(speed)
			
			
	# foot (left/right/both, デフォルトでは both) の足跡の色を color (Tk 準拠) に変更
	def color(self,color,foot="both"):
		if foot == "left":
			self.f_left.color(color)
		elif foot == "right":
			self.f_right.color(color)
		elif foot == "both":
			for foot in self.feet:
				foot.color(color)
		else:
			raise ValueError('引数 foot の値は left/right/bothのいずれかである必要があります')

	
	# 一歩だけ進む: 次の足を変更し、現在位置に足跡を打つ
	def __step(self):
		self.next_foot = self.feet[self.feet.index(self.next_foot)-1]
		self.next_foot.stamp()

	# 指定された歩数だけ歩く。
	def forward(self,steps):
		for _ in range(steps):
			self.__step()
			self.next_foot.forward(self.__STRIDE)
			
	# 中心角 angle 、半径 radius (デフォルトでは __STRIDE) の弧に沿って歩く
	def turn(self, angle, radius=None):
		if radius==None:
			radius = self.__STRIDE

		indicator = 1
		# 次の足が右なら符号を反転
		if self.next_foot == self.f_right:
			indicator *= -1
			
		# 右に曲がる場合の処理
		# r の符号を反転し、 angle の範囲を 0 から 180 までに収める
		if angle%360 > 180:
			angle = angle%360 - 180
			radius *= -1
			
		# 何歩で歩くかの決定
		steps = angle//30 * (radius//self.__STRIDE) *2 -1

		# 移動距離が短すぎる場合は2歩で移動
		if steps<3:
			self.__step()
			self.next_foot.forward(self.__STRIDE/2)
			self.next_foot.circle(radius + indicator*self.__WIDTH/2, angle)
			self.__step()
			self.next_foot.circle(radius + indicator*self.__WIDTH/2, angle)
			self.next_foot.forward(self.__STRIDE/2)
			return
		
		# 初めの足を移動
		self.__step()
		self.next_foot.forward(self.__STRIDE/2)
		self.next_foot.circle(radius + indicator*self.__WIDTH/2, angle/(steps-1))
		
		# 足の踏み換えに伴って円の半径を微調整
		indicator *= -1

		for i in range(steps-2):
			self.__step()
			self.next_foot.circle(radius + indicator*self.__WIDTH/2, angle/(steps-1)*2)
			indicator *= -1

		# 初めの足と同じ足を移動
		self.__step()
		self.next_foot.circle(radius + indicator*self.__WIDTH/2, angle/(steps-1))
		self.next_foot.forward(self.__STRIDE/2)
		

	#方向転換、足跡は付けない
	def left(self, angle):
		# 両足間の距離
		feet_distance = math.sqrt(self.__WIDTH ** 2 + (self.__STRIDE/2) ** 2)
		# 両足の向きに平行な直線と両足を結ぶ直線とがなす角
		feet_angle = (90 + self.f_left.towards(self.f_right) - self.f_left.heading())%360
		# 移動時間の関係上、 feet_angle は-180から180の間に収める
		if feet_angle > 180:
			feet_angle -= 360


		# 両足の向きが、両足を結ぶ直線に対して直角になるように回転　...1
		self.f_left.left(feet_angle)
		self.f_right.left(feet_angle)
		# 両足を結ぶ線分を直径とする円の円周に沿って、中心角 angle の分の弧だけ移動
		self.f_left.circle(-feet_distance/2, -angle)
		self.f_right.circle(feet_distance/2, angle)
		# 1 で回転させた分を戻す
		self.f_left.left(-feet_angle)
		self.f_right.left(-feet_angle)
			
	# 今の位置に足跡をつけてから移動、足跡は付けない
	def flyto(self, x,y=None):
		dest = Vec2D(x,y)
		d = dest - self.position
		
		for _ in range(len(self.feet)):
			self.__step()
			self.next_foot.goto(self.next_foot.pos() + d)
			
	# 鳥の向きを to_angle に設定
	def setheading(self, to_angle):
		d = to_angle - self.heading
		self.left(d)

# デモ
bird = Bird()
time.sleep(10)
bird.forward(2)

bird.turn(120,150)


bird.speed(4)
bird.color("red",foot="both")

bird.flyto(0,0)
bird.setheading(-30)
bird.forward(4)
bird.left(-90)

bird.forward(6)

print(f"bird.position={bird.position}")
print(f"bird.heading={bird.heading}")


done()
