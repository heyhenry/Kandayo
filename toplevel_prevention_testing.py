import tkinter as tk    

current_toplevel = None

root = tk.Tk()
root.geometry('400x400')

def first_popup():
    global current_toplevel
    if current_toplevel is not None and current_toplevel.winfo_exists():
        print('window already exists')
    else:
        
        fp_win = tk.Toplevel(root)
        fp_win.geometry('300x300')
        current_toplevel = fp_win
        fp_win_lbl = tk.Label(fp_win, text='Fucking dumbdogs')
        fp_win_cancel = tk.Button(fp_win, text='Cancel', command=fp_win.destroy)

        fp_win_lbl.pack()
        fp_win_cancel.pack()

def second_popup():
    global current_toplevel
    if current_toplevel is not None and current_toplevel.winfo_exists():
        print('window already exists')
    else:
        sp_win = tk.Toplevel(root)
        sp_win.geometry('300x300')
        current_toplevel = sp_win
        sp_win_lbl = tk.Label(sp_win, text='fucking nutmuncher')
        sp_win_btn = tk.Button(sp_win, text='Cancel', command=sp_win.destroy)

        sp_win_lbl.pack()
        sp_win_btn.pack()

click_lbl = tk.Label(root, text='This is a button: ')
click_btn = tk.Button(root, text='Click Me!', command=first_popup)
sec_btn = tk.Button(root, text='Or Click Me!', command=second_popup)

click_lbl.grid(row=0, column=0)
click_btn.grid(row=0, column=1)
sec_btn.grid(row=1, columnspan=2)

root.mainloop()