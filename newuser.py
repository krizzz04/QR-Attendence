import json
import qrcode
from PIL import Image

# Function to load data from the JSON file
def load_data(filename):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []
    return data

# Function to save data to the JSON file
def save_data(filename, data):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Function to create and save a QR code for the given ID
def create_qrcode(id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qrcodes/{id}.png")

# Load existing data from the JSON file (if it exists)
data = load_data("data.json")

# Get user input for name and ID
while True:
    name = input("Enter a name (or 'exit' to quit): ")
    if name == 'exit':
        break
    id = input("Enter an ID: ")
    
    # Check if the ID is already in use
    if any(user['id'] == id for user in data):
        print("ID already exists. Try again.")
    else:
        new_user = {
            "id": id,
            "name": name
        }
        data.append(new_user)
        print(f"User {name} with ID {id} added.")
        
        # Create and save a QR code for the new user
        create_qrcode(id)

# Save the updated data back to the JSON file
save_data("data.json", data)

print("Data has been appended to 'data.json' and QR codes have been created.")
