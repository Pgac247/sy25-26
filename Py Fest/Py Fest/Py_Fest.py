print("\n---Py-Fest 2026 Stage Manager ---")
print("1. View Lineup and Total Time")
print("2. Add a new Band")
print("3. Move First Bands to End (Late Arrival)")
print("4. Remove a Band by Name")
print("5. Move Band to a specific position")
print("6.Exit")

lineup = [ 
    ("name": "band_name", "time": 45),
    ("name": "band_name", "time": 30),
    ("name": "band_name", "time": 40),
    ("name": "band_name", "time": 25),
    ("name": "band_name", "time": 35)
]

while True:
    
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        print("\n---Current Lineup---")
        print(lineup)

    elif choice == "2":
        band_name = input("Enter the name of the new band: ")
        band_time = int(input("Enter the performance time (in minutes): "))
        print(f"Added {band_name} with a performance time of {band_time} minutes.")

    elif choice == "3":
        bands_name = int(input("Enter the name of bands to move to the end: "))
        print(f"Moved the first {bands_name} bands to the end of the lineup.")

    elif choice == "4":
        band_name = input("Enter the name of the band to remove: ")
        print(f"Removed {band_name} from the lineup.")


