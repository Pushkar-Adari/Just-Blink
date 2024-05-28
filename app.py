from customtkinter import *
from PIL import Image
app = CTk()
app.geometry("600x400")
img = Image.open("assets/view.png")
btn = CTkButton(master=app,width=200,height=32, text="Start Tracking", corner_radius=5, image=CTkImage(dark_image=img,light_image=img))
btn.place(relx=0.8,rely=0.3,anchor="center" )
app.mainloop()
