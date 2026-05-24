print("Nhap cac dong (nhap 'done' de ket thuc): ")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
print("Cac dong da nhap: ")

for line in lines:
    print(line.upper())