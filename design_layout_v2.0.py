# yellow = timers
# blue = char/boss buttons
# red = character list
# 

import tkinter as tk

root = tk.Tk()

yellow_frame = tk.Frame(root, width=800, height=120, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5) #
blue_frame = tk.Frame(root, width=10, height=600, bg='blue', highlightbackground='black', highlightthickness=1)
red_frame = tk.Frame(root, width=100, height=600, bg='red', highlightbackground='black', highlightthickness=1)

# red_frame = tk.Frame(root, width=200, height=500, bg='red', highlightbackground='black', highlightthickness=1)
# blue_frame = tk.Frame(root, width=400, height=125, bg='blue', highlightbackground='black', highlightthickness=1)
# magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta', highlightbackground='black', highlightthickness=1)
# orange_frame = tk.Frame(root, width=400, height=125, bg='orange', highlightbackground='black', highlightthickness=1)
# green_frame = tk.Frame(root, width=400, height=125, bg='green', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2, sticky='nwse') # 
blue_frame.grid(row=1, column=0, sticky='nswe')
red_frame.grid(row=1, column=1, sticky='nswe')
# red_frame.grid(rowspan=4, column=0, sticky='nwse')
# blue_frame.grid(row=1, column=1, sticky='nwse')
# magenta_frame.grid(row=2, column=1, sticky='nwse')
# orange_frame.grid(row=3, column=1, sticky='nwse')
# green_frame.grid(row=4, column=1, sticky='nwse')

root.mainloop()