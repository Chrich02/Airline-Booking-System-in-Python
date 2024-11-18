import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv
import random
import re

class Flight:
    def __init__(self, max_seats=100):
        self.max_seats = max_seats
        self.available_seats = max_seats
        self.bookings = {}
        self.cancelled_bookings = []
        self.window_seats = [3 * n - 2 for n in range(1, max_seats // 3 + 1)]

    def generate_customer_id(self):
        used_ids = set(self.bookings.keys())
        if len(used_ids) >= 900:
            raise ValueError("Maximum number of unique customer IDs reached.")
        while True:
            customer_id = random.randint(100, 999)
            if customer_id not in used_ids:
                return customer_id

    def generate_ticket_number(self, customer_id):
        used_ticket_numbers = set(ticket_number for ticket_number, _ in self.bookings.values())
        while True:
            ticket_number = f"{customer_id}-{str(random.randint(10000, 99999)).zfill(5)}"
            if ticket_number not in used_ticket_numbers:
                return ticket_number

    def book_ticket(self):
        if self.available_seats <= 0:
            return None, None
        customer_id = self.generate_customer_id()
        ticket_number = self.generate_ticket_number(customer_id)
        if self.window_seats:
            seat_number = self.window_seats.pop(0)
        else:
            seat_number = self.available_seats
        self.bookings[customer_id] = (ticket_number, seat_number)
        self.available_seats -= 1
        return ticket_number, seat_number

    def cancel_ticket(self, ticket_number):
        for customer_id, (stored_ticket, seat_number) in list(self.bookings.items()):
            if stored_ticket == ticket_number:
                del self.bookings[customer_id]
                self.available_seats += 1
                if seat_number % 3 == 1:
                    self.window_seats.append(seat_number)
                self.cancelled_bookings.append((customer_id, ticket_number))
                self.save_cancelled_tickets('cancelled.csv')
                return True
        return False

    def query_booking(self, ticket_number):
        for customer_id, (stored_ticket, seat_number) in self.bookings.items():
            if stored_ticket == ticket_number:
                is_window_seat = seat_number % 3 == 1
                return {
                    "customer_id": customer_id,
                    "seat_number": seat_number,
                    "is_window_seat": is_window_seat,
                }
        return None

    def save_bookings(self, filename='bookings.csv'):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Customer ID", "Ticket Number", "Seat Number"])
                for customer_id, (ticket_number, seat_number) in self.bookings.items():
                    writer.writerow([customer_id, ticket_number, seat_number])
        except Exception as e:
            print(f"Error saving bookings: {e}")

    def save_cancelled_tickets(self, filename):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Customer ID", "Ticket Number"])
                for customer_id, ticket_number in self.cancelled_bookings:
                    writer.writerow([customer_id, ticket_number])
        except Exception as e:
            print(f"Error saving cancelled tickets: {e}")


class FlightApp:
    def __init__(self, root, flight):
        self.flight = flight
        self.root = root
        self.root.title("Flight Booking System")

        # Label
        self.label = tk.Label(root, text="Welcome to Sagir's Airline!", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Book Ticket Button
        self.book_button = tk.Button(root, text="Book Ticket", command=self.book_ticket)
        self.book_button.pack(pady=5)

        # Cancel Ticket Button
        self.cancel_button = tk.Button(root, text="Cancel Ticket", command=self.cancel_ticket)
        self.cancel_button.pack(pady=5)

        # Query Booking Button
        self.query_button = tk.Button(root, text="Query Booking", command=self.query_booking)
        self.query_button.pack(pady=5)

        # Save Button
        self.save_button = tk.Button(root, text="Save and Quit", command=self.save_and_quit)
        self.save_button.pack(pady=5)

    def book_ticket(self):
        ticket_number, seat_number = self.flight.book_ticket()
        if ticket_number and seat_number:
            messagebox.showinfo("Booking Successful", f"Ticket Number: {ticket_number}\nSeat Number: {seat_number}")
        else:
            messagebox.showwarning("Booking Failed", "No seats available!")

    def cancel_ticket(self):
        ticket_number = self.ask_ticket_number("Cancel Ticket")
        if ticket_number:
            success = self.flight.cancel_ticket(ticket_number)
            if success:
                messagebox.showinfo("Cancellation Successful", f"Ticket {ticket_number} has been canceled.")
            else:
                messagebox.showerror("Cancellation Failed", "Ticket not found.")

    def query_booking(self):
        ticket_number = self.ask_ticket_number("Query Booking")
        if ticket_number:
            booking_info = self.flight.query_booking(ticket_number)
            if booking_info:
                details = (
                    f"Customer ID: {booking_info['customer_id']}\n"
                    f"Seat Number: {booking_info['seat_number']}\n"
                    f"Window Seat: {'Yes' if booking_info['is_window_seat'] else 'No'}"
                )
                messagebox.showinfo("Booking Information", details)
            else:
                messagebox.showerror("Query Failed", "Ticket not found.")

    def save_and_quit(self):
        self.flight.save_bookings('bookings.csv')
        messagebox.showinfo("Save Successful", "Bookings saved to 'bookings.csv'.")
        self.root.quit()

    def ask_ticket_number(self, title):
        return simpledialog.askstring(title, "Enter your ticket number:")


if __name__ == "__main__":
    flight = Flight()
    root = tk.Tk()
    app = FlightApp(root, flight)
    root.mainloop()
