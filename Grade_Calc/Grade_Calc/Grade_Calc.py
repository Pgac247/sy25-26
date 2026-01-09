ap =input("enter assesment percentage:")
cp=input("enter courswork percentage:")
fp=input("enter final percentage:")
print("Assesment", ap,"courswork", cp,"final", fp)")

ag = input("enter assesment grade:")
cg = input("enter courswork grade:")
fg = input("enter final grade:")

print("Your grade is ", (float(ag)*float(ap)/100) + \ (float(cg)*float(cp)/100) + (float(fg)*float(fp)/100))


tl=(ap,cp,fp)
l1=[ag,cg,fg]
t1[1]=10