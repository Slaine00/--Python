from turtle import *
import math

def draw(n, theta):
	for i in range(n):
		forward(100)
		left(theta)

mode = int(input("正n角形を描きたい場合は１を、正n角形に対応する星型を描きたい場合は２を入力して下さい> "))

n = int(input("n="))

if mode ==1:
	draw(n, 360/n)
	done()

if mode == 2:
	for i in range(2, n//2+1):
		print(i)
		if math.gcd(i,n) == 1:
			draw(n, 360*i/n)
			up()
			forward(200)
			down()

	done()