# khởi tạo mảng  sử dụng for 

a = [i for i in range(10)]

#co cai ngoac vuong => mang

print(a)

#dinh nghia ham

def ham_mu(number):
    return number*number

b = [ham_mu(i) for i in range(10)]

print("day la thang b: ",b)



aa  = []
for i in range(10):
    c = ham_mu(i)
    aa.append(c)

print("day la thang aa = ", aa)
