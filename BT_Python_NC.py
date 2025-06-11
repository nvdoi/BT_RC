import math
import time

# B1: Tìm số chia hết cho 3 và không là số chính phương
def la_so_nguyen(n):
    try:
        int(n)
        return True
    except:
        return False

def la_so_chinh_phuong(n):
    can = int(math.sqrt(n))
    return can * can == n

def tim_cac_so_chia_het_cho_3_khong_phai_chinh_phuong(a, b):
    ket_qua = []
    for i in range(a, b + 1):
        if i % 3 == 0 and not la_so_chinh_phuong(i):
            ket_qua.append(str(i))
    return ", ".join(ket_qua)

def chuong_trinh_1():
    print("Bài 1: Tìm các số chia hết cho 3 nhưng không phải số chính phương")
    while True:
        a = input("Nhập số nguyên a: ")
        b = input("Nhập số nguyên b: ")

        if not (la_so_nguyen(a) and la_so_nguyen(b)):
            print("Vui lòng nhập đúng định dạng số nguyên.")
            continue

        a = int(a)
        b = int(b)

        if a >= b:
            print("a phải nhỏ hơn b. Hãy nhập lại.")
            continue

        break

    ket_qua = tim_cac_so_chia_het_cho_3_khong_phai_chinh_phuong(a, b)
    print("Các số thỏa điều kiện là:")
    print(ket_qua)



# B2: Game đoán số

def tao_so_ngau_nhien():
    millis = int(round(time.time() * 1000))
    return (millis % 999) + 1

def chuong_trinh_2():
    print("Bài 2: Trò chơi đoán số (1 đến 999)")
    so_can_doan = tao_so_ngau_nhien()
    so_lan_sai = 0

    while True:
        nhap = input("Nhập số bạn đoán: ")

        if not la_so_nguyen(nhap):
            print("Vui lòng nhập một số nguyên.")
            continue

        doan = int(nhap)
        if doan < 1 or doan > 999:
            print("Số bạn đoán phải nằm trong khoảng từ 1 đến 999.")
            continue

        if doan == so_can_doan:
            print(f"Chúc mừng! Bạn đã đoán đúng số {so_can_doan}.")
            break
        else:
            so_lan_sai += 1
            if abs(doan - so_can_doan) <= 10:
                print("Bạn đoán gần đúng rồi.")
            else:
                print(f"Bạn đã đoán sai {so_lan_sai} lần.")

            if so_lan_sai == 5:
                print("Bạn đã đoán sai 5 lần. Kết quả sẽ được đổi.")
                so_can_doan = tao_so_ngau_nhien()
                so_lan_sai = 0


def menu():
    while True:
        print("\nChọn chức năng:")
        print("1. Bài 1: Tìm số chia hết cho 3 không phải số chính phương")
        print("2. Bài 2: Mini game đoán số")
        print("0. Thoát")

        chon = input("Nhập lựa chọn của bạn: ")

        if chon == "1":
            chuong_trinh_1()
        elif chon == "2":
            chuong_trinh_2()
        elif chon == "0":
            print("Kết thúc chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


menu()
