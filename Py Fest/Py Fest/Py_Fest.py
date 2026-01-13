print("\n---Py-Fest 2026 Stage Manager ---")
print("1. View Lineup and Total Time")
print("2. Add a new Band")
print("3. Move First Bands to End (Late Arrival)")
print("4. Remove a Band by Name")
print("5. Move Band to a specific position")
print("6.Exit")

choice = input("Enter your choice (1-6): ")

if choice == "1":
    print("\n---Current Lineup---")

elif choice == "2":
    band_name = input("Enter the name of the new band: ")
    band_time = int(input("Enter the performance time (in minutes): "))
    print(f"Added {band_name} with a performance time of {band_time} minutes.")

elif choice == "3":
    num_bands = int(input("Enter the number of bands to move to the end: "))
    print(f"Moved the first {num_bands} bands to the end of the lineup.")

elif choice == "4":
    band_name = input("Enter the name of the band to remove: ")
    print(f"Removed {band_name} from the lineup.")