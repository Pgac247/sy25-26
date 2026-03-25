import datetime
 
v1 = "my_diary.txt"
print("1.Write 2.Read 3.Clear 4.Exit")
v2 = input("select(1-4):")
v3 = open(v1, "a")
v4 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
v5 = input("Entry:")
v6 = v3.write(f"[{v4}]{v5}\n")
v3.close()
v3 = open(v1, "r")
v7 = v3.readline()

while True:
    if v2 == "1":
        v3 = open(v1, "w")
    elif v2 == "2":
        for v8 in v7:
            print(v8.strip())
    elif v2 == "3":
        v3.close()

    elif v2 == "4":
        break

