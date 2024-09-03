import tkinter as tk

root = tk.Tk()

title_lbl = tk.Label(root, text='Poopsa Title')
new_lb = tk.Listbox(root)
a_btn = tk.Button(root, text='Clicka Me')
lb_scrollbar = tk.Scrollbar(root)

title_lbl.grid(row=0, columnspan=2)
new_lb.grid(row=1, column=0)
lb_scrollbar.grid(row=1, column=1, sticky='ns')
a_btn.grid(row=1, column=2)

for values in range(100):
    new_lb.insert('end', values)

new_lb.config(yscrollcommand=lb_scrollbar.set)
lb_scrollbar.config(command=new_lb.yview)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()