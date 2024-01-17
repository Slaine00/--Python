# x の平方根を求める
x = 2

rnew = x
rnew_list = [rnew]
diff_list = []

r1 = rnew
r2 = x/r1
rnew = (r1 + r2)/2
print(r1, rnew, r2)
rnew_list.append(rnew)
diff_list.append(r2 - r1)

r1 = rnew
r2 = x/r1
rnew = (r1 + r2)/2
print(r1, rnew, r2)
rnew_list.append(rnew)
diff_list.append(r2 - r1)

r1 = rnew
r2 = x/r1
rnew = (r1 + r2)/2
print(r1, rnew, r2)
rnew_list.append(rnew)
diff_list.append(r2 - r1)

r1 = rnew
r2 = x/r1
rnew = (r1 + r2)/2
print(r1, rnew, r2)
rnew_list.append(rnew)
diff_list.append(r1 - r2)

print(rnew_list)
print(diff_list)