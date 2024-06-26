import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

class Customer:
    def __init__(self, name, email, phone, passport, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.passport = passport
        self.address = address

    def __str__(self):
        return f"Customer(name={self.name}, email={self.email}, phone={self.phone}, passport={self.passport}, address={self.address})"

class Trip:
    def __init__(self, destination, option, duration, price):
        self.destination = destination
        self.option = option
        self.duration = duration
        self.price = price

    def __str__(self):
        return f"Trip(destination={self.destination}, option={self.option}, duration={self.duration} days, price=${self.price})"

class Booking:
    def __init__(self,id, customer, trip):
        self.id = id
        self.customer = customer
        self.trip = trip

    def __str__(self):
        return f"Booking(Customer={self.customer.name}, Trip={self.trip.destination})"

class TravelAgencyApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("SU5 Travel Agency")

        self.customers = []
        self.trips = []
        self.bookings = []
        
        self.customer_id_map = {}
        self.trip_id_map = {}
        
        self.database_init()
        self.create_main_page()
        
    def database_init(self):
        try:
            self.mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='SUM5TA'
            )

            if self.mydb.is_connected():
                self.cursor = self.mydb.cursor()

                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    phone VARCHAR(50) NOT NULL,
                    passport VARCHAR(50) NOT NULL,
                    address TEXT NOT NULL
                )
                ''')

                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS trips (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    destination VARCHAR(255) NOT NULL,
                    option VARCHAR(255) NOT NULL,
                    duration INT NOT NULL,
                    price FLOAT NOT NULL
                )
                ''')

                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT NOT NULL,
                    trip_id INT NOT NULL,
                    status VARCHAR(50) DEFAULT 'Not Confirmed',
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (trip_id) REFERENCES trips(id)
                )
                ''')

                self.mydb.commit()
        except Error as e:
            print(f"Error: {e}")
            if self.mydb.is_connected():
                self.mydb.close()

    def create_main_page(self):
        self.main_frame = ttk.Frame(self.root, width=600, height=400)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=1, fill='both')
        self.load_image(self.main_frame)
        enter_button = ttk.Button(self.main_frame, text="Enter", command=self.create_widgets)
        enter_button.pack(pady=20)

    def load_image(self, frame):
        # Path to the image file
        image_path = "coverpage.jpg"
        try:
            # Load the image using PIL
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            # Create a label widget to display the image
            image_label = tk.Label(frame, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.pack(padx=10, pady=10)
        except IOError:
            print(f"Unable to load image at path: {image_path}")

       
        
    def create_widgets(self):
        self.main_frame.destroy()  # Remove the main frame

        # Set a fixed size for the notebook
        notebook_width = 1280
        notebook_height = 648
        
        self.tab_control = ttk.Notebook(self.root, width=notebook_width, height=notebook_height)  # Changed to self.tab_control

        self.customer_tab = ttk.Frame(self.tab_control)
        self.trip_tab = ttk.Frame(self.tab_control)
        self.booking_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.customer_tab, text='Customers')
        self.tab_control.add(self.trip_tab, text='Trips')
        self.tab_control.add(self.booking_tab, text='Bookings')

        self.tab_control.pack(expand=1, fill='both')

        self.create_customer_tab()
        self.create_trip_tab()
        self.create_booking_tab()

    def create_customer_tab(self):
                
        ttk.Label(self.customer_tab, text="Name:").grid(column=0, row=0, padx=10, pady=10)
        self.customer_name = ttk.Entry(self.customer_tab)
        self.customer_name.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.customer_tab, text="Email:").grid(column=0, row=1, padx=10, pady=10)
        self.customer_email = ttk.Entry(self.customer_tab)
        self.customer_email.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.customer_tab, text="Phone:").grid(column=0, row=2, padx=10, pady=10)
        self.customer_phone = ttk.Entry(self.customer_tab)
        self.customer_phone.grid(column=1, row=2, padx=10, pady=10)
        
        ttk.Label(self.customer_tab, text="Passport:").grid(column=0, row=3, padx=10, pady=10)
        self.customer_passport = ttk.Entry(self.customer_tab)
        self.customer_passport.grid(column=1, row=3, padx=10, pady=10)
        
        ttk.Label(self.customer_tab, text="Address:").grid(column=0, row=4, padx=10, pady=10)
        self.customer_address = ttk.Entry(self.customer_tab)
        self.customer_address.grid(column=1, row=4, padx=10, pady=10)

        ttk.Button(self.customer_tab, text="Add Customer", command=self.add_customer).grid(column=1, row=5, padx=10, pady=10)

        self.customer_list = tk.Listbox(self.customer_tab)
        self.customer_list.grid(column=0, row=6, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.customer_tab.grid_columnconfigure(0, weight=1)
        self.customer_tab.grid_columnconfigure(1, weight=1)
        self.customer_tab.grid_rowconfigure(6, weight=1)

    def create_trip_tab(self):
        ttk.Label(self.trip_tab, text="Destination:").grid(column=0, row=0, padx=10, pady=10)
        self.trip_destination = ttk.Entry(self.trip_tab)
        self.trip_destination.grid(column=1, row=0, padx=10, pady=10)
        
        ttk.Label(self.trip_tab, text="Option").grid(column=0, row=1, padx=10, pady=10)
        options = ["Select an option", "Bus Express", "Package Tours", "Cruises", "Flight Ticket", "Hotel", "Trekking"]
        self.option_var = tk.StringVar(value=options[0])
        self.trip_option = ttk.OptionMenu(self.trip_tab, self.option_var, *options)
        self.trip_option.grid(column=1, row=1, padx=10, pady=10)
        
        ttk.Label(self.trip_tab, text="Duration (days):").grid(column=0, row=3, padx=10, pady=10)
        self.trip_duration = ttk.Entry(self.trip_tab)
        self.trip_duration.grid(column=1, row=3, padx=10, pady=10)

        ttk.Label(self.trip_tab, text="Price:").grid(column=0, row=4, padx=10, pady=10)
        self.trip_price = ttk.Entry(self.trip_tab)
        self.trip_price.grid(column=1, row=4, padx=10, pady=10)

        ttk.Button(self.trip_tab, text="Add Trip", command=self.add_trip).grid(column=1, row=5, padx=10, pady=10)

        self.trip_list = tk.Listbox(self.trip_tab)
        self.trip_list.grid(column=0, row=6, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.trip_tab.grid_columnconfigure(0, weight=1)
        self.trip_tab.grid_columnconfigure(1, weight=1)
        self.trip_tab.grid_rowconfigure(6, weight=1)


    def create_booking_tab(self):
        
        self.customer_id_map = {}
        self.trip_id_map = {}
        
        #Create Customer label and combobox
        ttk.Label(self.booking_tab, text="Customer:").grid(column=0, row=0, padx=10, pady=10)
        self.booking_customer = ttk.Combobox(self.booking_tab)
        self.booking_customer.grid(column=1, row=0, padx=10, pady=10)

        #Create Trip label and combobox
        ttk.Label(self.booking_tab, text="Trip:").grid(column=0, row=1, padx=10, pady=10)
        self.booking_trip = ttk.Combobox(self.booking_tab)
        self.booking_trip.grid(column=1, row=1, padx=10, pady=10)

        #Create - Create Booking button
        ttk.Button(self.booking_tab, text="Create Booking", command=self.create_booking).grid(column=1, row=2, padx=10, pady=10)
        
        #Create Booking list
        self.booking_list = tk.Listbox(self.booking_tab)
        self.booking_list.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky='nsew')

        #Create Confirm Booking button
        ttk.Button(self.booking_tab, text="Confirm Booking", command=self.confirm_booking).grid(column=1, row=4, padx=10, pady=10)
        
        self.booking_tab.grid_columnconfigure(0, weight=1)
        self.booking_tab.grid_columnconfigure(1, weight=1)
        self.booking_tab.grid_rowconfigure(3, weight=1)
        
        #Load initial booking data
        self.load_booking_data()
        
       
    def load_booking_data(self):
        self.customer_id_map = {}  # Ensure the map is cleared and reinitialized
        self.trip_id_map = {}

        try:
            self.cursor.execute('SELECT id, name FROM customers')
            customer_rows = self.cursor.fetchall()
            customer_list = []
            
            for customer_row in customer_rows:
                customer_id, customer_name = customer_row
                combined = f"{customer_id} - {customer_name}"
                self.customer_id_map[combined] = customer_id
                customer_list.append(combined)
            self.booking_customer['values'] = customer_list
        except Exception as e:
            print(f"Error loading customers: {e}")

        try:
            self.cursor.execute('SELECT id, destination FROM trips')
            trip_rows = self.cursor.fetchall()
            trip_list = []
            for trip_row in trip_rows:
                trip_id, trip_destination = trip_row
                combined = f"{trip_id} - {trip_destination}"
                self.trip_id_map[combined] = trip_id
                trip_list.append(combined)
            self.booking_trip['values'] = trip_list
        except Exception as e:
            print(f"Error loading trips: {e}")

        self.booking_list.delete(0, tk.END)
        try:
            self.cursor.execute('''
            SELECT b.id,c.name, t.destination, b.status 
            FROM bookings b 
            JOIN customers c ON b.customer_id = c.id 
            JOIN trips t ON b.trip_id = t.id
            ORDER BY b.id
            ''')
            booking_rows = self.cursor.fetchall()
            self.bookings = [list(row) for row in booking_rows]
            for booking in self.bookings:
                booking_info = f"{booking[0]} - {booking[1]} - {booking[2]} - {booking[3]}"
                self.booking_list.insert(tk.END, booking_info)
        except Exception as e:
            print(f"Error loading bookings: {e}") 
            
        try:
            self.cursor.execute("SELECT id, name, email, phone, passport, address FROM customers")
            customer_rows = self.cursor.fetchall()
            customer_list = []
            self.customer_list.delete(0, tk.END)
            for customer_row in customer_rows:
                cust_info = f"{customer_row[0]} - {customer_row[1]} - {customer_row[2]} - {customer_row[3]} - {customer_row[4]}  - {customer_row[5]}"
                self.customer_list.insert(tk.END, cust_info)
        except Exception as e:
            print(f"Error loading customers: {e}")
        
        try:
            self.cursor.execute("SELECT id, destination, option, duration, price FROM trips")
            trip_rows = self.cursor.fetchall()
            trip_list = []
            self.trip_list.delete(0, tk.END)
            for trip_row in trip_rows:
                trip_info = f"{trip_row[0]} - {trip_row[1]} - {trip_row[2]} - {trip_row[3]} - {trip_row[4]}"
                self.trip_list.insert(tk.END, trip_info)
        except Exception as e:
            print(f"Error loading Trips: {e}")
    
    
    
    def create_booking_tab(self):
        # Create Customer label and combobox
        ttk.Label(self.booking_tab, text="Customer:").grid(column=0, row=0, padx=10, pady=10)
        self.booking_customer = ttk.Combobox(self.booking_tab)
        self.booking_customer.grid(column=1, row=0, padx=10, pady=10)

        # Create Trip label and combobox
        ttk.Label(self.booking_tab, text="Trip:").grid(column=0, row=1, padx=10, pady=10)
        self.booking_trip = ttk.Combobox(self.booking_tab)
        self.booking_trip.grid(column=1, row=1, padx=10, pady=10)

        # Create - Create Booking button
        ttk.Button(self.booking_tab, text="Create Booking", command=self.create_booking).grid(column=1, row=2, padx=10, pady=10)

        # Create Booking list
        self.booking_list = tk.Listbox(self.booking_tab)
        self.booking_list.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Create Confirm Booking button
        ttk.Button(self.booking_tab, text="Confirm Booking", command=self.confirm_booking).grid(column=1, row=4, padx=10, pady=10)

        self.booking_tab.grid_columnconfigure(0, weight=1)
        self.booking_tab.grid_columnconfigure(1, weight=1)
        self.booking_tab.grid_rowconfigure(3, weight=1)

        # Load initial booking data
        self.load_booking_data()


    def add_customer(self):
        name = self.customer_name.get()
        email = self.customer_email.get()
        phone = self.customer_phone.get()
        passport = self.customer_passport.get()
        address = self.customer_address.get()

        if not name or not email or not phone or not passport or not address:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        customer = Customer(name, email, phone, passport, address)
        self.customers.append(customer)
        self.customer_list.insert(tk.END, str(customer))

        self.cursor.execute('''
        INSERT INTO customers (name, email, phone, passport, address)
        VALUES (%s, %s, %s, %s, %s)
        ''', (name, email, phone, passport, address))
        self.mydb.commit()
        print(f"- Customer Added : {name}, {passport}.")

        self.customer_name.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)
        self.customer_passport.delete(0, tk.END)
        self.customer_address.delete(0, tk.END)

        self.load_booking_data()
        #self.refresh_booking_comboboxes()
        
        self.tab_control.select(self.trip_tab)

    def add_trip(self):
        
        destination = self.trip_destination.get()
        option = self.option_var.get()
        duration = self.trip_duration.get()
        price = self.trip_price.get()

        if not destination or option == "Select an option" or not duration or not price:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        try:
            duration = int(duration)
            price = float(price)
        except ValueError:
            messagebox.showwarning("Input Error", "Duration must be an integer and price must be a float")
            return

        trip = Trip(destination, option, duration, price)
        self.trips.append(trip)
        self.trip_list.insert(tk.END, str(trip))

        self.cursor.execute('''
        INSERT INTO trips (destination, option, duration, price)
        VALUES (%s, %s, %s, %s)
        ''', (destination, option, duration, price))
        self.mydb.commit()
        print(f"- Trip Added : {destination}, {price}.")

        self.trip_destination.delete(0, tk.END)
        self.option_var.set("Select an option")
        self.trip_duration.delete(0, tk.END)
        self.trip_price.delete(0, tk.END)
        
        self.load_booking_data()
        #self.refresh_booking_comboboxes()
        self.tab_control.select(self.booking_tab)

    
    def create_booking(self):
        customer_entry = self.booking_customer.get()
        trip_entry = self.booking_trip.get()

        if not customer_entry or not trip_entry:
            messagebox.showwarning("Input Error", "Customer and Trip must be selected")
            return

        customer_id = self.customer_id_map.get(customer_entry)
        trip_id = self.trip_id_map.get(trip_entry)

        if not customer_id or not trip_id:
            messagebox.showwarning("Input Error", "Selected customer or trip not found")
            return

        self.cursor.execute("SELECT id, name, email, phone, passport, address FROM customers WHERE id = %s", (customer_id,))
        customer_data = self.cursor.fetchone()

        if not customer_data:
            messagebox.showwarning("Input Error", "Selected customer not found")
            return

        customer = Customer(*customer_data[1:])
        customer.id = customer_data[0]

        self.cursor.execute("SELECT id, destination, option, duration, price FROM trips WHERE id = %s", (trip_id,))
        trip_data = self.cursor.fetchone()

        if not trip_data:
            messagebox.showwarning("Input Error", "Selected trip not found")
            return

        trip = Trip(*trip_data[1:])
        trip.id = trip_data[0]

        self.cursor.execute('''
        INSERT INTO bookings (customer_id, trip_id, status)
        VALUES (%s, %s, %s)
        ''', (customer.id, trip.id, 'Not Confirmed'))
        
        self.mydb.commit()
        
        self.cursor.execute('SELECT LAST_INSERT_ID()')
        booking_id = self.cursor.fetchone()[0]
        print(booking_id)
        
        booking = Booking(booking_id,customer, trip)
        booking.id = booking_id
        self.bookings.append(booking)
        self.booking_list.insert(tk.END, f"{booking.id}- {booking.customer.name}-{booking.trip.destination} - Not Confirmed")

        
        print(f"- Booking created: {customer_entry}, {trip_entry}.")
        self.load_booking_data()

         
    def confirm_booking(self):
        try:
            # Get the selected booking from the Tkinter list
            selected_index = self.booking_list.curselection()[0]
            selected_booking = self.bookings[selected_index]
            
            print("The selected index is ", selected_booking)
            
            # Retrieve the booking ID for the selected booking directly
            booking_id = selected_booking[0]
            
            # Retrieve the current status of the booking to ensure it can be confirmed
            self.cursor.execute('''
            SELECT * FROM bookings WHERE id = %s
            ''', (booking_id,))
            booking_details = self.cursor.fetchone()
        
            if not booking_details:
                raise ValueError("Booking not found in the database")
            
            customer_id, trip_id, current_status = booking_details[1], booking_details[2], booking_details[3]


            if current_status == 'Confirmed':
                raise ValueError("Booking is already confirmed in the database")
            
            # Update the booking status to 'Confirmed'
            self.cursor.execute('''
            UPDATE bookings SET status = 'Confirmed' WHERE id = %s
            ''', (booking_id,))
            self.mydb.commit()

            # Retrieve customer and trip details using the booking's customer_id and trip_id

            self.cursor.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
            customer_details = self.cursor.fetchone()

            self.cursor.execute('SELECT * FROM trips WHERE id = %s', (trip_id,))
            trip_details = self.cursor.fetchone()

            # Update the Tkinter list and show confirmation
            self.booking_list.delete(selected_index)
            self.booking_list.insert(selected_index, f"{selected_booking[0]} - {selected_booking[1]}, {selected_booking[2]} - Confirmed")
            
            confirmed_booking = [selected_booking[0], selected_booking[1], selected_booking[2], 'Confirmed']
            self.show_booking_confirmation(confirmed_booking)
            print(f"Booking confirmed: {selected_booking[1]}, {selected_booking[2]}.")

            # Display customer and trip details (replace with your actual display logic)
            print(f"Customer Details: {customer_details}")
            print(f"Trip Details: {trip_details}")
            
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a booking to confirm")
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        except ValueError as ve:
            messagebox.showwarning("Confirmation Error", str(ve))


    def show_booking_confirmation(self, booking_info):
        booking_id = booking_info[0]
        
        self.cursor.execute('''
        SELECT customer_id,trip_id FROM bookings where id = %s''',(booking_id,))
        booking_data=self.cursor.fetchone()
        
        customer_id=booking_data[0]
        trip_id=booking_data[1]
        
        print("Customer id is ", customer_id)
        print("Trip id is ", trip_id)
        
        self.cursor.execute('''
            SELECT * FROM customers WHERE id = %s
            ''', (customer_id,))
        customer_details = self.cursor.fetchone()
        if customer_details is None:
            customer_info = "Customer details not available"
        else:
            customer_info = f"Customer: {customer_details[1]}, Email: {customer_details[2]}, Phone: {customer_details[3]}, Passport: {customer_details[4]}, Address: {customer_details[5]}"
            
        self.cursor.execute('''
            SELECT * FROM trips WHERE id = %s
            ''', (trip_id,))
        trip_details = self.cursor.fetchone()
        if trip_details is None:
            trip_info = "Trip details not available"
        else:
            trip_info = f"Trip: {trip_details[1]}, Option: {trip_details[2]}, Duration: {trip_details[3]} days, Price: ${trip_details[4]}"

            
        confirmation_message = f"Booking Confirmed!\n\n{customer_info}\n{trip_info}"
        messagebox.showinfo("Booking Confirmed!!", confirmation_message)
        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title("Customer Copy")
        
        tk.Label(confirmation_window, text=confirmation_message, padx=20, pady=20).pack()
        ttk.Button(confirmation_window, text="Got it!", command=lambda: self.close_confirmation_window(confirmation_window)).pack(pady=10)


    def close_confirmation_window(self, window):
        window.destroy()
        self.reset_main_page()

    def reset_main_page(self):
        self.tab_control.destroy()
        self.create_main_page()

def main():
    root = tk.Tk()
    app = TravelAgencyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()