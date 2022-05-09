# Viết chương trình mã hóa, giải mã, xây dựng và kiểm thử chữ ký trên hệ mật ElGamal với n có độ dài 100, 500 và 1000 bit

## I. BaseFunc.py
Các hàm tính toán cơ bản 
1. **gcd(a, b)** : hàm trả về ước chung lớn nhất của 2 số a và b
2. **modinv(a,b)**: Hàm trả về nghịch đảo của a theo mod b (a^-1 mod b)
3. **modexp(b, n, m)**: Hàm trả về b^n mod m
4. **primitive_root(p)**: Hàm trà về 1 phần tử nguyên thủy ngẫu nhiên của p
5. **check_primirive_root(g, p)**: Hàm trả về True nếu g là thành phần nguyên thủy của p, nếu không trả về False

## II. Prime.py
Hai chức năng chính là kiểm tra tính nguyên tố và tạo số nguyên tố dựa trên Miller-Rabin

_Tham khảo_ 

[1] https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/

[2] https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/

1. **Kiểm tra tính nguyên tố dựa trên thuật toán Miller-Rabin**
![image](https://user-images.githubusercontent.com/62466416/167335747-838f4a2e-6e8d-4652-9de8-9f3c19e51fa3.png)

2. **Tạo số nguyên tố dựa trên kiểm tra tính nguyên tố của Miller-Rabin**
![image](https://user-images.githubusercontent.com/62466416/167337200-aa9d0452-f1e6-4448-ae92-247165b68bb9.png)

## III. TextProcessing.py
![image](https://user-images.githubusercontent.com/62466416/167338836-0211e7e9-6f7d-4b0d-98bb-51975b7c4cc4.png)

## IV. Elgamal.py
1. **Tạo khóa**

    a. **generate_keys(bits)**: tạo khóa công khai {p, alpha, beta} với số nguyên tố p có bits bit

    b. **generate_key_with_p(p)**: tạo khóa với số nguyên tố p có trước-> tạo alpha, a, tính beta

    c. **check_keys(p, alpha, a, beta)**: kiểm tra khóa

      - kiểm tra p thỏa mãn tính nguyên tố
      - Kiểm tra alpha là thành phần nguyên thủy theo mod p
      - Kiểm tra beta < p
      - Kiểm tra a thuộc [1, p-2]
    
2. **Mã hóa**

    a. **encrypt_num(x, publicKey)**: mã hóa đoạn tin có giá trị int = x
    
    b. **encrypt_mess(plainText, publicKey, alphabet)**: 
    
    - chia phainText thành các đoạn có giá trị lớn nhất < p -> mã hóa từng đoạn

    - trả về bản mã hóa
 
3. **Giải mã**

    a. **decrypt_unit(unitCypher, privateKey, publicKey, alphabet)**: giải mã 1 cặp mã hóa

    b. **decrypt_mess(cypherNum, privateKey, publicKey, alphabet)**: giải mã với tất cả cặp mã hóa trả về bản giải mã
  
4. **Tạo chữ ký**

    a. **sign_num(x, privateKey, publicKey, alphabet)**: Tạo chữ ký 1 đoạn tin có giá trị int = x

    b. **sign_mess(message, privateKey, publicKey, alphabet)**

      - chia message thành các đoạn có giá trị lớn nhất < p -> ký từng đoạn

      - trả về bản chữ ký
    
5. **Chứng thực chữ ký**

    **verify_message(SignNum, message, publicKey, alphabet)**: chứng thực chữ ký

## V. UI.py
    Tạo giao diện dựa trên thư viện **tkinter** của Python

 
