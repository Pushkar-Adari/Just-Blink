import numpy as np
import matplotlib.pyplot as plt

# Set the figure size to 800x600 pixels
fig = plt.figure(figsize=(8, 6), dpi=100)  # size in inches and dpi to achieve 800x600 pixels
ax = fig.add_subplot(111)

# Create a bar chart
x = np.arange(5)
y = np.random.random(5)
bars = ax.bar(x, y)

# Print the axis limits and dimensions
print(f"Axis limits: xlim={ax.get_xlim()}, ylim={ax.get_ylim()}")
print(f"Figure dimensions: width={fig.get_figwidth()*fig.dpi}px, height={fig.get_figheight()*fig.dpi}px")

# Initialize lists to hold the pixel coordinates of bar vertices
pixel_coords = []

# Get the pixel coordinates of each bar's vertices
for bar in bars:
    # Get the vertices of the bar
    vertices = bar.get_bbox().get_points()
    
    # Transform the data coordinates to pixel coordinates
    pixels = ax.transData.transform(vertices)
    pixel_coords.append(pixels)

# Adjust the y coordinates to match the pixel coordinate system
width, height = fig.canvas.get_width_height()
for pixels in pixel_coords:
    pixels[:, 1] = height - pixels[:, 1]

# Print and label the pixel coordinates of the bar vertices
print("Pixel coordinates:")
for i, pixels in enumerate(pixel_coords):
    print(f"Bar {i}:")
    for xp, yp in pixels:
        print(f'({xp:.2f}, {yp:.2f})')
    
    # Calculate the bar's width and height in data coordinates
    x0, y0 = bars[i].get_xy()
    w = bars[i].get_width()
    h = bars[i].get_height()
    
    # Label the bar with its x, y, width, and height
    ax.text(x0 + w/2, y0 + h/2, f'x={x0:.2f}\ny={y0:.2f}\nw={w:.2f}\nh={h:.2f}',
            ha='center', va='center', fontsize=8, color='black', bbox=dict(facecolor='white', alpha=0.5))

plt.show()
