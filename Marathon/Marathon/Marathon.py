from functools import total_ordering


runner_info = ("Chris", 540, 54)
mile_split = [8.5, 8.2, 8.4]

mile_split.append(8.3)
print(mile_split)

print(runner_info[0], sum(mile_split))

total_time = 0
total_miles = 0

for split in mile_split:
    toal_miles = total_miles + 1
    total_time = total_time + split

print("total time", total_time,"total miles", total_miles)