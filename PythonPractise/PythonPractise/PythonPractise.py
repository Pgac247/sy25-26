def flag():
    for i in range(3):
        print("**********====================")
    for i in range(3):
        print("==============================")
    
print("Helo")
name = input("what is your name?")
age = int(input("what is your age?"))
if age >= 18:
    print(name + ", you can vote")
    flag()
else:
    print(name + ", you can not vote")
