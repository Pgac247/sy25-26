import glob

# Get all .txt files in the directory
files = glob.glob("server_dump/*.txt")  

# Initialize counters
ok_count = 0
warn_count = 0
error_count = 0

# Initialize lists to store filenames
ok_files = []
warn_files = []
error_files = []

# Read each file
for filename in files:
    with open(filename) as f:
        content = f.read()
        if "OK" in content:
            ok_count += 1
            ok_files.append(filename)
        if "WARN" in content:
            warn_count += 1
            warn_files.append(filename)
        if "ERROR" in content:
            error_count += 1
            error_files.append(filename)

# Print the counts
print("OK:", ok_count)
print("WARN:", warn_count)
print("ERROR:", error_count)

# Give user option to print file names
if input("Print files with OK? (yes/no): ").lower() == "yes":
    print("Files with OK:", ok_files)

if input("Print files with WARN? (yes/no): ").lower() == "yes":
    print("Files with WARN:", warn_files)

if input("Print files with ERROR? (yes/no): ").lower() == "yes":
    print("Files with ERROR:", error_files)