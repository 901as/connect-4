def lucas_lehmer(p):
    s = 4
    m = 2 ** p-1
    for _ in range(p-2):
        s = ((s*s) - 2)%m
    return s == 0

def is_prime(num):
    if num%2 == 0:
        return num == 2
    i = 3
    while i * i <= num:
        if num % i == 0:
            return False
        i += 2
    return True

print(3)

for i in range(3, 5000, 2):
    if is_prime(i) and lucas_lehmer(i):
        print(i)
        print((2**i) - 1)

