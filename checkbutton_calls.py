import tkinter as tk

root = tk.Tk()

def boop(clicked_button):
    clicked_button.config(text='Poop')

title = tk.Label(root, text='Title')
cb_one = tk.Checkbutton(root, text='Check One', command=lambda:boop(cb_one))
cb_zet = tk.Checkbutton(root, text='Check Zet', command=lambda:boop(cb_zet))

title.pack()
cb_one.pack()
cb_zet.pack()

root.mainloop()