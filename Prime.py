import random
import BaseFunc as bf
ATTEMPTS = 23 # Set number of trials here
#----------------------------------Kiểm tra số nguyên tố theo Miller- Rabin ----------------------------------------

# d là số lẻ sao cho n-1 = 2^r * d với r >= 1
def millerTest(d, n):
    # Chọn ngẫu nhiên 1 số a thuộc [2, n-2]
    a = 2 + random.randint(1, n - 4)

    # Tính x = a^d % n
    x = bf.modexp(a, d, n)
    if (x == 1 or x == n - 1):
        return True

    # Bình phương x nếu 1 trong các điều sau đây không xảy ra
    # (i) d không đạt đến n-1
    # (ii) (x^2) % n != 1
    # (iii) (x^2) % n != n-1
    while (d != n - 1):
        x = (x * x) % n
        d *= 2
        if (x == 1):
            return False
        if (x == n - 1):
            return True
    return False

# Hàm kiểm tra tính nguyên tố của n với độ chính xác là attempts lần liên tiếp pass millerTest
# attempts càng cao thì độ chính xác càng lớn
def isPrime(n, attempts):
    # Các trường hợp cơ sở cho n < 3
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True
    # Tìm số lẻ d thỏa mãn n-1 = 2^r * d
    d = n - 1
    while (d % 2 == 0):
        d //= 2
    # Thực hiện MillerTest attempts lần
    for i in range(attempts):
        if (millerTest(d, n) == False):
            return False
    return True

#-------------------------------Tạo số nguyên tố dựa trên kiểm tra tính nguyên tố của Miller-Rabin---------------------

# Dãy nguyên tố [2, 349]
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
# 1 số p bất kỳ độ dài n bits
def nBitRandom(n):
    # Returns a random number
    # between 2**(n-1)+1 and 2**n-1'''
    return (random.randrange(2 ** (n - 1) + 1, 2 ** n - 1))

#Kiểm tra p có chia hết cho bất kỳ số nguyên tố nào thuộc dãy trên không, nếu có thì p không phải là số nguyên tố
def getLowLevelPrime(n):

    while True:
        # Tạo một số ngẫu nhiên n bit
        pc = nBitRandom(n)
        # kiểm tra tính nguyên tố bằng low level primality test
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor ** 2 <= pc:
               break
        else:
            return pc

# 3. Nếu qua hết low level primality test
# Thực hiện kiểm tra tính nguyên tố bằng thuật toán Rabin Miller
# Nếu qua hết các test trong miller rabin, có thể kết luận p là số nguyên tố
def isMillerRabinPassed(mrc, attempts):
    #mrc: miller_rabin_candidate
    '''Run attempts iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert (2 ** maxDivisionsByTwo * ec == mrc - 1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    # Thực hiện attempts lần test
    numberOfRabinTrials = attempts
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True




# Hàm sinh số nguyên tố độ dài n bits, độ chính xác là vượt qua attemps test liên tiếp
def generatePrime(n, attempts):
    while True:
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate, attempts):
            continue
        else:
            return prime_candidate
