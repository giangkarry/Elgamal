import random
import math


# Thuật toán Euclid tìm ước chung lớn nhất của 2 số a và b
def gcd(a, b):
		while b != 0:
			r = a % b
			a = b
			b = r
		return a

#Thuật toán Euclide mở rộng tìm nghịch đảo modulo: a^-1 mod b

def modinv(a, b):
	temp = b
	x2 = 1
	x1 = 0
	y2 = 0
	y1 = 1
	while b > 0:
		q = a // b
		r = a % b
		x = x2 - q * x1
		y = y2 - q * y1
		a = b
		b = r
		x2 = x1
		x1 = x
		y2 = y1 
		y1 = y
	return x2 if x2 >= 0 else x2 + temp

# Thuật toán lũy thừa theo modulo tính b^n mod m
def modexp(b, n, m):
	x = 1
	power = b % m
	while n > 0:
		if (n % 2 == 1):
			x = (x * power) % m
		n = n // 2
		power = (power * power) % m
	return x

#---------------------- p là số lớn 100, 500, 1000 bit------------------------------------------------------------------


# Tìm 1 phần tử nguyên thủy tính trong trường hợp p là số nguyên tố an toàn: SophieGermain
def primitive_root(p):
	if p == 2:
		return 1
	# Các ước của p-1 là 2 và (p-1)/2 bởi vì p = 2q+1 trong đó q là số nguyên tố
	p1 = 2
	p2 = (p - 1) // p1
	#Kiểm tra ngẫu nhiên cho đến khi tìm thấy 1 tử nguyên thủy theo mod p
	while True:
		g = random.randint(2, p-1)
		if (modexp(g, p1, p) != 1 and modexp(g, p2, p) != 1):
			return g

# kiểm tra xem g có phải là thành phần nguyên thủy của p không
def check_primitive_root(g, p):
	p1 = 2
	p2 = (p - 1) // p1
	return True if (modexp(g,p1, p) != 1 and modexp(g, p2, p) != 1) else False
