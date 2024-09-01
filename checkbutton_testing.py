from tkinter import *

root = Tk()

def func(var):
    if var.get(): # Also same as 'if var.get() == 1'
        print('It is ticked')
    else:
        print('Not ticked')

def new_win(cb):
    top = Toplevel(root)
    
    def cmd(cb):
        cb.invoke()

    Button(top, text='Click me to toggle the tickbox', command=lambda: cmd(cb)).pack(pady=5)

var = IntVar()
cb = Checkbutton(root, text='Checkbutton 1', variable=var, command=lambda: func(var))
cb.pack(padx=10, pady=10)

# test case of var being used for multiple checkbuttons --> verdict you need separate variables for each checkbutton
bb = Checkbutton(root, text='Checkbutton 2', variable=var, command=lambda: func(var))
bb.pack(padx=10, pady=10)

Button(root, text='Open new window', command=lambda: new_win(cb)).pack()

root.mainloop()