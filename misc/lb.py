import tkinter as tk

class CustomScrollbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create a canvas to draw the scrollbar
        self.canvas = tk.Canvas(self, width=20, bg='lightgrey')
        self.canvas.pack(side='right', fill='y')

        # Create the scrollbar thumb
        self.thumb = self.canvas.create_rectangle(0, 0, 20, 50, fill='lightblue', outline='')

        # Configure scrollbar
        self.canvas.bind('<Button-1>', self.start_scroll)
        self.canvas.bind('<B1-Motion>', self.scroll)

        # Track the scrollbar's movement
        self.scroll_start_y = 0
        self.scroll_start_thumb_y = 0

    def start_scroll(self, event):
        self.scroll_start_y = event.y
        self.scroll_start_thumb_y = self.canvas.coords(self.thumb)[1]

    def scroll(self, event):
        delta_y = event.y - self.scroll_start_y
        new_thumb_y = self.scroll_start_thumb_y + delta_y
        thumb_coords = self.canvas.coords(self.thumb)
        # Ensure thumb stays within canvas
        if 0 <= new_thumb_y <= self.canvas.winfo_height() - thumb_coords[3] + thumb_coords[1]:
            self.canvas.coords(self.thumb, thumb_coords[0], new_thumb_y, thumb_coords[2], new_thumb_y + thumb_coords[3] - thumb_coords[1])

class App:
    def __init__(self, root):
        self.root = root

        # Create a frame to hold the Listbox and scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a Listbox
        self.chars_lb = tk.Listbox(self.frame, height=30)
        self.chars_lb.pack(side='left', fill='both', expand=True)

        # Create a custom scrollbar
        self.scrollbar = CustomScrollbar(self.frame)
        self.scrollbar.pack(side='right', fill='y')

        # Add items to Listbox
        for i in range(50):
            self.chars_lb.insert(tk.END, f"Item {i}")

        # Adjust scrollbar thumb size based on Listbox height
        self.update_scrollbar()

    def update_scrollbar(self):
        listbox_height = self.chars_lb.winfo_height()
        thumb_height = int(listbox_height * 0.5)  # Example thumb height
        self.scrollbar.canvas.config(scrollregion=(0, 0, 20, listbox_height))
        self.scrollbar.canvas.coords(self.scrollbar.thumb, 0, 0, 20, thumb_height)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()




