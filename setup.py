from tkinter import *
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk
from stegano import lsb
import time

class TextAnimator:
    def __init__(self, master, text , font):
        self.master = master
        self.text = text
        self.font = font
        self.label = Label(master, font=self.font, bg='black', fg='lightblue')
        self.label.pack(pady=10)
        self.animate_text()

    def animate_text(self):
        for char in self.text:
            self.label.config(text=self.label.cget("text") + char)
            self.master.update()
            time.sleep(0.05) 
class STextAnimator:
    def __init__(self, master, text , font):
        self.master = master
        self.text = text
        self.font = font
        self.label = Label(master, font=self.font, bg='black', fg='red')
        self.label.pack(pady=8)
        self.animate_text()

    def animate_text(self):
        for char in self.text:
            self.label.config(text=self.label.cget("text") + char)
            self.master.update()
            time.sleep(0.02) 

def encode_image():
    global encode_wn  

    def browse_file(entry, str_var, img_label):
     file_path = filedialog.askopenfilename()
     if file_path:
        entry.delete(0, END)
        entry.insert(0, file_path)
        img = Image.open(file_path)
        img = img.resize((250, 220), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        img_label.configure(image=img_tk)
        img_label.image = img_tk


    def encode(img_path, text_to_be_encoded, after_save_path, text_entry, canvas):
        try:
            image = Image.open(img_path)
            encoded_image = lsb.hide(image, text_to_be_encoded)
            encoded_image.save(after_save_path + ".png")

            canvas.image = ImageTk.PhotoImage(encoded_image)
            canvas.create_image(0, 0, anchor=NW, image=canvas.image)

            text_entry.config(state=NORMAL)
            text_entry.delete(1.0, END)
            text_entry.insert(END, "Image encoded successfully.")
            text_entry.config(state=DISABLED)
        except Exception as e:
            mb.showerror("Error", f"An error occurred: {str(e)}")
    
    def decode(img_path, str_var, text_entry):
        try:
            decoded_message = lsb.reveal(Image.open(img_path))
            str_var.set(decoded_message)

            text_entry.config(state=NORMAL)
            text_entry.delete(1.0, END)
            text_entry.insert(END, f"Message decoded successfully:\n\n{decoded_message}")
            text_entry.config(state=DISABLED)
        except Exception as e:
            mb.showerror("Error", f"An error occurred: {str(e)}")

    encode_wn = Toplevel(root)
    encode_wn.geometry('700x600')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='black')

    # Image Selection
    canvas = Canvas(encode_wn, width=700, height=300, bg='black')
    canvas.pack()

    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='black', fg='lightgreen').place(x=258, rely=0)

    Label(encode_wn, text='Select the image to encode:', font=("Times New Roman", 13), bg='black', fg='lightgreen').place(x=10, y=330)
    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=330)
    img_label = Label(encode_wn, bg='black')
    img_label.place(x=10, y=50 )
    Button(encode_wn, text='Browse', font=('Helvetica', 10), fg='black', bg='lightgreen',
           command=lambda: browse_file(img_path, None, img_label)).place(x=570, y=327)

    # Data Entry and Display
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='black', fg='lightgreen').place(x=10, y=360)
    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=360)

    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13), bg='black', fg='lightgreen').place(x=10, y=390)
    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=390)

    text_entry = Text(encode_wn, wrap=WORD, width=70, height=5, state=DISABLED, bg='black', fg='lightgreen')
    text_entry.place(x=10, y=490)

    Button(encode_wn, text='Encode', font=('Helvetica', 10), fg='black', bg='lightgreen',
           command=lambda: encode(img_path.get(), text_to_be_encoded.get(), after_save_path.get(), text_entry, canvas)).place(x=350, y=420)

def decode_image():
    global decode_wn  # Reference the global variable

    def browse_file(entry, str_var, img_label):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, END)
            entry.insert(0, file_path)
            img = Image.open(file_path)
            img = img.resize((250, 220), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk

    def decode(img_path, str_var, text_entry):
        try:
            decoded_message = lsb.reveal(Image.open(img_path))
            str_var.set(decoded_message)

            text_entry.config(state=NORMAL)
            text_entry.delete(1.0, END)
            text_entry.insert(END, f"Message decoded successfully:\n\n{decoded_message}")
            text_entry.config(state=DISABLED)
        except Exception as e:
            mb.showerror("Error", f"An error occurred: {str(e)}")

    decode_wn = Toplevel(root)
    decode_wn.geometry('700x600')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='black')

    # Image Selection
    canvas = Canvas(decode_wn, width=700, height=300, bg='black')
    canvas.pack()

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='black', fg='lightgreen').place(x=258, rely=0)

    Label(decode_wn, text='Select the image to decode:', font=("Times New Roman", 13), bg='black', fg='lightgreen').place(x=10, y=330)
    img_entry = Entry(decode_wn, width=30)
    img_entry.place(x=350, y=330)
    img_label = Label(decode_wn, bg='black')
    img_label.place(x=10, y=50)
    Button(decode_wn, text='Browse', font=('Helvetica', 10 ), fg='black', bg='lightgreen',
           command=lambda: browse_file(img_entry, None, img_label)).place(x=550, y=327 )

    str_var = StringVar()

    # Data Display
    Label(decode_wn, text='Decoded Message:', font=("Times New Roman", 13), bg='black', fg='lightgreen').place(x=10, y=360)
    decoded_message = Entry(decode_wn, width=35, textvariable=str_var, state='readonly')
    decoded_message.place(x=350, y=360)

    text_entry = Text(decode_wn, wrap=WORD, width=70, height=5, state=DISABLED, bg='black', fg='lightgreen')
    text_entry.place(x=10, y=490)

    Button(decode_wn, text='Decode', font=('Helvetica', 12),  fg='black', bg='lightgreen',
           command=lambda: decode(img_entry.get(), str_var, text_entry)).place(x=300, y=410)
    


root = Tk()
root.title("Steganography App")
root.geometry('600x400')
root.configure(bg='black')

# Use a fixed-width font for the hacker style
font = ("Courier New", 12)
font1 = ("Courier New", 10,'bold')

Label(root, text='Steganography App', font=("Comic Sans MS", 15), bg='black', fg='lightgreen').pack(pady=10)
text_animator = TextAnimator(root, "\n\nIn the digital realm, steganography whispers secrets in\n the language of pixels, where silence speaks volumes to\n those who know how to listen Concealed within the \ncanvas of images.\n", font)
encode_btn = Button(root, text='Encode Image', font=('Helvetica', 12), bg='lightgreen', fg='black', command=encode_image,highlightthickness=4, highlightcolor="blue", highlightbackground="red")
encode_btn.pack(pady=10)
decode_btn = Button(root, text='Decode Image', font=('Helvetica', 12), bg='lightgreen',fg='black', command=decode_image , highlightthickness=4, highlightcolor="blue", highlightbackground="red")
decode_btn.pack(pady=10)
text_animator = STextAnimator(root, "powered by team 🜪⌘∪я⚶🜩🜿🜼\n\nAll Rights Reserverd", font1)
root.mainloop()
