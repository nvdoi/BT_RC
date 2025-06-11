import re
from collections import Counter

def chuan_hoa_ten(s):
    return ' '.join(word.capitalize() for word in s.split())

def dao_nguoc_tu(s):
    return ' '.join(s.split()[::-1])

def ky_tu_xuat_hien_nhieu_nhat(s):
    s = s.replace(" ", "")
    counter = Counter(s)
    ky_tu, so_lan = counter.most_common(1)[0]
    return ky_tu, so_lan

def dem_tan_suat_ky_tu(s):
    return dict(Counter(s))

def tach_so_tu_chuoi(s):
    so = re.findall(r'\d+', s)
    return [int(i) for i in so] if so else []

def cat_ho_ten(full_name):
    parts = full_name.strip().split()
    ho_lot = ' '.join(parts[:-1])
    ten = parts[-1]
    return ho_lot, ten

def viet_hoa_dau_tu(s):
    return s.title()

def chu_xen_ke(s):
    result = ''
    for i, c in enumerate(s):
        result += c.upper() if i % 2 == 0 else c.lower()
    return result

def la_doi_xung(s):
    return s == s[::-1]

def doc_so_ba_chu_so(n):
    hang_tram = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    hang_chuc = ["", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
    hang_don_vi = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

    if not (100 <= n <= 999):
        return "Số không hợp lệ"

    tram = n // 100
    chuc = (n % 100) // 10
    don_vi = n % 10

    result = f"{hang_tram[tram]} trăm"
    if chuc == 0 and don_vi != 0:
        result += f" lẻ {hang_don_vi[don_vi]}"
    else:
        result += f" {hang_chuc[chuc]}"
        if don_vi != 0:
            result += f" {hang_don_vi[don_vi]}"
    return result.strip()


def menu():
    while True:
        print("\n===== MENU =====")
        print("1. Chuẩn hóa tên (viết hoa đầu từ)")
        print("2. Đảo ngược thứ tự từ trong chuỗi")
        print("3. Ký tự xuất hiện nhiều nhất")
        print("4. Đếm số lần xuất hiện mỗi ký tự")
        print("5. Tách số khỏi chuỗi")
        print("6. Cắt họ và tên")
        print("7. Viết hoa chữ cái đầu mỗi từ")
        print("8. Chữ xen kẽ hoa thường")
        print("9. Kiểm tra chuỗi đối xứng")
        print("10. Đọc số có 3 chữ số")
        print("0. Thoát")
        lua_chon = input("Chọn chức năng (0-10): ")

        if lua_chon == '1':
            s = input("Nhập chuỗi: ")
            print("Kết quả:", chuan_hoa_ten(s))
        elif lua_chon == '2':
            s = input("Nhập chuỗi: ")
            print("Kết quả:", dao_nguoc_tu(s))
        elif lua_chon == '3':
            s = input("Nhập chuỗi: ")
            ky_tu, so_lan = ky_tu_xuat_hien_nhieu_nhat(s)
            print(f"Ký tự xuất hiện nhiều nhất: '{ky_tu}' với {so_lan} lần")
        elif lua_chon == '4':
            s = input("Nhập chuỗi: ")
            print("Tần suất ký tự:", dem_tan_suat_ky_tu(s))
        elif lua_chon == '5':
            s = input("Nhập chuỗi: ")
            print("Các số tìm thấy:", tach_so_tu_chuoi(s))
        elif lua_chon == '6':
            s = input("Nhập họ tên đầy đủ: ")
            ho_lot, ten = cat_ho_ten(s)
            print("Họ lót:", ho_lot)
            print("Tên:", ten)
        elif lua_chon == '7':
            s = input("Nhập chuỗi: ")
            print("Kết quả:", viet_hoa_dau_tu(s))
        elif lua_chon == '8':
            s = input("Nhập chuỗi: ")
            print("Kết quả:", chu_xen_ke(s))
        elif lua_chon == '9':
            s = input("Nhập chuỗi: ")
            print("Đối xứng" if la_doi_xung(s) else "Không đối xứng")
        elif lua_chon == '10':
            try:
                n = int(input("Nhập số có 3 chữ số: "))
                print("Đọc:", doc_so_ba_chu_so(n))
            except ValueError:
                print("Vui lòng nhập số nguyên hợp lệ.")
        elif lua_chon == '0':
            print("Kết thúc chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

menu()
