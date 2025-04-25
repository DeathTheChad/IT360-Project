from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from stegano import lsb
import os

root = Tk()
root.title("Steganography - Hide a secret text message in an Image")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#CC313D")

# Declare 'secret' and 'filename' globally
secret = None
filename = None

def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:  # Check if a file was selected
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img, width=250, height=250)
        lbl.image = img
    else:
        messagebox.showerror("Error", "No image file selected.")

def Hide():
    global secret
    message = text1.get(1.0, END).strip()
    if not filename:
        messagebox.showerror("Error", "No image selected.")
        return
    if not message:
        messagebox.showerror("Error", "Message is empty.")
        return
    secret = lsb.hide(filename, message)
    messagebox.showinfo("Success", "Message hidden successfully.")  # Success message

def Show():
    if not filename:
        messagebox.showerror("Error", "No image selected.")
        return
    
    # Reveal the hidden message
    clear_message = lsb.reveal(filename)
    
    # Check if a message exists
    if clear_message:
        text1.delete(1.0, END)  # Clear any previous text
        text1.insert(END, clear_message)  # Insert the revealed message
    else:
        messagebox.showerror("Error", "No hidden message found in the image.")

def save():
    global secret
    if secret is None:
        messagebox.showerror("Error", "No secret message to save.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if save_path:
        secret.save(save_path)
        messagebox.showinfo("Success", f"Image saved to {save_path}")  # Success message

Label(root, text="", bg="#CC313D", fg="white", font="arial 25 bold").place(x=100, y=20)

# First Frame
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)
lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame
f2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
f2.place(x=350, y=80)

text1 = Text(f2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(f2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

frame3 = Frame(root, bd=3, bg="#F7C5CC", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", bg="#FCF6F5", fg="black", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", bg="#FCF6F5", fg="black", command=save).place(x=160, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#F7C5CC", fg="black").place(x=20, y=5)

# Fourth Frame
frame4 = Frame(root, bd=3, bg="#F7C5CC", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", bg="#FCF6F5", fg="black", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", bg="#FCF6F5", fg="black", command=Show).place(x=160, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="#F7C5CC", fg="black").place(x=20, y=5)

root.mainloop()
