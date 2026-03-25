cars = [
    ["F1", "VW Off-Road-Bug", 185, (104, 142), 6000, 1980, 4],
    ["E1", "Mitsubishi Carisma GT", 225, (213, 240), 6000, 1996, 4],
    ["E3", "Skoda Octavia WRS", 230, (221, 300), 7500, 2000, 4],
    ["G2", "Seat Ibiza GTi", 220, (205, 280), 8400, 1984, 4],
    ["G3", "Mitsubishi Pajero", 185, (153, 208), 7000, 3497, 6]
]

i = 1
for car in cars:
    print(i, car[1])
    i += 1

choice = int(input("Choose a car number: "))
car = cars[choice - 1]

print(f"\nStatistics for {car[1]}:")
print(f"Max Speed: {car[2]} km/h")
print(f"Speed Range: {car[3][0]} - {car[3][1]} km/h")
print(f"Weight: {car[4]} kg")
print(f"Year: {car[5]}")
print(f"Seats: {car[6]}")

