seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
winners = ['Purdue', 'FDU', 'FAU', 'Memphis', 'Duke', 'Oral Roberts', 'UVA', 'Furman', 'Kentucky', 'Pitt', 'Kansas', 'Howard', 'Texas', 'Penn St', 'UCLA', 'UNC Asheville']

upsets = 0

for seed, team in zip(seeds, winners):
    if seed >= 10:
        print(f"Cinderella Alert: {team}")
        upsets += 1

print(f"Total number of upsets: {upsets}")