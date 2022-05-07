import random
import ElGamal
import Prime
import TextProcessing
import BaseFunc as bf
from tkinter import *
from tkinter import ttk, messagebox



window = Tk()
window.title('Elgamal')
window.geometry('1200x680')
window.iconbitmap('icon.ico')
window.resizable(height = None, width = None)


# Tạo 2 tab
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Mã hóa ')
tab_control.add(tab2, text='Chữ ký')

#---------------------------Giao diện mã hóa---------------------------------

# title1 = Label(tab1, text='Mã hóa', font=('TkDefaultFont', 20))
# title1.place(x=500, y=10)

public_key_label1 = Label(tab1, text='Khóa công khai K\'',font=('TkDefaultFont', 10))
public_key_label1.place(x=10, y=25)

# số bit của p
bitNum_label1 = Label(tab1, text='Số bit của p')
bitNum_label1.place(x=25, y=65)

# các lựa chọn cho số bit của p
option1 = [100, 500, 1000]
bitNum_value1 = IntVar()
bitNum_value1.set(option1[0])
bitNum_option1 = OptionMenu(tab1, bitNum_value1, *option1)
bitNum_option1.place(x=100, y=60)

# p
p_label1 = Label(tab1, text='p = ')
p_label1.place(x=25, y=125)

p_text1 = Text(tab1, width=52, height=6)
p_text1.place(x=80, y=95)

# alpha
alpha_label1 = Label(tab1, text='alpha = ')
alpha_label1.place(x=25, y=255)

alpha_text1 = Text(tab1, width=52, height=6)
alpha_text1.place(x=80, y=215)

# beta
beta_label1 = Label(tab1, text='beta = ')
beta_label1.place(x=25, y=390)

beta_text1 = Text(tab1, width=52, height=6)
beta_text1.place(x=80, y=335)

# Khóa bí mật
private_key_label1 = Label(tab1, text='Khóa bí mật K\'\'',font=('TkDefaultFont', 10))
private_key_label1.place(x=10, y=440)
# a
a_label1 = Label(tab1, text='a = ')
a_label1.place(x=25, y=510)

a_text1 = Text(tab1, width=52, height=6)
a_text1.place(x=80, y=470)



# tạo khóa
def keys_generate1():
    # xóa khóa cũ
    cipher_message_text1.delete('1.0', END)
    p_text1.delete('1.0', END)
    alpha_text1.delete('1.0', END)
    a_text1.delete('1.0', END)
    beta_text1.delete('1.0', END)

    # tạo khóa mới
    p1 = Prime.generatePrime(bitNum_value1.get(), Prime.ATTEMPTS)
    p_text1.insert(END, p1)
    alpha1 = bf.primitive_root(p1)
    alpha_text1.insert(END, alpha1)
    a1 = random.randint(1, (p1 - 1) // 2)
    a_text1.insert(END, a1)
    beta1 = bf.modexp(alpha1, a1, p1)
    beta_text1.insert(END, beta1)


keys_generate_button1 = Button(tab1, text='Tạo khóa\nngẫu nhiên', bg='white', fg='black', command=keys_generate1)
keys_generate_button1.place(x=180, y=598)


# kiểm tra khóa đã thỏa mãn điều kiện hay chưa
def keys_check1():
    # lấy khóa
    p1 = int(p_text1.get('1.0', "end-1c"))
    alpha1 = int(alpha_text1.get('1.0', "end-1c"))
    a1 = int(a_text1.get('1.0', 'end-1c'))
    beta1 = beta_text1.get('1.0', 'end-1c')

    if beta1:
        beta1 = int(beta1)
        # kiểm tra khóa
        if Prime.isPrime(p1, Prime.ATTEMPTS) == False:
            messagebox.showerror("Error", "p phải là số nguyên tố!!")
        elif bf.check_primitive_root(alpha1, p1) == False:
            messagebox.showerror("Error", "alpha phải là thành phần nguyên thủy của theo mod p!")
        elif a1 < 1 or a1 > (p1 - 2):
            messagebox.showerror("Error", "a phải nằm trong khoảng [1, p-2]!")
        elif beta1 != bf.modexp(alpha1, a1, p1):
            messagebox.showerror("Error", "beta phải bằng alpha ^ a mod p!")
        else:
            messagebox.showinfo('Correct', "Khóa hợp lệ")
    else:
        if Prime.isPrime(p1, Prime.ATTEMPTS) == False:
            messagebox.showerror("Error", "p phải là số nguyên tố!")
        elif bf.check_primitive_root(alpha1, p1) == False:
            messagebox.showerror("Error", "alpha phải là thành phần nguyên thủy của p!")
        elif a1 < 1 or a1 > (p1 - 2):
            messagebox.showerror("Error", "a phải có giá trị nằm trong khoảng [1, p-2]!")
        else:
            beta1 = bf.modexp(alpha1, a1, p1)
            beta_text1.insert(END, beta1)
            messagebox.showinfo('Correct', "Khóa hợp lệ")


keys_check_button1 = Button(tab1,text='Kiểm tra  \n khóa', bg='white', fg='black', command=keys_check1)
keys_check_button1.place(x=280, y=600)

# separator
separator1 = ttk.Separator(tab1, orient='vertical')
separator1.place(x=520, y=60, relheight=0.9)

# bản tin gốc
original_message_label1 = Label(tab1, text='Bản tin')
original_message_label1.place(x=530, y=120)

original_message_text1 = Text(tab1, width=65, height=6)
original_message_text1.place(x=600, y=95)


# mã hóa bản tin gốc
def encrypt1():
    # xóa văn bản mã hóa cũ
    cipher_message_text1.delete('1.0', END)
    decrypt_message_text1.delete('1.0', END)

    # lấy khóa
    p1 = int(p_text1.get('1.0', "end-1c"))
    alpha1 = int(alpha_text1.get('1.0', "end-1c"))
    # x = int(a_text.get('1.0', "end-1c"))
    beta1 = int(beta_text1.get('1.0', 'end-1c'))

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
encrypt_button1.place(x=810, y=210)

# bản tin mã hóa
cipher_message_label1 = Label(tab1, text='Bản mã')
cipher_message_label1.place(x=530, y=320)

cipher_message_text1 = Text(tab1, width=65, height=10)
cipher_message_text1.place(x=600, y=250)


# giải mã bản tin
def decrypt1():
    # xóa bản tin giải mã
    decrypt_message_text1.delete('1.0', END)

    # lấy khóa
    p1 = int(p_text1.get('1.0', "end-1c"))
    alpha1 = int(alpha_text1.get('1.0', "end-1c"))
    a1 = int(a_text1.get('1.0', "end-1c"))
    beta1 = int(beta_text1.get('1.0', 'end-1c'))
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
decrypt_message_label1 = Label(tab1, text='Bản tin')
decrypt_message_label1.place(x=530, y=500)

decrypt_message_text1 = Text(tab1, width=65, height=6)
decrypt_message_text1.place(x=600, y=470)
tab_control.pack(expand=1, fill='both')

#---------------------------Giao diện chữ ký---------------------------------
# # title UI
# title = Label(tab2, text='Chữ ký', font=('TkDefaultFont', 20))
# title.place(x=500, y=10)

# keys UI
key_label = Label(tab2, text='Khóa công khai K\'\'', font=('TkDefaultFont', 10))
key_label.place(x=10, y=25)

# số bit của p
bitNum_label = Label(tab2, text='Số bit của p')
bitNum_label.place(x=25, y=65)

# các lựa chọn cho số bit của p
option = [100, 500, 1000]
bitNum_value = IntVar()
bitNum_value.set(option[0])
bitNum_option = OptionMenu(tab2, bitNum_value, *option)
bitNum_option.place(x=100, y=60)

# p
p_label = Label(tab2, text='p = ')
p_label.place(x=25, y=125)

p_text = Text(tab2, width=52, height=6)
p_text.place(x=80, y=95)

# alpha
alpha_label = Label(tab2, text='alpha = ')
alpha_label.place(x=25, y=255)

alpha_text = Text(tab2, width=52, height=6)
alpha_text.place(x=80, y=215)

# beta
beta_label = Label(tab2, text='beta = ')
beta_label.place(x=25, y=390)

beta_text = Text(tab2, width=52, height=6)
beta_text.place(x=80, y=335)

# Khóa bí mật
private_key_label = Label(tab2, text='Khóa bí mật K\'',font=('TkDefaultFont', 10))
private_key_label.place(x=10, y=440)
# a
a_label = Label(tab2, text='a = ')
a_label.place(x=25, y=510)

a_text = Text(tab2, width=52, height=6)
a_text.place(x=80, y=470)



# tạo khóa
def keys_generate():
    # xóa khóa cũ
    cipher_message_text.delete('1.0', END)
    p_text.delete('1.0', END)
    alpha_text.delete('1.0', END)
    a_text.delete('1.0', END)
    beta_text.delete('1.0', END)

    # tạo khóa mới
    p = Prime.generatePrime(bitNum_value.get(), Prime.ATTEMPTS)
    p_text.insert(END, p)
    alpha = bf.primitive_root(p)
    alpha_text.insert(END, alpha)
    a = random.randint(1, (p - 1) // 2)
    a_text.insert(END, a)
    beta = bf.modexp(alpha, a, p)
    beta_text.insert(END, beta)


keys_generate_button = Button(tab2,text='Tạo khóa\nngẫu nhiên', bg='white', fg='black', command=keys_generate)
keys_generate_button.place(x=180, y=598)


# kiểm tra khóa đã thỏa mãn điều kiện hay chưa
def keys_check():
    # lấy khóa
    p = int(p_text.get('1.0', "end-1c"))
    alpha = int(alpha_text.get('1.0', "end-1c"))
    a = int(a_text.get('1.0', 'end-1c'))
    beta = beta_text.get('1.0', 'end-1c')


    if beta:
        beta = int(beta)
        # kiểm tra khóa
        if Prime.isPrime(p, Prime.ATTEMPTS) == False:
            messagebox.showerror("Error", "p phải là số nguyên tố")
        elif bf.check_primitive_root(alpha, p) == False:
            messagebox.showerror("Error", "alpha phải là thành phần nguyên thủy của p")
        elif a < 1 or a > (p - 2):
            messagebox.showerror("Error", "a phải có giá trị nằm trong khoảng [1, p-2]")
        elif beta != bf.modexp(alpha, a, p):
            messagebox.showerror("Error", "beta phải bằng alpha ^ a mod p")
        else:
            messagebox.showinfo('Thông tin khóa', "Khóa của bạn hợp lệ")
    else:
        if Prime.isPrime(p, Prime.ATTEMPTS) == False:
            messagebox.showerror("Error", "p phải là số nguyên tố")
        elif bf.check_primitive_root(alpha, p) == False:
            messagebox.showerror("Error", "alpha phải là thành phần nguyên thủy của p")
        elif a < 1 or a > (p - 2):
            messagebox.showerror("Error", "a phải có giá trị nằm trong khoảng [1, p-2]")
        else:
            beta = bf.modexp(alpha, a, p)
            beta_text.insert(END, beta)
            messagebox.showinfo('Thông tin khóa', "Khóa của bạn hợp lệ")


keys_check_button = Button(tab2, text='Kiểm tra   \nkhóa', bg='white', fg='black', command=keys_check)
keys_check_button.place(x=280, y=600)

# separator
# separator = ttk.Separator(tab2, orient='horizontal')
# separator.place(x=500, y=320, relwidth=0.7)
#
# separator
separator = ttk.Separator(tab2, orient='vertical')
separator.place(x=520, y=40, relheight=1)

# keys UI
# signature_label = Label(tab2, text='Ký văn bản')
# signature_label.place(x=520, y=60)

# bản tin gốc
original_message_label = Label(tab2, text='Văn bản')
original_message_label.place(x=530, y=120)

original_message_text = Text(tab2, width=65, height=8)
original_message_text.place(x=600, y=95)


# ký văn bản
def encrypt():
    # xóa chữ ký cũ
    cipher_message_text.delete('1.0', END)

    # lấy khóa
    p = int(p_text.get('1.0', "end-1c"))  # Prime number
    alpha = int(alpha_text.get('1.0', "end-1c"))  # Primitive root
    a = int(a_text.get('1.0', "end-1c"))  # Random
    beta = int(beta_text.get('1.0', 'end-1c'))

    # kiểm tra khóa
    if ElGamal.check_keys(p, alpha, a, beta) == True:

        privateKey = ElGamal.PrivateKey(a)
        publicKey = ElGamal.PublicKey(p, alpha, beta)

        # lấy bản tin gốc
        message = original_message_text.get('1.0', "end-1c")

        # ký và hiển thị chữ ký
        e = ElGamal.sign_mess(message, privateKey, publicKey, TextProcessing.ALPHABET)
        signature_message = 'y: ' + ElGamal.merge_gam(e) + 'ơ: ' + ElGamal.merge_sig(e)
        cipher_message_text.insert(END, signature_message)
    else:
        messagebox.showerror("Error", "Khoá không hợp lệ")


encrypt_button = Button(tab2,text='Thực hiện ký', bg='white', fg='black', command=encrypt)
encrypt_button.place(x=810, y=275)

# bản tin
cipher_message_label = Label(tab2, text='Chữ ký')
cipher_message_label.place(x=530, y=400)

cipher_message_text = Text(tab2, width=65, height=12)
cipher_message_text.place(x=600, y=350)


# Kiểm tra chữ ký
def decrypt():
    # lấy khóa
    p = int(p_text.get('1.0', "end-1c"))
    alpha = int(alpha_text.get('1.0', "end-1c"))
    beta = int(beta_text.get('1.0', 'end-1c'))
    publicKey = ElGamal.PublicKey(p, alpha, beta)

    # kiểm tra khóa
    if ElGamal.check_publickey(p, alpha, beta) == True:
        # lấy văn bản và chữ ký
        message = original_message_text.get('1.0', "end-1c")
        signature = cipher_message_text.get('1.0', "end-1c")
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
        messagebox.showerror("Error", "Khóa  không hợp lệ!")


decrypt_button = Button(tab2,text='Chứng thực\nchữ ký', bg='white', fg='black', command=decrypt)
decrypt_button.place(x=800, y=600)
tab_control.pack(expand=2, fill='both')


#lặp vô tận để hiển thị cửa sổ
window.mainloop()