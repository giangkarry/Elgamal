import random
import ElGamal
import Prime
import TextProcessing
import BaseFunc as bf
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image


window = Tk()
window.title('Elgamal')
window.geometry('1200x680')
window.iconbitmap('icon.ico')
window.resizable(height = None, width = None)


# Tạo 2 tab
s = ttk.Style()
s.configure('TNotebook.Tab', font=('TkDefaultFont','10','bold'))
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Mã hóa ')
tab_control.add(tab2, text='Chữ ký số')

#==============================================CÁC PHẦN DÙNG CHUNG======================================================

# Giao diện khóa công khai
class PublicKey:
    def __init__(self, master):
        self.master = master
        self.public_key_label1 = Label(master, text='Khóa công khai = {p, α, β}', font=('TkDefaultFont', 10))
        self.public_key_label1.place(x=200, y=25)
        # số bit của p
        self.bitNum_label1 = Label(master, text='Số bit', font=('TkDefaultFont', 10))
        self.bitNum_label1.place(x=25, y=65)
        # các lựa chọn cho số bit của p
        self.option1 = [100, 500, 1000]
        self.bitNum_value1 = IntVar()
        self.bitNum_value1.set(self.option1[0])
        self.bitNum_option1 = OptionMenu(master, self.bitNum_value1, *self.option1)
        self.bitNum_option1.place(x=100, y=60)
        # p
        self.p_label1 = Label(master, text='p = ', font=('TkDefaultFont', 10))
        self.p_label1.place(x=25, y=130)

        self.p_text1 = Text(master, width=52, height=6)
        self.p_text1.place(x=90, y=95)

        # alpha
        self.alpha_label1 = Label(master, text='α = ', font=('TkDefaultFont', 10))
        self.alpha_label1.place(x=25, y=255)

        self.alpha_text1 = Text(master, width=52, height=6)
        self.alpha_text1.place(x=90, y=215)

        # beta
        self.beta_label1 = Label(master, text='β =\n(α^a modp)', font=('TkDefaultFont', 10))
        self.beta_label1.place(x=5, y=370)

        self.beta_text1 = Text(master, width=52, height=6)
        self.beta_text1.place(x=90, y=335)
    def getp_text1(self):
        return self.p_text1
    def getalpha_text1(self):
        return self.alpha_text1
    def getbeta_text1(self):
        return self.beta_text1
    def getbitNum_value1(self):
        return self.bitNum_value1

# Giao diện khóa bí mật
class PrivateKey:
    def __init__(self, master):
        self.master = master
        # Khóa bí mật
        self.private_key_label1 = Label(master, text='Khóa bí mật = {a}', font=('TkDefaultFont', 10))
        self.private_key_label1.place(x=200, y=445)
        # a
        self.a_label1 = Label(master, text='a = ', font=('TkDefaultFont', 10))
        self.a_label1.place(x=25, y=510)

        self.a_text1 = Text(master, width=52, height=6)
        self.a_text1.place(x=90, y=470)
    def geta_text1(self):
        return self.a_text1

# Tạo khóa
class KeyGenerate:
    def __init__(self, master, PublicKey, PrivateKey):
        self.master = master
        self.PublicKey = PublicKey
        self.PrivateKey = PrivateKey
        self.p_text1 = PublicKey.getp_text1()
        self.alpha_text1 = PublicKey.getalpha_text1()
        self.beta_text1 = PublicKey.getbeta_text1()
        self.a_text1 = PrivateKey.geta_text1()
        self.bitNum_value1 = PublicKey.getbitNum_value1()
        self.keys_generate_button1 = Button(master, text='Tạo khóa\nngẫu nhiên', bg='white', fg='black',
                                       command=self.keys_generate1)
        self.keys_generate_button1.place(x=180, y=575)

    def keys_generate1(self):
        # xóa khóa cũ
        cipher_message_text1.delete('1.0', END)
        self.p_text1.delete('1.0', END)
        self.alpha_text1.delete('1.0', END)
        self.a_text1.delete('1.0', END)
        self.beta_text1.delete('1.0', END)

        # tạo khóa mới
        p1 = Prime.generatePrime(self.bitNum_value1.get(), Prime.ATTEMPTS)
        self.p_text1.insert(END, p1)
        alpha1 = bf.primitive_root(p1)
        self.alpha_text1.insert(END, alpha1)
        a1 = random.randint(1, (p1 - 1) // 2)
        self.a_text1.insert(END, a1)
        beta1 = bf.modexp(alpha1, a1, p1)
        self.beta_text1.insert(END, beta1)

# kiểm tra khóa đã thỏa mãn điều kiện hay chưa
class KeyCheck:
    def __init__(self, master, PublicKey, PrivateKey):
        self.master = master
        self.PublicKey = PublicKey
        self.PrivateKey = PrivateKey
        self.p_text1 = PublicKey.getp_text1()
        self.alpha_text1 = PublicKey.getalpha_text1()
        self.beta_text1 = PublicKey.getbeta_text1()
        self.a_text1 = PrivateKey.geta_text1()
        self.bitNum_value1 = PublicKey.getbitNum_value1()
        self.keys_check_button1 = Button(master, text='Kiểm tra \n khóa', bg='white', fg='black', command=self.keys_check1)
        self.keys_check_button1.place(x=280, y=575)
    def keys_check1(self):
        # lấy khóa
        p1 = int(self.p_text1.get('1.0', "end-1c"))
        alpha1 = int(self.alpha_text1.get('1.0', "end-1c"))
        a1 = int(self.a_text1.get('1.0', 'end-1c'))
        beta1 = self.beta_text1.get('1.0', 'end-1c')
        if beta1:
            beta1 = int(beta1)
            # kiểm tra khóa
            if Prime.isPrime(p1, Prime.ATTEMPTS) == False:
                messagebox.showerror("Error", "p phải là số nguyên tố!!")
            elif bf.check_primitive_root(alpha1, p1) == False:
                messagebox.showerror("Error", "α phải là thành phần nguyên thủy của theo mod p!")
            elif a1 < 1 or a1 > (p1 - 2):
                messagebox.showerror("Error", "a thỏa mãn 1 ≤ a ≤ p – 2!")
            elif beta1 != bf.modexp(alpha1, a1, p1):
                messagebox.showerror("Error", "β phải bằng α ^ a mod p!")
            else:
                messagebox.showinfo('Correct', "Khóa hợp lệ")
        else:
            if Prime.isPrime(p1, Prime.ATTEMPTS) == False:
                messagebox.showerror("Error", "p phải là số nguyên tố!")
            elif bf.check_primitive_root(alpha1, p1) == False:
                messagebox.showerror("Error", "α phải là thành phần nguyên thủy của p!")
            elif a1 < 1 or a1 > (p1 - 2):
                messagebox.showerror("Error", "a thỏa mãn 1 ≤ a ≤ p – 2!")
            else:
                beta1 = bf.modexp(alpha1, a1, p1)
                self.beta_text1.insert(END, beta1)
                messagebox.showinfo('Correct', "Khóa hợp lệ")

#============================================GIAO DIỆN MÃ HÓA==========================================================

# khóa công khai
public_key_1 = PublicKey(tab1)
#khóa bí mật
private_key_1 = PrivateKey(tab1)
# tạo khóa
key_generate_1 = KeyGenerate(tab1, public_key_1, private_key_1)

# kiểm tra khóa đã thỏa mãn điều kiện hay chưa
key_check_1 = KeyCheck(tab1, public_key_1, private_key_1)

# bản tin gốc
original_message_label1 = Label(tab1, text='Bản rõ x = ', font=('TkDefaultFont', 10))
original_message_label1.place(x=540, y=120)

original_message_text1 = Text(tab1, width=65, height=6)
original_message_text1.place(x=650, y=95)


# mã hóa bản tin gốc
def encrypt1():
    # xóa văn bản mã hóa cũ
    cipher_message_text1.delete('1.0', END)
    decrypt_message_text1.delete('1.0', END)

    # lấy khóa
    p1 = int(public_key_1.getp_text1().get('1.0', "end-1c"))
    alpha1 = int(public_key_1.getalpha_text1().get('1.0', "end-1c"))
    beta1 = int(public_key_1.getbeta_text1().get('1.0', 'end-1c'))

    # kiểm tra khóa
    if ElGamal.check_publickey(p1, alpha1, beta1) == True:
        publicKey1 = ElGamal.PublicKey(p1, alpha1, beta1)

        # lấy bản tin gốc
        message1 = original_message_text1.get('1.0', "end-1c")

        # mã hóa và hiển thị bản tin mã hóa
        e1 = ElGamal.encrypt_mess(message1, publicKey1, TextProcessing.ALPHABET)
        cipher_message1 = 'y1: ' + ElGamal.merge_y1(e1) + 'y2: ' + ElGamal.merge_y2(e1)
        cipher_message_text1.insert(END, cipher_message1)
    else:
        messagebox.showerror("Error", "Khóa không hợp lệ!")


encrypt_button1 = Button(master=tab1,text='Mã hóa', bg='white', fg='black', command=encrypt1)
encrypt_button1.place(x=820, y=210)

# bản tin mã hóa
cipher_message_label1 = Label(tab1, text='Bản mã =',font=('TkDefaultFont', 10))
cipher_message_label1.place(x=530, y=320)

cipher_message_text1 = Text(tab1, width=65, height=10)
cipher_message_text1.place(x=650, y=250)


# giải mã bản tin
def decrypt1():
    # xóa bản tin giải mã
    decrypt_message_text1.delete('1.0', END)

    # lấy khóa
    p1 = int(public_key_1.getp_text1().get('1.0', "end-1c"))
    alpha1 = int(public_key_1.getalpha_text1().get('1.0', "end-1c"))
    a1 = int(private_key_1.geta_text1().get('1.0', "end-1c"))
    beta1 = int(public_key_1.getbeta_text1().get('1.0', 'end-1c'))
    privateKey1 = ElGamal.PrivateKey(a1)
    publicKey1 = ElGamal.PublicKey(p1, alpha1, beta1)

    # kiểm tra khóa
    if ElGamal.check_keys(p1, alpha1, a1, beta1) == True:
        # lấy bản tin mã hóa
        cipher_message1 = cipher_message_text1.get('1.0', "end-2c")
        y = cipher_message1.split('y2')
        y1 = y[0][4:-1]
        y2 = y[1][2:]
        y1 = y1.split('\n')
        y2 = y2.split('\n')
        cypherNums1 = []
        for i in range(len(y1)):
            unitCypherNum1 = ElGamal.CypherNum(int(y1[i]), int(y2[i]))
            cypherNums1.append(unitCypherNum1)

        # giải mã và hiển thị bản tin sau khi giải mã
        decrypt_message1 = ElGamal.decrypt_mess(cypherNums1, privateKey1, publicKey1, TextProcessing.ALPHABET)
        decrypt_message_text1.insert(END, decrypt_message1)
    else:
        messagebox.showerror("Error", "Khóa không hợp lệ")


decrypt_button1 = Button(tab1,text='Giải mã', bg='white', fg='black', command=decrypt1)
decrypt_button1.place(x=810, y=430)

# bản tin giải mã
decrypt_message_label1 = Label(tab1, text='Bản giải mã = ',font=('TkDefaultFont', 10))
decrypt_message_label1.place(x=530, y=500)

decrypt_message_text1 = Text(tab1, width=65, height=6)
decrypt_message_text1.place(x=650, y=470)
tab_control.pack(expand=1, fill='both', pady = 20)


#===============================================GIAO DIỆN CHỮ KÝ=======================================================

# khóa công khai
public_key_2 = PublicKey(tab2)
# Khóa bí mật
private_key_2 = PrivateKey(tab2)
# tạo khóa
key_generate_2 = KeyGenerate(tab2, public_key_2, private_key_2)
# kiểm tra khóa đã thỏa mãn điều kiện hay chưa
key_check_2 = KeyCheck(tab2, public_key_2, private_key_2)

# bản tin gốc
original_message_label = Label(tab2, text='Văn bản', font=('TkDefaultFont', 10))
original_message_label.place(x=530, y=120)

original_message_text = Text(tab2, width=65, height=8)
original_message_text.place(x=600, y=95)


# ký văn bản
def sign():
    # xóa chữ ký cũ
    sign_message_text.delete('1.0', END)

    # lấy khóa
    p = int(public_key_2.getp_text1().get('1.0', "end-1c"))  # Prime number
    alpha = int(public_key_2.getalpha_text1().get('1.0', "end-1c"))  # Primitive root
    a = int(private_key_2.geta_text1().get('1.0', "end-1c"))  # Random
    beta = int(public_key_2.getbeta_text1().get('1.0', 'end-1c'))

    # kiểm tra khóa
    if ElGamal.check_keys(p, alpha, a, beta) == True:

        privateKey = ElGamal.PrivateKey(a)
        publicKey = ElGamal.PublicKey(p, alpha, beta)

        # lấy bản tin gốc
        message = original_message_text.get('1.0', "end-1c")

        # ký và hiển thị chữ ký
        e = ElGamal.sign_mess(message, privateKey, publicKey, TextProcessing.ALPHABET)
        signature_message = 'y: ' + ElGamal.merge_gam(e) + 'ơ: ' + ElGamal.merge_sig(e)
        sign_message_text.insert(END, signature_message)
    else:
        messagebox.showerror("Error", "Khoá không hợp lệ")


sign_button = Button(tab2,text='Thực hiện ký', bg='white', fg='black', command=sign)
sign_button.place(x=810, y=275)

# bản tin
sign_message_label = Label(tab2, text='Chữ ký', font=('TkDefaultFont', 10))
sign_message_label.place(x=530, y=400)

sign_message_text = Text(tab2, width=65, height=12)
sign_message_text.place(x=600, y=350)


# Kiểm tra chữ ký
def verify():
    # lấy khóa
    p = int(public_key_2.getp_text1().get('1.0', "end-1c"))
    alpha = int(public_key_2.getalpha_text1().get('1.0', "end-1c"))
    beta = int(public_key_2.getbeta_text1().get('1.0', 'end-1c'))
    publicKey = ElGamal.PublicKey(p, alpha, beta)

    # kiểm tra khóa
    if ElGamal.check_publickey(p, alpha, beta) == True:
        # lấy văn bản và chữ ký
        message = original_message_text.get('1.0', "end-1c")
        signature = sign_message_text.get('1.0', "end-1c")
        print(message)
        print(signature)

        y = signature.split('ơ')
        gam = y[0][4:-1]
        sig = y[1][2:-1]
        sig_num = ElGamal.SigNum(int(gam), int(sig))

        # Xác thực chữ ký và hiển thị kết quả xác thực
        is_verified = ElGamal.verify_message(sig_num, message, publicKey, TextProcessing.ALPHABET)
        if is_verified:
            messagebox.showinfo("Chữ ký", "Chữ ký được xác thực")
        else:
            messagebox.showerror("Chữ ký", "Chữ ký không được xác thực")
    else:
        messagebox.showerror("Error", "Khóa không hợp lệ!")


verify_button = Button(tab2,text='Chứng thực\nchữ ký', bg='white', fg='black', command=verify)
verify_button.place(x=800, y=575)
tab_control.pack(expand=2, fill='both')


#lặp vô tận để hiển thị cửa sổ
window.mainloop()