import tkinter as tk


root = tk.Tk()

a_lbl = tk.Label(root, text='Right Man')
b_lbl = tk.Label(root, text='Left Man')

a_lbl.pack(side='right')
b_lbl.pack(side='left')

root.mainloop()