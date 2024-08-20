import tkinter as tk

root = tk.Tk()

yellow_frame = tk.Frame(root, width=600, height=80, bg='yellow')
red_frame = tk.Frame(root, width=200, height=500, bg='red')
blue_frame = tk.Frame(root, width=400, height=125, bg='blue')
magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta')
orange_frame = tk.Frame(root, width=400, height=125, bg='orange')
green_frame = tk.Frame(root, width=400, height=125, bg='green')

yellow_frame.grid(row=0, columnspan=2)
red_frame.grid(rowspan=4, column=0)
blue_frame.grid(row=1, column=1)
magenta_frame.grid(row=2, column=1)
orange_frame.grid(row=3, column=1)
green_frame.grid(row=4, column=1)

root.mainloop()