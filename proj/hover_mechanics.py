import tkinter as tk

root = tk.Tk()

def button_hover(widget):
    my_btn['bg'] = 'red'
    status_lbl.config(text="I'm hovering over the button!!")

def button_hover_leave(widget):
    my_btn['bg'] = 'SystemButtonFace'
    status_lbl.config(text='')

my_btn = tk.Button(root, text='Click Me')
my_btn.pack(pady=50)

status_lbl = tk.Label(root, text='', bd=1, relief='sunken', anchor='e')
status_lbl.pack(fill='x', side='bottom', ipadx=2)

my_btn.bind("<Enter>", button_hover)
my_btn.bind("<Leave>", button_hover_leave)

root.mainloop()