# working version of a ticked state checkbutton for the top level widget
# the usage of .var is required to python's garbage collection throwing out the set state of True

import tkinter as tk

root = tk.Tk()
root.title('Main Window')

def open_popup():
    
    cb_var = tk.IntVar()
    cb_var.set(True)

    pp = tk.Toplevel(root)
    pp.title('Top Level Window')

    pp_cb = tk.Checkbutton(pp, text='Did ya poop?', variable=cb_var)
    pp_cb.pack()

    pp_cb.var = cb_var

clickme_btn = tk.Button(root, text='--> Click Me <--', command=open_popup)
clickme_btn.pack()

root.mainloop()

