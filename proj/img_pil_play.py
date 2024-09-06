import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

cpb_img = Image.open('./img/Chaos_Pink_Bean.webp')

max_width, max_height = 300, 300
cpb_img.thumbnail((max_width, max_height))

cpb_img = ImageTk.PhotoImage(cpb_img)

image_btn = tk.Button(root, image=cpb_img, borderwidth=0, relief='flat')
image_btn.pack(padx=20, pady=20)

root.mainloop()