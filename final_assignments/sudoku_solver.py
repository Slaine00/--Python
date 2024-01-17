import copy
import sys
input_grid = [[0, 1, 8, 0, 0, 0, 3, 2, 0],
              [2, 5, 0, 0, 0, 0, 0, 4, 6],
              [0, 0, 4, 6, 5, 2, 1, 0, 0],
              [0, 0, 6, 0, 7, 0, 2, 0, 0],
              [0, 2, 0, 0, 4, 0, 0, 5, 0],
              [0, 0, 3, 1, 0, 8, 7, 0, 0],
              [0, 0, 2, 5, 3, 9, 4, 0, 0],
              [4, 9, 0, 0, 0, 0, 0, 8, 3],
              [0, 7, 0, 0, 0, 0, 0, 9, 0]]

def solver(l):
    l_ = copy.deepcopy(l)

    for i, k in enumerate(l_):
        for j in range(len(k)):
            if k[j] == 0:
                for n in range(1,10):
                    if is_against_rule(l,i,j,n):
                        if n == 9:
                            return
                        continue
                    k[j] = n
                    solver(l_)

    printer(l_)
    print()
    sys.exit()

# [i,j]にnを入れるとルールに違反しているかを判定する関数
def is_against_rule(l,i,j,n):
    if n in l[i]:
        return True
    if n in [k[j] for k in l]:
        return True

    i_ = i//3 * 3
    j_ = j//3 * 3
    if n in sum([k[j_:j_+3] for k in l[i_:i_+3]], []):
        return True

    else:
        return False


def printer(l):
    for i in l:
        print(i)
        
solver(input_grid)

def a(i):
    return i//3 * 3

a(4)