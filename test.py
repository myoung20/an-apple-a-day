def toBase(n):
    alph='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-'
    s=''
    while n:
        s = str(alph[int(n % 64)]) + s
        n -= n%64
        n/=64
    return s

print(toBase(13 62 39 52 59 99 41 71 75 68))