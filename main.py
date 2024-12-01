import os
from getpass import getpass
import datetime

# File paths
ADMIN_FILE = "data/admins.txt"
STAFF_FILE = "data/staff.txt"
USERS_FILE = "data/users.txt"

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")

def load_users(file_path):
    if not os.path.exists(file_path):
        return {}
    users = {}
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():  # Skip empty lines
                parts = line.strip().split(",")
                if file_path == STAFF_FILE and len(parts) >= 3:
                    username, password, position = parts[:3]
                    users[username] = {"password": password, "position": position}
                elif len(parts) >= 2:  # admin and regular users
                    username, password = parts[:2]
                    users[username] = {"password": password}
    return users

def save_user(username, password, file_path, position=None):
    ensure_data_directory()  # Ensure directory exists before saving
    with open(file_path, "a") as f:
        if file_path == STAFF_FILE:
            f.write(f"{username},{password},{position}\n")
        else:  # admin and regular users
            f.write(f"{username},{password}\n")

def signup():
    print("\n=== Sign Up ===")
    print("1. Sign up as Staff")
    print("2. Sign up as Customer")
    choice = input("Enter choice (1-2): ")
    
    if choice not in ["1", "2"]:
        print("Invalid choice. Please select 1 or 2.")
        return
        
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
            
        # Check all files for existing username
        all_users = {}
        all_users.update(load_users(ADMIN_FILE))
        all_users.update(load_users(STAFF_FILE))
        all_users.update(load_users(USERS_FILE))
        
        if username in all_users:
            print("Username already exists. Please choose another.")
            continue
            
        password = getpass("Enter password: ")
        if not password:
            print("Password cannot be empty.")
            continue
            
        confirm_password = getpass("Confirm password: ")
        
        if password != confirm_password:
            print("Passwords don't match. Try again.")
            continue
        
        if choice == "1":  # Staff signup
            position = input("Enter position (chef/waiter/receptionist/housekeeper/manager): ").lower().strip()
            while position not in ["chef", "waiter", "receptionist", "housekeeper", "manager"]:
                print("Invalid position. Please enter 'chef', 'waiter', 'receptionist', 'housekeeper', or 'manager'.")
                position = input("Enter position (chef/waiter/receptionist/housekeeper/manager): ").lower().strip()
            save_user(username, password, STAFF_FILE, position)
        else:  # Customer signup
            save_user(username, password, USERS_FILE)
            
        print("Signup successful!")
        break

def login():
    print("\n=== Login ===")
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None
        
    password = getpass("Enter password: ")
    if not password:
        print("Password cannot be empty.")
        return None
    
    # Check admin file first
    admins = load_users(ADMIN_FILE)
    if username in admins:
        if admins[username]["password"] == password:
            return {"username": username, "role": "admin"}
        else:
            print("Incorrect password.")
            return None
    
    # Check staff file
    staff = load_users(STAFF_FILE)
    if username in staff:
        if staff[username]["password"] == password:
            return {"username": username, "role": "staff", "position": staff[username]["position"]}
        else:
            print("Incorrect password.")
            return None
    
    # Check regular users file
    users = load_users(USERS_FILE)
    if username in users:
        if users[username]["password"] == password:
            return {"username": username, "role": "user"}
        else:
            print("Incorrect password.")
            return None
    
    print("Username not found.")
    return None

def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. View all users")
        print("2. Make user admin")
        print("3. Delete user")
        print("4. View staff by position")
        print("5. Update staff position")
        print("6. Logout")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == "1":
            print("\nAdmins:")
            for username in load_users(ADMIN_FILE):
                print(f"Username: {username} (Admin)")
                
            print("\nStaff:")
            for username, data in load_users(STAFF_FILE).items():
                print(f"Username: {username}, Position: {data['position']}")
                
            print("\nUsers:")
            for username in load_users(USERS_FILE):
                print(f"Username: {username} (User)")
        
        elif choice == "4":
            staff = load_users(STAFF_FILE)
            positions = ["chef", "waiter", "receptionist", "housekeeper", "manager"]
            
            for position in positions:
                print(f"\n{position.title()}s:")
                for username, data in staff.items():
                    if data['position'] == position:
                        print(f"Username: {username}")
        
        elif choice == "5":
            username = input("Enter staff username to update position: ").strip()
            staff = load_users(STAFF_FILE)
            if username in staff:
                new_position = input("Enter new position (chef/waiter/receptionist/housekeeper/manager): ").lower().strip()
                if new_position in ["chef", "waiter", "receptionist", "housekeeper", "manager"]:
                    with open(STAFF_FILE, "w") as f:
                        for user, data in staff.items():
                            position = new_position if user == username else data["position"]
                            f.write(f"{user},{data['password']},{position}\n")
                    print(f"Updated {username}'s position to {new_position}.")
                else:
                    print("Invalid position.")
            else:
                print("Staff member not found.")
        
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please select 1-6.")

def main():
    ensure_data_directory()
    
    # Create admin account if it doesn't exist
    if not os.path.exists(ADMIN_FILE):
        save_user("admin", "admin123", ADMIN_FILE)
        print("Admin account created with username: admin and password: admin123")
    
    while True:
        print("\n=== Welcome ===")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            user = login()
            if user and user["role"] == "admin":
                admin_menu()
            elif user:
                print(f"Welcome {user['username']}!")
                if user["role"] == "staff":
                    print(f"You are logged in as {user['position']}")
                user_menu(user)
            
        elif choice == "2":
            signup()
            
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

def rooms():
    """Display available room types and their basic information"""
    print("\n=== Available Rooms ===")
    print("1. Tower Exclusive (₹18,000 - ₹25,000)")
    print("2. ITC ONE (Single Occupancy) (₹25,000 - ₹35,000)")
    print("3. LUXURY SUITE (₹40,000 - ₹60,000)")
    print("4. ITC ROYAL (₹30,000 - ₹50,000)")
    print("5. TOWER EXCLUSIVE (single occupancy) (₹40,000 - ₹60,000)")

def user_menu(user):
    while True:
        print("\n=== User Menu ===")
        print("1. View Rooms")
        print("2. Book a Room")
        print("3. Logout")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            rooms()
        elif choice == "2":
            book_room(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select 1-3.")
            

def book_room(user):
    rooms()
    try:
        select = int(input("select the rooms (1-5): "))
        if select not in range(1, 6):
            print("Invalid selection. Please choose a room number between 1-5.")
            return
            
        match select:
            case 1:
                print("=====~FACILITY~=====")
                print("Tower Exclusive  (₹18,000 - ₹25,000)")
                print("--Bed--: King-size  ")
                print("--View--: City/East Kolkata Wetlands ")
                print(" ~~~~~AMENITIES~~~~~ ")
                print("   1. Complimentary Wi-Fi")
                print("   2. Flat-screen TV ")
                print("   3. Minibar")
                print("   4. 24-hour room service")
                print("   6.--occupancy--: 2 adults, 2 children (below 12 years)")
            case 2:
                print("=====~FACILITY~=====")
                print("ITC ONE (Single Occupancy) (₹25,000 - ₹35,000)")
                print("--Bed--: King-size/twin  ")
                print("--View--: City/East Kolkata Wetlands ")
                print(" ~~~~~AMENITIES~~~~~ ")
                print("   1. Complimentary Wi-Fi")
                print("   2. Flat-screen TV ")
                print("   3. Minibar")
                print("   4. 24-hour room service")
                print("   6.--occupancy--: 2 adults, 1 children (below 12 years)")
            case 3:
                print("=====~FACILITY~=====")
                print("LUXURY SUITE (₹40,000 - ₹60,000)")
                print("--Bed--: King-size  ")
                print("--View--: City/East Kolkata Wetlands ")
                print(" ~~~~~AMENITIES~~~~~ ")
                print("   1. Complimentary Wi-Fi")
                print("   2. Flat-screen TV ")
                print("   3. Minibar")
                print("   4. 24-hour room service")
                print("   5. Private balcony")
                print("   6.--occupancy--: 2 adults, 2 children (below 12 years)")
            case 4:
                print("=====~FACILITY~=====")
                print("ITC ROYAL (₹30,000 - ₹50,000)")
                print("--Bed--: King-size/twin  ")
                print("--View--: City/East Kolkata Wetlands ")
                print(" ~~~~~AMENITIES~~~~~ ")
                print("   1. Complimentary Wi-Fi")
                print("   2. Flat-screen TV ")
                print("   3. Minibar")
                print("   4. 24-hour room service")
                print("   5. Kitchenette")
                print("   6.--occupancy--: 2 adults, 2 children (below 12 years)")
            case 5:
                print("=====~FACILITY~=====")
                print("TOWER EXCLUSIVE (single occupancy) (₹40,000 - ₹60,000)")
                print("--Bed--: single  ")
                print("--View--: City/East Kolkata Wetlands ")
                print(" ~~~~~AMENITIES~~~~~ ")
                print("   1. Complimentary Wi-Fi")
                print("   2. Flat-screen TV ")
                print("   3. Minibar")
                print("   4. 24-hour room service")
                print("   5.--occupancy--: 1 adult")
                
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("*****ADDITIONAL FACILITY******")
        print("!````fitness center````!")
        print("!`````spa`````!")
        print("!`````pool`````!")
        print('!`````restaurant`````!')
        print("!`````bar`````!")
        print("!`````meeting spaces`````!")
        print('!`````business centre`````!')
        print("------------------------------------------------------------")
        
        # Fill the booking and enquiries for booked room
        name = input("Enter the name of the client: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
            
        phone = input("Enter the phone number: ").strip()
        while not phone.isdigit() or len(phone) != 10:
            print("Invalid input, please enter a 10 digit number:")
            phone = input("Enter the phone number: ").strip()
        print("Valid number:", phone)
        
        # Save booking details to file with username
        ensure_data_directory()
        with open("data/bookings.txt", "a") as f:
            f.write(f"Username: {user['username']}, Room: {select}, Name: {name}, Phone: {phone}\n")
        print("Booking details saved successfully!")
        
    except ValueError:
        print("Please  enter a valid room number (1-5)")
def foods_details():
    print("available  types of food  ")
    print("1.drinks")
    print("2.vegitarian food")
    print("3.non vegitarian food")
    print("4.chainese food")
    
    print("__DISCOUNTS__")
    print("10% off on orders above ₹1000")
    print("20% off on birthday parties (min 10 people)")
    print("__DELIVERY__")
    print("Available within 5 km radius")
    print("Charges: ₹50 (min order ₹200)")
    print("__TIMING__")
    print("- Monday to Thursday: 11am - 11pm")
    print("- Friday to Sunday: 11am - 12am")
    
def foods_order():
    print("!~~~~~~~~~~~~~~~~~~~~~MANU CARD~~~~~~~~~~~~~~~~~~~~~~~!")
    foods_details()
    select=int(input("select the type of food"))
    match select:
     case 1:
         print("====BEVERAGES BRAND====")
         print(":-soft drinks-:")
         print("-coca-cola (₹150)")
         print("- Pepsi (₹120)")
         print("- Sprite (₹100)")
         print(":-----------------:")
    
         print(":-juices-:")
         print("- Fresh Orange Juice (₹200)")
         print("- Fresh Mango Juice (₹250)")
         print(":------------------:")
    
         print(" :-Tea/Coffee-:")
         print("- Nescafe Coffee (₹80)")
         print("- Tata Tea (₹60)")
         print("- Green Tea (₹50)")
         print(":-----------------:")
     case 2:
        print("====APPETIZERS====")
        print("vagitarian food")
        print("- Vegetable Samosas (₹150)")
        print("- Paneer Tikka (₹200)")
        print("- Palak Paneer (₹250)")
        print("- Vegetable Biryani (₹200)")
        print(" Veg Combo (₹500)")
        print("1.Vegetable Biryani")
        print("2.Paneer Tikka")
        print("3.Gulab Jamun")
        print(":------------------:")
     case 3:
        print("non vegiterian food")
        print("- Fish Fingers (₹350)")
        print("- Chicken Tikka Masala (₹400)")
        print("- Fish Curry (₹450)")
        print("Non-Veg Combo (₹700)")
        print("1.Chicken Tikka Masala")
        print("2.Fish Fingers")
        print("3.Ras Malai")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
     case 4:
        print(":-chainese food-:")
        print("manchurian{veg/non veg}(₹150-200/₹200-250)")
        print("chowmein{veg/non veg}(₹100-150/₹150-200)")
        print("fried rice{veg/non veg}(₹80-120/₹120-180)")
        print(" veg spring rolls(₹80-120)")
        print("1.Veg/Chicken Hakka Noodles (₹100-150)")
        print("2. Szechuan Fried Rice (₹150-200)")
        print("3. Chili Chicken (₹200-250)")
        print("4. Paneer Chilli (₹200-250)")
        print("5. Gobi Manchurian (₹150-200)")
        name = input("Enter the name of the client: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
            
        phone = input("Enter the phone number: ").strip()
        while not phone.isdigit() or len(phone) != 10:
            print("Invalid input, please enter a 10 digit number:")
            phone = input("Enter the phone number: ").strip()
        print("Valid number:", phone)
        
        # Save booking details to file with username
        ensure_data_directory()
        with open("data/food.txt", "a") as f:
            f.write(f"Username: {name['username']}, food {select}, Name: {name}, Phone: {phone}\n")
        print("your order successfully!")
def event_details():
    print("******EVENT TYPES********")
    print("1.BIRTHDAY PARTIES")
    print("2.WEDINGS EVENT")
    print("3.ANNIVERSARIES EVENT")
    print("4.HOLIDAY PARTIES (chistmas,new years etc)")
    print("5.CONFRENCE EVENT")
    
    print("**********event pricing**********")
    print(" Per-person pricing (e.g., $50-$100)")
    print("Flat-rate pricing (e.g., $1,000-$5,000)")
    print(" Package pricing (e.g., $500-$2,000)")
def event_booking():
    selection=int(input("select the you orgnized event: enter the 1-5 number  of selection "))
    event_booking()
    match selection:
        case 1:
            print("BIRTHDAY PARTIES(charge(RS-30000))")
            print("provide to birthday decoretion ( ( RS.500-RS.2,000))")
            print("catring price according to members ")
            print("ENTERTAINMENT(live music,DJ,etc)")
            print("photography provide to organization side ")
        case 2:
            print("WEDINGS EVENT(100000-700000)")
            print("PROVIDE TO FACILITY OF ORGANIZATION")
            print("unik decorations of weding")
            print("entertanment (live music,DJ,etc)")
            print(' Photography')
            print( "Catering")
            print("Banquet Halls")
            print("a beautyful decoreted garden")
        case 3:
           print("ANNIVERSARIES EVENT(100000-200000)")
           print("PROVIDE TO FACILITY OF ORGANIZATION")
           print("unik decorations of ANNIVERSARIE")
           print("entertanment (live music,DJ,etc)")
           print(' Photography')
           print( "Catering")
           print("Private Dining Rooms")
           print("a beautyful decoreted garden") 
        case 4:
           print("HOLIDAY PARTIES (chistmas,new years (50000-80000) ")
           print("PROVIDE TO FACILITY OF ORGANIZATION")
           print("unik decorations of  HOLIDAY PARTIES")
           print("entertanment (live music,DJ,etc)")
           print(' Photography')
           print( "Catering")
           print("DISCO ")
           print("a beautyful decoreted garden") 
        case 5:
           print("CONFRENCE EVENT (50000-60000)")
           print("PROVIDE TO FACILITY OF ORGANIZATION")
           print("unik decorations of CONFRENCE EVENT")
           print("Conference Rooms")
           print(' Photography')
           print( "Catering")
           name = input("Enter the name of the client: ").strip()  
           phone = input("Enter the phone number: ").strip()
           while not phone.isdigit() or len(phone) != 10:
            print("Invalid input, please enter a 10 digit number:")
            phone = input("Enter the phone number: ").strip()
            print("Valid number:", phone)
            date=input("enter the date of event")
            guests=input("enter the num of guests")
            
        
        # Save booking details to file with username
            ensure_data_directory()
            with open("data/event.txt", "a") as f:
             f.write(f"Username: {name['username']}, event {selection}, Name: {name}, Phone: {phone},date: {date},guests: { guests}\n")
           print("your order successfully!")
        
if __name__ == "__main__":
    main()