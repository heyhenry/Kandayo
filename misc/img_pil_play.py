# import tkinter as tk
# from PIL import Image, ImageTk

# root = tk.Tk()

# cpb_img = Image.open('./img/Chaos_Pink_Bean.webp')

# max_width, max_height = 300, 300
# cpb_img.thumbnail((max_width, max_height))

# cpb_img = ImageTk.PhotoImage(cpb_img)

# image_btn = tk.Button(root, image=cpb_img, borderwidth=0, relief='flat')
# image_btn.pack(padx=20, pady=20)

# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk

# root = tk.Tk()
# max_width, max_height = 300, 300

# cpb_img = Image.open('./img/Chaos_Pink_Bean.webp')
# cpb_img.thumbnail((max_width, max_height))
# cpb_img = ImageTk.PhotoImage(cpb_img)

# cpbb_img = Image.open('./img/Chaos_Pink_Bean.webp')
# cpbb_img.thumbnail((max_width, max_height))
# cpbb_img = ImageTk.PhotoImage(cpbb_img)

# image_btn = tk.Label(root, image=cpb_img)
# image_btn.grid(row=0, column=0)

# imageb_btn = tk.Label(root, image=cpbb_img)
# imageb_btn.grid(row=0, column=1)

# root.mainloop()

import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

def popup():

    pu_win = tk.Toplevel(root)
    
    cpb_img = Image.open('./img/Chaos_Pink_Bean.webp')

    max_width, max_height = 300, 300
    cpb_img.thumbnail((max_width, max_height))

    cpb_img = ImageTk.PhotoImage(cpb_img)

    image_btn = tk.Button(pu_win, image=cpb_img, borderwidth=0, relief='flat')
    image_btn.pack(padx=20, pady=20)

    hey = tk.Label(pu_win, text='Hey')
    hey.pack()

    image_btn.image = cpb_img

clickme = tk.Button(root, text='Click Me', command=popup)
clickme.pack()

root.mainloop()