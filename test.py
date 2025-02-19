import tkinter as tk

class HoverPopup:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.popup = None

        # Bind events to show/hide tooltip
        widget.bind("<Enter>", self.show_popup)
        widget.bind("<Leave>", self.hide_popup)

    def show_popup(self, event):
        """Create a popup when mouse enters the widget."""
        if self.popup:
            return  # Prevent multiple popups

        # Create the popup window
        self.popup = tk.Toplevel(self.widget)
        self.popup.wm_overrideredirect(True)  # Remove window decorations

        # Position the popup near the cursor
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.popup.wm_geometry(f"+{x}+{y}")

        # Add text label to popup
        label = tk.Label(self.popup, text=self.text, bg="yellow", relief="solid", borderwidth=1, padx=5, pady=2)
        label.pack()

    def hide_popup(self, event):
        """Destroy the popup when the mouse leaves the widget."""
        if self.popup:
            self.popup.destroy()
            self.popup = None

# Create the main application window
root = tk.Tk()
root.title("Hover Popup Example")

# Create a label
label = tk.Label(root, text="Hover over me", font=("Arial", 14), fg="blue")
label.pack(pady=20)

# Attach popup tooltip to the label
HoverPopup(label, "This is a tooltip!")

# Run the Tkinter event loop
root.mainloop()