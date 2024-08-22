import tkinter as tk

root = tk.Tk()
root.resizable(False, False)

# frames setup
yellow_frame = tk.Frame(root, width=600, height=80, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5)
red_frame = tk.Frame(root, width=200, height=500, bg='red', highlightbackground='black', highlightthickness=1)
blue_frame = tk.Frame(root, width=400, height=125, bg='blue', highlightbackground='black', highlightthickness=1)
magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta', highlightbackground='black', highlightthickness=1)
orange_frame = tk.Frame(root, width=400, height=125, bg='orange', highlightbackground='black', highlightthickness=1)
green_frame = tk.Frame(root, width=400, height=125, bg='green', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2, sticky='nwse')
red_frame.grid(rowspan=4, column=0, sticky='nwse')
blue_frame.grid(row=1, column=1, sticky='nwse')
magenta_frame.grid(row=2, column=1, sticky='nwse')
orange_frame.grid(row=3, column=1, sticky='nwse')
green_frame.grid(row=4, column=1, sticky='nwse')

# to not ignore frame attributes when widgets are introduced
yellow_frame.grid_propagate(False)
red_frame.grid_propagate(False)

# yellow frame
co_lbl = tk.Label(yellow_frame, text='Characters Overview', font=('Kozuka Gothic Pro B', 18), bg='yellow')
co_lbl.place(relx=0.5, rely=0.5, anchor='center')

# red frame
chars_lb = tk.Listbox(red_frame, height=30)
chars_lb.place(relx=0.5, rely=0.5, anchor='center')

# blue frame

# to check if buttons are working correctly
def run(i : str):
    if i == 'add':
        print('add works')
    elif i == 'upd':
        print('update works')
    elif i == 'del':
        print('delete works')
    else:
        print('Error!')

blue_buttons = {'font':('Kozuka Gothic Pro B', 12), 'relief': 'raised'}

addchar_btn = tk.Button(blue_frame, text='Add Char', **blue_buttons, command=lambda:run('add'))
updchar_btn = tk.Button(blue_frame, text='Update Char', **blue_buttons, command=lambda:run('upd'))
delchar_btn = tk.Button(blue_frame, text='Delete Char', **blue_buttons, command=lambda:run('del'))

blue_frame.grid_rowconfigure(0, weight=1)
blue_frame.grid_columnconfigure(0, weight=1)
blue_frame.grid_columnconfigure(1, weight=1)
blue_frame.grid_columnconfigure(2, weight=1)

addchar_btn.grid(row=0, column=0)
updchar_btn.grid(row=0, column=1)
delchar_btn.grid(row=0, column=2)

# root configs for resizability ('can ignore for time being, may reinstate later')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

