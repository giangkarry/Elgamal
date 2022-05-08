import random
import sys
import Prime
import BaseFunc as bf
import TextProcessing as text


#========================================TẠO KHÓA cho cả hệ mật và chữ ký===============================================
# Khóa bí mật
class PrivateKey:
	def __init__(self, a):
		self.a = a
	def geta(self):
		return self.a

# Khóa công khai
class PublicKey:
	def __init__(self, p, alpha, beta):
		self.p = p
		self.alpha = alpha
		self.beta = beta

	def getp(self):
		return self.p

	def getalpha(self):
		return self.alpha

	def getbeta(self):
		return self.beta

# tạo khóa công khai {p, alpha, beta} và khóa bí mật a

def generate_keys(bits):
	p = Prime.generatePrime(bits, Prime.ATTEMPTS)
	alpha = bf.primitive_root(p)
	a = random.randint(1, (p - 1))
	beta = bf.modexp(alpha, a, p)

	privateKey = PrivateKey(a)
	publicKey = PublicKey(p, alpha, beta)

	return {'privateKey': privateKey, 'publicKey': publicKey}

# Tạo khóa với p có trước
def generate_key_with_p(p):
	alpha = bf.primitive_root(p)
	a = random.randint(1, (p - 1))
	privateKey = PrivateKey(a)
	beta = bf.modexp(alpha, a, p)
	publicKey = PublicKey(p, alpha, beta)

	return {'privateKey': privateKey, 'publicKey': publicKey}

# kiểm tra khóa công khai có sẵn
def check_publickey(p, alpha, beta):
	return True if (Prime.isPrime(p, Prime.ATTEMPTS) and bf.check_primitive_root(alpha, p) and beta < p) else False

# kiểm tra khóa công khai và khóa bí mật
def check_keys(p, alpha, a, beta):
	return True if(check_publickey(p, alpha, beta) and a >=1 and a <= p-2 and beta == bf.modexp(alpha, a, p)) else False

#===========================================MÃ HÓA======================================================================
# Bản mã (y1, y2)
class CypherNum:
	def __init__(self, y1, y2):
		self.y1 = y1
		self.y2 = y2

	def gety1(self):
		return self.y1

	def gety2(self):
		return self.y2

# trả về y1
def merge_y1(CypherNum):
	y1 = ""
	for encryptUnit in CypherNum:
		y1 += str(encryptUnit.gety1())
		y1 += "\n"
	return y1
# trả về y2
def merge_y2(CypherNum):
	y2 = ""
	for encryptUnit in CypherNum:
		y2 += str(encryptUnit.gety2())
		y2 += "\n"
	return y2

# mã hóa đoạn tin có giá trị int = x
def encrypt_num(x, publicKey):
	p = publicKey.getp()
	alpha = publicKey.getalpha()
	beta = publicKey.getbeta()
	k = random.randrange(1, p - 2)
	y1 = bf.modexp(alpha, k, p)
	y2 = (x * bf.modexp(beta, k, p)) % p
	return CypherNum(y1, y2)	#int

# chia plaintext thành các đoạn có giá trị < p rồi mã hóa
def encrypt_mess(plainText, publicKey, alphabet):
	unitText = text.splitText(plainText, text.unitLength(alphabet, publicKey.getp()))
	cypherNum = []
	# mã hóa từng đoạn 
	for unit in unitText:
		# chuyển đoạn tin -> số
		x = text.textToNum(unit, alphabet)
		# mã hóa đoạn tin có giá trị int = x
		encrypt = encrypt_num(x, publicKey)
		cypherNum.append(encrypt)
	return cypherNum


#==========================================GIẢI MÃ======================================================================
# giải mã 1 cặp mã hóa
def decrypt_unit(unitCypher, privateKey, publicKey, alphabet):
	p = publicKey.getp()
	a = privateKey.geta()
	y1 = unitCypher.gety1()
	y2 = unitCypher.gety2()
	y1inv = bf.modinv(y1, p)
	decryptValue = (y2 * (bf.modexp(y1inv, a, p))) % p
	# chuyển dạng số sang text
	decryptText = text.numToText(decryptValue, alphabet)
	return decryptText

# giải mã với các cặp mã hóa cipherNum
def decrypt_mess(cypherNum, privateKey, publicKey, alphabet):
	plainText = ""
	for unit in cypherNum:
		plainText += decrypt_unit(unit, privateKey, publicKey, alphabet)
	return plainText


#========================================TẠO CHỮ KÝ=====================================================================

# Chữ ký (gamma, sigma)
class SigNum:
	def __init__(self, gam, sig):
		self.gam = gam
		self.sig = sig

	def getgam(self):
		return self.gam

	def getsig(self):
		return self.sig

#  trả về gamma
def merge_gam(SigNum):
	gam = ""
	for sigUnit in SigNum:
		gam += str(sigUnit.getgam())
		gam += "\n"
	return gam
# trả về sigma
def merge_sig(SigNum):
	sig = ""
	for sigUnit in SigNum:
		sig += str(sigUnit.getsig())
		sig += "\n"
	return sig

# Tạo chữ ký 1 đoạn tin có giá trị int = x
def sign_num(x, privateKey, publicKey, alphabet):
	p = publicKey.getp()
	alpha = publicKey.getalpha()
	a = privateKey.geta()
	# Chọn ngẫu nhiễn một số k
	while True:
		k = random.randrange(1, p - 2)  # k thuộc tập thặng dư thu gọn theo mod p-1
		if bf.gcd(p - 1, k) == 1:
			break
	# hàm băm hx = x
	hx = x
	gam = bf.modexp(alpha, k, p)
	# sig = (h(x) - a * lmd) * k ^ -1 mod(p - 1)
	inv_k = bf.modinv(k, p - 1)
	sig = ((hx - a * gam) * inv_k) % (p - 1)
	return SigNum(gam, sig)	#int

# chia message thành các đoạn có giá trị < p rồi ký
def sign_mess(message, privateKey, publicKey, alphabet):
	unitText = text.splitText(message, text.unitLength(alphabet, publicKey.getp()))
	signNum = []
	# ký từng đoạn
	for unit in unitText:
		# chuyển đoạn tin -> số
		x = text.textToNum(unit, alphabet)
		# ký đoạn tin có giá trị int = x
		sign = sign_num(x, privateKey, publicKey, alphabet)
		signNum.append(sign)
	return signNum


#=====================================CHỨNG THỰC CHỮ KÝ==============================================================

# chứng thực với các cặp chữ ký
def verify_message(SignNum, message, publicKey, alphabet):
	p = publicKey.getp()
	alpha = publicKey.getalpha()
	beta = publicKey.getbeta()
	gam = SignNum.getgam()
	sig = SignNum.getsig()
	hx = text.textToNum(message, alphabet)
	# β^γ.γ^δ  ≡ αlpha^h(x) (mod p)
	left = (bf.modexp(beta, gam, p) * bf.modexp(gam, sig, p)) % p
	right = bf.modexp(alpha, hx, p)
	return True

