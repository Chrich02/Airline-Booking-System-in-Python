import csv
import random
import re

class Flight:
    def __init__(self, max_seats=100):
        """Initializes the flight with a maximum number of seats.
    
        Args:
            max_seats (int): Maximum number of seats available on the flight. Defaults to 100.
            
        Attributes:
            available_seats (int): Tracks the number of seats still available.
            bookings (dict): Maps customer IDs to tuples of (ticket number, seat number).
            cancelled_bookings (list): Stores cancelled bookings as tuples of (customer ID, ticket number).
            window_seats (list): Pre-computed list of seat numbers that are window seats.
            """
        self.max_seats = max_seats
        self.available_seats = max_seats
        self.bookings = {} 
        self.cancelled_bookings = [] 
        self.window_seats = [3 * n - 2 for n in range(1, max_seats // 3 + 1)]


    def generate_customer_id(self): 
        """Generates a unique 3-digit customer ID.
    
        Ensures the generated ID does not duplicate any existing customer ID in the bookings.
        
        Returns:
            int: A unique 3-digit customer ID.
        """
        used_ids = set(customer_id for customer_id, _ in self.bookings.items()) 
        while True:
            customer_id = random.randint(100, 999)
            if customer_id not in used_ids: 
                return customer_id


    def generate_ticket_number(self, customer_id): 
        """Generates a unique ticket number for a customer.
    
        The ticket number is in the format xxx-xxxxx, where the first part is the customer ID.
        
        Args:
            customer_id (int): The unique customer ID.
        
        Returns:
            str: A unique ticket number.
        """
        used_ticket_numbers = set(ticket_number for ticket_number, _ in self.bookings.values())
        while True:
            ticket_number = f"{customer_id}-{str(random.randint(10000, 99999)).zfill(5)}" 
            if ticket_number not in used_ticket_numbers:
                return ticket_number
        
    
    def window_seat_tickets(self):
        # Displays ticket numbers for all booked window seats.
        for ticket_number, (_, seat_number, _) in self.bookings.items():
            if seat_number % 3 == 1: # modulo equivalent of an = 3n - 2 to distinguish the first of every row of three seats as a window seat
                print(f"Window Seat Ticket: {ticket_number}")


    def book_ticket(self):
        """Books a ticket for the next available seat.
    
        Assigns a window seat if available. Updates seat availability and stores booking information.
        """
        if self.available_seats > 0: 
            customer_id = self.generate_customer_id()
            ticket_number = self.generate_ticket_number(customer_id)

            if self.window_seats:
                seat_number = self.window_seats.pop(0) 
            else:
                seat_number = self.available_seats

            self.bookings[customer_id] = (ticket_number, seat_number)   
            self.available_seats -= 1  
            print(f"Booking successful! Your ticket number is: {ticket_number}, Seat: {seat_number}")
        else:
            print("Sorry, the flight is fully booked.")

    def validate_ticket_number(self, ticket_number):
        """Validates the format of the ticket number.
    
        Args:
            ticket_number (str): The ticket number to validate.
            
        Returns:
            bool: True if the ticket number is valid, False otherwise.
        """ 
        pattern = r"\d{3}-\d{5}"
        if not re.match(pattern, ticket_number):
            print("Invalid ticket number format. Please enter in the format 123-12345 as displayed on your booking.")
            return False 
        return True
    
    def cancel_ticket(self, ticket_number):
        """Cancels a booking based on the ticket number.
    
        Validates the ticket number format, removes the booking, and updates seat availability.
        If the seat was a window seat, re-adds it to the available window seats.
        
        Args:
            ticket_number (str): The ticket number to cancel.
        """
        if not self.validate_ticket_number(ticket_number):
            return 

        found = False
        for customer_id, (ticket, seat_number) in self.bookings.items():
            ticket_parts = ticket.split('-')
            if ticket_parts[1] == ticket_number.split('-')[1]:  
                del self.bookings[customer_id]
                self.available_seats += 1

                if seat_number % 3 == 1:
                    self.window_seats.append(seat_number)

                self.cancelled_bookings.append((customer_id, ticket_number))  
                found = True
                print(f"Ticket {ticket_number} cancelled successfully.")
                break

        if not found:
            print("Ticket not found.")


    def query_booking(self, ticket_number):
        """Queries booking information based on the ticket number.
    
        Validates the ticket number format and displays the associated booking details.
        
        Args:
            ticket_number (str): The ticket number to query.
        """
        if not self.validate_ticket_number(ticket_number):  
            return 
        
        for customer_id, (stored_ticket, seat_number) in self.bookings.items():
            if stored_ticket == ticket_number:
                is_window_seat = "Yes" if seat_number % 3 == 1 else "No"
                print(f"Thank you for entering your ticket number. Here's your booking information:")
                print(f"Customer ID: {customer_id}")
                print(f"Ticket Number: {ticket_number}")
                print(f"Seat Number: {seat_number}")
                print(f"Window seat: {is_window_seat}")
                return 
            
        print("Ticket not found.") 


    def save_bookings(self, filename):
        """Saves all current bookings to a CSV file.
    
        Args:
            filename (str): The name of the file to save bookings to.
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Customer ID', 'Ticket Number', 'Available Seats']) 
            for customer_id, (ticket_number, seat_number) in self.bookings.items():
                writer.writerow([customer_id, ticket_number,seat_number, self.available_seats])


    def load_bookings(self, filename):
        """Loads bookings from a CSV file.
    
        Args:
            filename (str): The name of the file to load bookings from.
            
        If the file does not exist, it gracefully handles the error.
        """
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader) 
                for row in reader:
                    customer_id, ticket_number, seat_number = int(row[0]), row[1], int(row[2])
                    self.bookings[customer_id] = (ticket_number, seat_number)
                    self.available_seats -= 1

                    if seat_number % 3 ==1 and seat_number in self.window_seats:
                        self.window_seats.remove(seat_number)
        except FileNotFoundError:
            print(f" No existing booking file found: {filename}. Starting with empty records.")


    def save_cancelled_bookings(self, filename):
        """Saves cancelled bookings to a CSV file.
        
        Args:
            filename (str): The name of the file to save cancelled bookings to.
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Cancelled Customer ID', 'Cancelled Ticket Number'])
            for customer_id, ticket_number in self.cancelled_bookings:
                writer.writerow([customer_id, ticket_number])
    

    """def reset_flight(self):
        *ADMIN TOOL* Resets the flight to its initial state.
        
        Clears all bookings and restores the full set of available seats.
        
        self.available_seats = self.max_seats
        self.bookings = {}
        self.window_seats = [3 * n - 2 for n in range(1, self.max_seats // 3 + 1)]
        print("Flight has been reset. All seats are now available.")
    """


def main():
    flight = Flight()
    flight.load_bookings('bookings.csv')

    while True:
        print("Welcome to Sagir's Airline! Please enter the number corresponding to your desired query:")
        print(f"\n1. Book a ticket: {flight.available_seats} seats remaining")
        print("2. Cancel a ticket")
        print("3. Query a booking")
        print("4. Save and Exit")
        # print("5. Reset Flight\n")  # Admin tool

        choice = input("Enter your choice: ")

        if choice.isdigit():  # Check if the input is a digit
            choice = int(choice)
            if choice == 1:
                flight.book_ticket()

            elif choice == 2:
                ticket_number = input("\nEnter ticket number to cancel: ")
                flight.cancel_ticket(ticket_number)
                flight.save_cancelled_bookings('cancelled.csv')

            elif choice == 3:
                ticket_number = input("\nEnter your ticket number for seat information: ")
                flight.query_booking(ticket_number)

            elif choice == 4:
                flight.save_bookings('bookings.csv')
                print("\nThank you for using Sagir's Airline. Your changes have been saved.")
                break

            elif choice == 5:
                flight.reset_flight()

            else:
                print("\nInvalid choice. Please select a valid option.")
        else:
            print("\nInvalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
"""
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
"""