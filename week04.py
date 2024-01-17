def approx_PI(n):
    approxPI = 0

    for i in range(n):
        if i%2 == 0:
            approxPI += 4 / (2*i + 1)
        else:
            approxPI -= 4/(2*i + 1)

    return approxPI
    
for i in range(7):
    print(approx_PI(10**i))