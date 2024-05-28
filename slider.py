import tkinter as tk

# Function to decrement the slider value
def decrement_slider():
    current_value = slider.get()
    if current_value > 0:
        slider.set(current_value - 1)
        # Call this function again after 100 milliseconds
        root.after(100, decrement_slider)

# Function to start the timer when the slider value changes
def on_slider_change(value):
    # Start decrementing the slider
    root.after(100, decrement_slider)

# Create the main Tkinter window
root = tk.Tk()
root.title("Slider Timer Example")

# Create a Tkinter Scale widget
slider = tk.Scale(root, from_=100, to=0, orient=tk.HORIZONTAL)
slider.pack(pady=20)

# Bind the slider change event to the on_slider_change function
slider.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider.get()))

# Run the Tkinter event loop
root.mainloop()
