#ｘの平方根を求める
x = float(input("平方数を求める数> "))
rnew = x
diff = abs(rnew - x/rnew)

while diff > 1.0E-6:
	r1 = rnew
	r2 = x / r1
	rnew = (r1 + r2) / 2
	diff = abs(r1 - r2)
	
	print(r1, rnew, r2)
