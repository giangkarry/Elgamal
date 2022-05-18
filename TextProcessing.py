ALPHABET = ".,:;!?-'()[]&+=<>/*_$#@^abcdefghijklmnopqrstuvwxyzáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ 0123456789"

# Chuyển kí tự sang số tương ứng với vị trí trong bảng chữ cái
def charToInt(char, alphabet):
	return alphabet.find(char)

#chuyển từ số sang ký tự tương ứng trong bảng chữ cái
def intToChar(n, alphabet):
	n = n % len(alphabet)
	return alphabet[n]

# Đảo ngược chuỗi abc->cba
def invStr(str):
	return str[::-1]

# chuyển 1 đoạn ký tự về 1 số
# #EX: abc->num = a.len(ALPHABET)^2 + b.len(ALPHABET) + c
def textToNum(text, alphabet):
	num = 0
	base = 1
	alp = len(alphabet)
	for i in invStr(text):
		cti = charToInt(i, alphabet)
		num += cti * base
		base *= alp
	return num

# chuyển đổi 1 số về 1 đoạn ký tự
def numToText(num, alphabet):
	text = ""
	alp = len(alphabet)
	while(num > 0):
		r = num % alp
		itc = intToChar(r, alphabet)
		text += itc
		num = (num-r)//alp
	text = invStr(text)
	return text

# tìm độ dài tối đa cho 1 đoạn tin để giá trị của nó < p(bản tin thuộc Zp)
def unitLength(alphabet, p):
	alp = len(alphabet)
	result = 0
	while (p > 0):
		result += 1
		p = p // alp
	return result

# chia text thành các đoạn tin có độ dài length
def splitText(text, length):
	textLen = len(text)
	arr = []
	if (textLen < length):
		arr.append(text)
	else:
		for i in range(0, textLen, length):
			textsub = text[i:i+length]
			arr.append(textsub)
	return arr
