import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["music_db"]
collection = db["musician"]

def create_musician():
    musician_id = input("Enter the musician's ID: ")
    name = input("Enter the musician's name: ")
    instrument = input("Enter the musician's instrument: ")
    genre = input("Enter the musician's genre: ")
    address = input("Enter the musician's address: ")

    musician = {
        "_id": int(musician_id), 
        "name": name,
        "instrument": instrument,
        "genre": genre,
        "address": address
    }

    result = collection.insert_one(musician)
    print("Musician added with ID:", result.inserted_id)

def find_musician():
    musician_id = input("Enter the ID of the musician to find: ")
    query = {"_id": int(musician_id)}  

    musician = collection.find_one(query)

    if musician:
        print("Musician found:")
        print("ID:", musician["_id"])
        print("Name:", musician["name"])
        print("Instrument:", musician["instrument"])
        print("Genre:", musician["genre"])
        print("Address:", musician["address"])
    else:
        print("Musician not found.")

def update_musician():
    musician_id = input("Enter the ID of the musician to update: ")
    query = {"_id": int(musician_id)}  # Convert input to an integer

    musician = collection.find_one(query)

    if musician:
        new_name = input("Enter the new name: ")
        new_instrument = input("Enter the new instrument: ")
        new_genre = input("Enter the new genre: ")
        new_address = input("Enter the new address: ")

        update_data = {
            "$set": {
                "name": new_name,
                "instrument": new_instrument,
                "genre": new_genre,
                "address": new_address
            }
        }

        collection.update_one(query, update_data)
        print("Musician updated successfully.")
    else:
        print("Musician not found.")

def delete_musician():
    musician_id = input("Enter the ID of the musician to delete: ")
    query = {"_id": int(musician_id)}  

    musician = collection.find_one(query)

    if musician:
        collection.delete_one(query)
        print("Musician deleted successfully.")
    else:
        print("Musician not found.")

while True:
    print("\nMenu:")
    print("1. Create Musician")
    print("2. Find Musician")
    print("3. Update Musician")
    print("4. Delete Musician")
    print("5. Exit")

    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
        create_musician()
    elif choice == "2":
        find_musician()
    elif choice == "3":
        update_musician()
    elif choice == "4":
        delete_musician()
    elif choice == "5":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")