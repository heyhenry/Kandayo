import tkinter as tk

root = tk.Tk()

yellow_frame = tk.Frame(root, width=600, height=80, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5)
red_frame = tk.Frame(root, width=200, height=500, bg='red', highlightbackground='black', highlightthickness=1)
blue_frame = tk.Frame(root, width=400, height=125, bg='blue', highlightbackground='black', highlightthickness=1)
magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta', highlightbackground='black', highlightthickness=1)
orange_frame = tk.Frame(root, width=400, height=125, bg='orange', highlightbackground='black', highlightthickness=1)
green_frame = tk.Frame(root, width=400, height=125, bg='green', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2)
yellow_frame.grid_propagate(False)
red_frame.grid(rowspan=4, column=0)
blue_frame.grid(row=1, column=1)
magenta_frame.grid(row=2, column=1)
orange_frame.grid(row=3, column=1)
green_frame.grid(row=4, column=1)

co_lbl = tk.Label(yellow_frame, text='Characters Overview', font=('Helvetica', 18), bg='yellow')
yellow_frame.columnconfigure(0, weight=1)
yellow_frame.columnconfigure(1, weight=1)
yellow_frame.columnconfigure(2, weight=1)
co_lbl.grid(row=0, column=1)

root.mainloop()