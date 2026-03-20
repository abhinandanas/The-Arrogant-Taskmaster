import customtkinter as ctk
import tkinter as tk
import math

class AnalogMeter(ctk.CTkFrame):
    def __init__(self, master, size=100, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.size = size
        
        # Determine canvas size (width=size, height=size/2 + some padding for text)
        canvas_width = size
        canvas_height = int(size / 2) + 20
        
        self.canvas = ctk.CTkCanvas(self, width=canvas_width, height=canvas_height, 
                                    bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Draw background arc
        # bounding box: (margin, margin, width-margin, width-margin) 
        # Since height is half width, the bottom of bbox is at canvas_width - margin
        self.margin = 10
        self.bbox_coords = (self.margin, self.margin, self.size - self.margin, self.size - self.margin)
        
        # Background track (gray)
        self.canvas.create_arc(*self.bbox_coords, start=0, extent=180, 
                               style=tk.ARC, outline="#444444", width=12)
        
        # Foreground track (starts empty)
        self.fg_arc = self.canvas.create_arc(*self.bbox_coords, start=180, extent=0, 
                                             style=tk.ARC, outline="green", width=12)
                                             
        # Text label for percentage
        self.text_id = self.canvas.create_text(canvas_width / 2, canvas_height - 10, 
                                               text="0%", fill="white", font=("Helvetica", 14, "bold"))
        
    def set_pressure(self, value): # value between 0.0 and 1.0
        # Validate value
        value = max(0.0, min(1.0, value))
        
        # Calculate extent (negative to draw clockwise from 180)
        extent = -int(value * 180)
        
        # Determine color
        if value <= 0.3:
            color = "#00cc00" # green
        elif value <= 0.7:
            color = "#ff9900" # orange
        else:
            color = "#ff3333" # red
            
        # Update canvas
        self.canvas.itemconfig(self.fg_arc, extent=extent, outline=color)
        self.canvas.itemconfig(self.text_id, text=f"{int(value * 100)}%")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("300x200")
    m = AnalogMeter(app, size=120)
    m.pack(pady=20)
    
    # Test animation
    val = 0.0
    def update():
        global val
        val += 0.05
        if val > 1.0: val = 0.0
        m.set_pressure(val)
        app.after(500, update)
        
    app.after(500, update)
    app.mainloop()
