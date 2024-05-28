from PIL import Image, ImageTk
import tkinter as tk

class CustomTkinterButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.image = kwargs.pop("image", None)
        super().__init__(master, **kwargs)
        if self.image:
            self.configure(image=self.image, compound="center")

if __name__ == "__main__":
    root = tk.Tk()

    # Open the image with PIL
    with Image.open("assets/scar.jpg") as img:
        # Convert the image to a format that Tkinter can use
        image = ImageTk.PhotoImage(img)

    # Create a button with the background image
    button = CustomTkinterButton(root, text="Click me", image=image)
    button.pack()

    root.mainloop()
