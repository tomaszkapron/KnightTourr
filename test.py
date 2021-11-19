def func(num):
    counter1 = 0
    counter1 += num if num < 4 else -num

    return counter1

print(func(6))