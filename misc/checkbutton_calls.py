import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

img = Image.open('incomplete_status.png')
img.thumbnail((100,100))
img = ImageTk.PhotoImage(img)

img2 = Image.open('complete_status.png')
img2.thumbnail((100, 100))
img2 = ImageTk.PhotoImage(img2)

cb_one_check = tk.IntVar()
cb_zet_check = tk.IntVar()

def boop(clicked_button, button_id):

    if clicked_button.get():
        button_id.config(image=img2)
    else:
        button_id.config(image=img)

title = tk.Label(root, text='Title')
cb_one = tk.Checkbutton(root, image=img, variable=cb_one_check, command=lambda:boop(cb_one_check, cb_one))
cb_one.config(indicatoron=False, borderwidth=0)
cb_zet = tk.Checkbutton(root, image=img, variable=cb_zet_check, command=lambda:boop(cb_zet_check, cb_zet))
cb_zet.config(indicatoron=False, borderwidth=0)

title.pack()
cb_one.pack()
cb_zet.pack()

root.mainloop()