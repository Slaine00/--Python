#xの平方根を求める

x = 2

#近似値を格納する変数
rnew = x

#１ステップあたりの近似幅が一定値を下回るまで近似を続ける
while True:
    r1 = rnew
    r2 = x/r1
    rnew = (r1 + r2)/2
    print(r1, rnew, r2)
    diff = r1 - r2
    if diff < 0:
        diff = -diff
    if diff <= 1.0E-6:
        break