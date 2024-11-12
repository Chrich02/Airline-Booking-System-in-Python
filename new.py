import csv
import random
import re

class Flight:
    def __init__(self, max_seats=100):
        self.max_seats = max_seats
        self.available_seats = max_seats
        self.bookings = {} # {customer_id: ticket_number} dict as efficient look-up and unique keys
        self.cancelled_bookings = [] # list for ordered sequence and flexible storage 

        # initialise window seat tracking. nth-term an = 3n - 2 for the window seat sequence listed in assessment brief
        self.window_seats = [3 * n - 2 for n in range(1, max_seats // 3 + 1)]

    def generate_customer_id(self):# high-traffic scenarios could duplicate a customer ID using random.randint 
        used_ids = set(customer_id for customer_id, _ in self.bookings.items()) # create a set of cusotmer IDs used in existing bookings
        while True:
            customer_id = random.randint(100, 999)
            if customer_id not in used_ids: # checks if the generated ID is in used_ids
                return customer_id


    def generate_ticket_number(self, customer_id): # same logic from above to avoid duplication of ticket_numbers
        used_ticket_numbers = set(ticket_number for ticket_number, _ in self.bookings.values())
        while True:
            ticket_number = f"{customer_id}-{str(random.randint(10000, 99999)).zfill(5)}" # assign a five diget ticket ID, padded with zeroes if under 5 digets 
            if ticket_number not in used_ticket_numbers:
                return ticket_number
        
    
    def window_seat_tickets(self):
        for ticket_number, (_, seat_number, _) in self.bookings.items():
            if seat_number % 3 == 1: # modulo equivalent of an = 3n - 2 to distinguish the first of every row of three seats as a window seat
                print(f"Window Seat Ticket: {ticket_number}")


    def book_ticket(self):
        if self.available_seats > 0: # check that there are seats left to allocate
            customer_id = self.generate_customer_id()
            ticket_number = self.generate_ticket_number(customer_id)

            # Assign window seat if available 
            if self.window_seats:
                seat_number = self.window_seats.pop(0) # removes and returns the first available window seat from the list
            else:
                seat_number = self.available_seats

            self.bookings[customer_id] = (ticket_number, seat_number) # Store ticket number and seat number together for the cancel ticket windowseat re-appending 
            self.available_seats -= 1 # as now booked, decrement the available seat counter 
            print(f"Booking successful! Your ticket number is: {ticket_number}, Seat: {seat_number}")
        else:
            print("Sorry, the flight is fully booked.")

    def cancel_ticket(self, ticket_number):
        # Validate ticket number format using regular expression
        pattern = r"\d{3}-\d{5}"
        if not re.match(pattern, ticket_number):
            print("Invalid ticket number format. Please enter in the format 123-12345 as displayed on your booking.")
            return

        found = False
        for customer_id, (ticket, seat_number) in self.bookings.items():
            ticket_parts = ticket.split('-')
            if ticket_parts[1] == ticket_number.split('-')[1]:  # if the input matches an exisitng ticket number
                del self.bookings[customer_id]
                self.available_seats += 1

                # If the cancelled seat was a window seat, add it back to the list of available window seats
                if seat_number % 3 == 1:
                    self.window_seats.append(seat_number)

                self.cancelled_bookings.append((customer_id, ticket_number))  # Append to a separate list for cancelled bookings
                found = True
                print(f"Ticket {ticket_number} cancelled successfully.")
                break

        if not found:
            print("Ticket not found.")

    def update_ticket(self, ticket_number, new_info):
        #implement ticket update logic (e.g., change passenger name, contact details)
        pass 

    def query_booking(self, ticket_number):
        for customer_id, ticket in self.bookings.items():
            if ticket == ticket_number:
                print(f"Customer ID: {customer_id}\nTicket Number: (ticket)")
                return 
        print("Ticket not found.")

    def save_bookings(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Customer ID', 'Ticket Number', 'Available Seats']) # inclue seat number
            for customer_id, (ticket_number, seat_number) in self.bookings.items():
                writer.writerow([customer_id, ticket_number,seat_number, self.available_seats])

    def load_bookings(self, filename):
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader) # skip header row
                for row in reader:
                    customer_id, ticket_number = int(row[0]), row[1]
                    self.bookings[customer_id] = ticket_number
                    self.available_seats -= 1
        except FileNotFoundError:
            pass

    def save_cancelled_bookings(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Cancelled Customer ID', 'Cancelled Ticket Number'])
            for customer_id, ticket_number in self.cancelled_bookings:
                writer.writerow([customer_id, ticket_number])
    
# ADMIN TOOL 
    def reset_flight(self):
        self.available_seats = self.max_seats
        self.bookings = {}
        self.window_seats = [3 * n - 2 for n in range(1, self.max_seats // 3 + 1)]
        print("Flight has been reset. All seats are now available.")


def main():
    flight = Flight()
    flight.load_bookings('bookings.csv')

    while True:
        print("Welcome to Sagir's Airline! Please enter the number corresponding to your desired query:")
        print(f"\n1. Book a ticket: {flight.available_seats} seats remaining")
        print("2. Cancel a ticket")
        print("3. Update a ticket")
        print("4. Query a booking")
        print("5. Save and Exit")
        print("6. Reset Flight")  # Admin tool

        choice = input("Enter your choice: ")

        if choice.isdigit():  # Check if the input is a digit
            choice = int(choice)
            if choice == 1:
                flight.book_ticket()
            elif choice == 2:
                ticket_number = input("Enter ticket number to cancel: ")
                flight.cancel_ticket(ticket_number)
                flight.save_cancelled_bookings('cancelled.csv')
            elif choice == 3:
                # Implement ticket update logic
                print("Update functionality coming soon.")
            elif choice == 4:
                ticket_number = input("Enter ticket number to query: ")
                flight.query_booking(ticket_number)
            elif choice == 5:
                flight.save_bookings('bookings.csv')
                print("Thank you for using Sagir's Airline. Your changes have been saved.")
                break
            elif choice == 6:
                flight.reset_flight()
            else:
                print("Invalid choice. Please select a valid option.")
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk
import csv
import random

class AirlineBookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airline Booking System")
        self.geometry("400x300")

        # GUI components and event handlers

if __name__ == "__main__":
    app = AirlineBookingApp()
    app.mainloop()