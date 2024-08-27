import tkinter as tk

root = tk.Tk()
root.title('Main Window')

def open_popup():
    
    def popup_close():
        top.destroy()
    
    top = tk.Toplevel(root)
    top.title('Pop-Up Window')
    popup_lbl = tk.Label(top, text='Poop')
    popup_lbl.pack()
    popup_close_btn = tk.Button(top, text='Close Pop-Up', command=popup_close)
    popup_close_btn.pack()


popup_btn = tk.Button(root, text='Open Pop-Up', command=open_popup)
popup_btn.pack()

root.mainloop()