from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# PASSWORD GENERATOR


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# FIND PASSWORD

def find_password():
    searched_website = name_of_website_search_entry.get()
    try:
        with open("saved_data.json") as sd:
            data = json.load(sd)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if searched_website in data:
            email = data[searched_website]["email"]
            password = data[searched_website]["password"]
            messagebox.showinfo(title=searched_website, message=f"Email/Phone Number: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {searched_website} exists.")


# SAVE PASSWORD


def save():
    entered_website = name_of_website_entry.get()
    entered_email_id = email_id_entry.get()
    entered_password = password_entry.get()
    new_data = {
        entered_website: {
            "email": entered_email_id,
            "password": entered_password,
        }
    }
    if len(entered_website) == 0 or len(entered_password) == 0 or len(entered_email_id) == 0:
        messagebox.showinfo(title="Warning", message="Please make sure you haven't left any field empty.")
    else:
        is_true = messagebox.askokcancel(title=entered_website, message=f"You have entered Email = {entered_email_id}\n"
                                                                        f"Password = {entered_password}\n"
                                                                        f"You sure about saving it?")
        if is_true:
            try:
                with open("saved_data.json", "r") as sd:
                    data = json.load(sd)
            except FileNotFoundError:
                with open("saved_data.json", "w") as sd:
                    json.dump(new_data, sd, indent=4)
            else:
                data.update(new_data)
                with open("saved_data.json", "w") as sd:
                    json.dump(data, sd, indent=4)
            finally:
                name_of_website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_id_entry.delete(0, END)
                name_of_website_entry.focus()


# UI SETUP


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="ghost white")

canvas = Canvas(height=200, width=320)
logo_img = PhotoImage(file="img.png ")
canvas.create_image(100, 100, image=logo_img)
canvas.config(bg="ghost white", highlightthickness=0)
canvas.grid(column=1, row=0)

name_of_website_label = Label(text="Name of Website : ")
name_of_website_label.config(bg="ghost white")
name_of_website_label.grid(row=1, column=0)
email_id_label = Label(text="Email ID/Username/Phone : ")
email_id_label.config(bg="ghost white")
email_id_label.grid(row=2, column=0)
password_label = Label(text="Password : ")
password_label.config(bg="ghost white")
password_label.grid(row=3, column=0)

name_of_website_entry = Entry(width=40)
name_of_website_entry.grid(row=1, column=1, columnspan=2)
name_of_website_entry.focus()
email_id_entry = Entry(width=40)
email_id_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=40)
password_entry.grid(row=3, column=1, columnspan=2)
name_of_website_search_entry = Entry(width=20)
name_of_website_search_entry.place(height=20, x=310, y=3, anchor=NW)

password_generate_button = Button(text="Generate Password", command=generate_password)
password_generate_button.grid(row=4, column=0, sticky=W + E)
search_button = Button(text="Search", command=find_password)
search_button.place(height=22, x=480, y=2, anchor=NE)
add_button = Button(text="Add", width=34, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
