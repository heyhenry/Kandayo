import tkinter as tk

root = tk.Tk()

def button_hover(event, widget_name, status_bar, info_text):
    widget_name['bg'] = 'red'
    status_bar.config(text=info_text)

def button_hover_leave(event, widget_name, status_bar):
    widget_name['bg'] = 'SystemButtonFace'
    status_bar.config(text='')

my_btn = tk.Button(root, text='Click Me')
my_btn.pack(pady=50)
second_btn = tk.Button(root, text="Don't Click Me!")
second_btn.pack(pady=10)

status_lbl = tk.Label(root, text='', bd=1, relief='sunken', anchor='e')
status_lbl.pack(fill='x', side='bottom', ipadx=2)

my_btn.bind("<Enter>", lambda event: button_hover(event, my_btn, status_lbl, 'Poooper Hovered!'))
my_btn.bind("<Leave>", lambda event: button_hover_leave(event, my_btn, status_lbl))

second_btn.bind("<Enter>", lambda event: button_hover(event, second_btn, status_lbl, 'Oh no!! You CLICKED MEEE'))
second_btn.bind("<Leave>", lambda event: button_hover_leave(event, second_btn, status_lbl))

root.mainloop()