import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Scrollable Canvas with Frames")

# Create a frame to hold the canvas and scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Create a canvas inside the main frame
canvas = tk.Canvas(main_frame, height=400, width=400)
canvas.pack(side="left", fill="both", expand=True)

# Create a vertical scrollbar and link it to the canvas
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create an inner frame inside the canvas
inner_frame = tk.Frame(canvas)
inner_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Function to update the scroll region when inner_frame changes size
def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the update function to inner_frame resizing
inner_frame.bind("<Configure>", update_scroll_region)

# Add multiple frames inside the inner_frame
for i in range(20):  # Example: Creating 20 frames
    frame = tk.Frame(inner_frame, bg="lightblue", height=50, width=380)
    label = tk.Label(frame, text=f"Frame {i+1}")
    label.pack(pady=10)
    frame.pack(pady=5, padx=10)

# Start the Tkinter main loop
root.mainloop()
