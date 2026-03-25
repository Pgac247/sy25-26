file_name = input("Enter the file name: ")

file = open(file_name, "r")

word = input("Enter the word to search for:")

count = 0

line = file.readline()

while line:
    if word.upper() in line.upper():
        count += line.upper().count(word.upper())
    line = file.readline()

print(f"Serching for '{word}' in {file_name}.....")

print(f"{word} appear in the file {count} times.")