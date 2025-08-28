import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import json
import os
from typing import Dict, Any, Tuple

class ColorSwatch(tk.Canvas):
    """A custom widget to display color swatches"""
    def __init__(self, parent, color_data, **kwargs):
        self.color_data = color_data
        # Calculate width based on text content
        width = self.calculate_width()
        super().__init__(parent, width=width, height=20, **kwargs)
        self.draw_swatch()
    
    def calculate_width(self):
        """Calculate the width needed for the text, based on HEX value"""
        r, g, b = self.color_data.get("R", 128), self.color_data.get("G", 128), self.color_data.get("B", 128)
        text = f"#{r:02x}{g:02x}{b:02x}"
        
        # Estimate width: 7 pixels per character + padding for borders
        return len(text) * 7 + 30
    
    def draw_swatch(self):
        """Draw the color swatch"""
        # Get RGB values
        if "Name" in self.color_data:
            # Convert named colors to RGB
            named_colors = {
                "DimGray": (105, 105, 105),
                "DarkGray": (169, 169, 169),
                "Gray": (128, 128, 128),
                "LightGray": (211, 211, 211),
                "White": (255, 255, 255),
                "Black": (0, 0, 0),
                "Red": (255, 0, 0),
                "Green": (0, 128, 0),
                "Blue": (0, 0, 255),
                "Yellow": (255, 255, 0),
                "Cyan": (0, 255, 255),
                "Magenta": (255, 0, 255)
            }
            r, g, b = named_colors.get(self.color_data["Name"], (128, 128, 128))
        elif all(key in self.color_data for key in ["R", "G", "B"]):
            r, g, b = self.color_data["R"], self.color_data["G"], self.color_data["B"]
        else:
            r, g, b = 128, 128, 128  # Default gray
        
        # Convert to hex color
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Get current width
        width = self.winfo_reqwidth()
        
        # Draw the color rectangle - ensure it stays within canvas bounds
        self.delete("all")
        # Use width-3 to account for the border width and ensure it's fully visible
        self.create_rectangle(2, 2, width-3, 18, fill=hex_color, outline="black", width=1)
        
        # Add text label
        if "Name" in self.color_data:
            text = self.color_data["Name"]
        else:
            text = hex_color
        
        # Choose text color based on background brightness
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = "black" if brightness > 128 else "white"
        
        # Center the text
        text_x = width // 2
        self.create_text(text_x, 10, text=text, fill=text_color, font=("Arial", 8))
    
    def update_color(self, color_data):
        """Update the color swatch with new color data"""
        self.color_data = color_data
        # Recalculate width and redraw
        new_width = self.calculate_width()
        self.configure(width=new_width)
        self.draw_swatch()

class ThemeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Theme Color Editor")
        self.root.geometry("600x600")
        
        # Load the theme data
        self.theme_data = self.load_theme()
        self.original_theme = self.load_theme()  # Keep original for comparison
        
        # Create the main interface
        self.create_widgets()
        
    def load_theme(self) -> Dict[str, Any]:
        """Load the theme from the JSON file"""
        try:
            with open('sample-theme.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "sample-theme.json not found!")
            return {"Name": "Default Theme", "Theme": {}}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in sample-theme.json!")
            return {"Name": "Default Theme", "Theme": {}}
    
    def create_widgets(self):
        """Create the main interface widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Theme Color Editor", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        # Theme name entry
        ttk.Label(main_frame, text="Theme Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar(value=self.theme_data.get("Name", "New Theme"))
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 15), pady=2)

        # Create treeview for controls and colors
        self.create_treeview(main_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Load Theme", command=self.load_theme_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Theme", command=self.export_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Original", command=self.reset_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
    def create_treeview(self, parent):
        """Create a custom list view for displaying controls and colors"""
        # Create frame for the list
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(list_frame, height=400)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel events for scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        
        # Grid layout - canvas takes available space, scrollbar takes minimal space
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Store references to color swatches
        self.color_swatches = {}
        
        # Populate the list
        self.populate_list()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows/Mac
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def populate_list(self):
        """Populate the list with control and color data"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.color_swatches.clear()
        
        # Create header row
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2, pady=(0, 5))
        header_frame.columnconfigure(1, weight=1)
        
        # Header labels
        control_header = ttk.Label(header_frame, text="Control", font=("Arial", 10, "bold"), width=40, anchor=tk.W)
        control_header.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        color_header = ttk.Label(header_frame, text="Color", font=("Arial", 10, "bold"), anchor=tk.W)
        color_header.grid(row=0, column=1, sticky=tk.W)
        
        # Add items from theme
        theme = self.theme_data.get("Theme", {})
        for i, (control_name, color_data) in enumerate(theme.items()):
            # Create row frame
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.grid(row=i+1, column=0, sticky=(tk.W, tk.E), padx=2, pady=1)
            row_frame.columnconfigure(1, weight=1)
            
            # Control name label
            control_label = ttk.Label(row_frame, text=control_name, width=40, anchor=tk.W)
            control_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            
            # Color swatch
            color_swatch = ColorSwatch(row_frame, color_data)
            color_swatch.grid(row=0, column=1, sticky=tk.W)
            
            # Bind click event to color swatch
            color_swatch.bind("<Button-1>", lambda e, name=control_name, swatch=color_swatch: self.edit_color(name, swatch))
            
            # Store reference
            self.color_swatches[control_name] = color_swatch
    
    def get_color_display(self, color_data: Dict[str, Any]) -> str:
        """Get a display string for the color"""
        if "Name" in color_data:
            return f"Named Color: {color_data['Name']}"
        elif all(key in color_data for key in ["R", "G", "B"]):
            r, g, b = color_data["R"], color_data["G"], color_data["B"]
            return f"RGB({r}, {g}, {b})"
        else:
            return "Invalid Color"
    
    def get_color_rgb(self, color_data: Dict[str, Any]) -> Tuple[int, int, int]:
        """Get RGB values from color data"""
        if "Name" in color_data:
            # Convert named colors to RGB (simplified mapping)
            named_colors = {
                "DimGray": (105, 105, 105),
                "DarkGray": (169, 169, 169),
                "Gray": (128, 128, 128),
                "LightGray": (211, 211, 211),
                "White": (255, 255, 255),
                "Black": (0, 0, 0),
                "Red": (255, 0, 0),
                "Green": (0, 128, 0),
                "Blue": (0, 0, 255),
                "Yellow": (255, 255, 0),
                "Cyan": (0, 255, 255),
                "Magenta": (255, 0, 255)
            }
            return named_colors.get(color_data["Name"], (128, 128, 128))
        elif all(key in color_data for key in ["R", "G", "B"]):
            return (color_data["R"], color_data["G"], color_data["B"])
        else:
            return (128, 128, 128)  # Default gray
    

    
    def edit_color(self, control_name: str, color_swatch: ColorSwatch):
        """Open color picker for the selected control"""
        current_color_data = self.theme_data["Theme"][control_name]
        
        # Convert current color to RGB for color picker
        initial_color = self.get_color_rgb(current_color_data)
        
        # Open color picker
        color = colorchooser.askcolor(
            color=initial_color,
            title=f"Choose color for {control_name}"
        )
        
        if color[0]:  # User didn't cancel
            r, g, b = [int(c) for c in color[0]]
            # Update the color data
            self.theme_data["Theme"][control_name] = {"R": r, "G": g, "B": b}
            
            # Update the color swatch
            color_swatch.update_color(self.theme_data["Theme"][control_name])
    
    def export_theme(self):
        """Export the current theme to a JSON file"""
        # Update the theme name
        self.theme_data["Name"] = self.name_var.get()
        
        # Ask user for file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".eot",
            filetypes=[("Theme files", "*.eot"), ("All files", "*.*")],
            title="Save Theme As"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.theme_data, f, indent=4)
                messagebox.showinfo("Success", f"Theme exported successfully to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export theme: {str(e)}")
    
    def load_theme_file(self):
        """Load a theme from an .eot file"""
        filename = filedialog.askopenfilename(
            defaultextension=".eot",
            filetypes=[("Theme files", "*.eot"), ("All files", "*.*")],
            title="Load Theme File"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    loaded_theme = json.load(f)
                
                # Validate the loaded theme structure
                if "Name" not in loaded_theme or "Theme" not in loaded_theme:
                    messagebox.showerror("Error", "Invalid theme file format. File must contain 'Name' and 'Theme' fields.")
                    return
                
                # Update the current theme data
                self.theme_data = loaded_theme
                self.name_var.set(self.theme_data.get("Name", "New Theme"))
                
                # Refresh the display
                self.populate_list()
                
                messagebox.showinfo("Success", f"Theme loaded successfully from {filename}")
                
            except FileNotFoundError:
                messagebox.showerror("Error", f"File not found: {filename}")
            except json.JSONDecodeError:
                messagebox.showerror("Error", f"Invalid JSON format in {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load theme: {str(e)}")
    
    def reset_theme(self):
        """Reset the theme to the original values"""
        if messagebox.askyesno("Reset Theme", "Are you sure you want to reset to the original theme?"):
            self.theme_data = self.load_theme()
            self.name_var.set(self.theme_data.get("Name", "New Theme"))
            self.populate_list()

def main():
    root = tk.Tk()
    app = ThemeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

