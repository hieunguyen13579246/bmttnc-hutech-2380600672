def dao_nguoc_chuoi(chuoi):
    return chuoi[::-1]
input_string = input("Moi nhap chuoi can dao nguoc: ")
print("Chuoi sau khi dao nguoc:", dao_nguoc_chuoi(input_string))