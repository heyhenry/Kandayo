import tkinter as tk
from PIL import Image, ImageTk

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Button with JPEG Image Example")
    root.geometry('400x400')  # Set the window size

    try:
        # Load the JPEG image using Pillow
        image_path = 'gc.png'
        image = Image.open(image_path)
        
        # Resize the image using Image.LANCZOS
        max_width, max_height = 300, 300  # Maximum dimensions
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        
        photo_image = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image: {e}")
        return  # Exit if there's an error loading the image

    # Create the button with the image
    image_button = tk.Button(root, image=photo_image, borderwidth=0, relief='flat')
    image_button.pack(padx=20, pady=20)  # Adjust padding as needed

    # Keep a reference to the image
    image_button.image = photo_image

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()



