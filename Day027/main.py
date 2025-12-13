# Day 27: TKinter GUI and Advanced Function Arguments
# 100 Days of Code

import tkinter as tk
from tkinter import ttk

# =============================================================================
# PART 1: ADVANCED FUNCTION ARGUMENTS (*args and **kwargs)
# =============================================================================

print("="*60)
print("PART 1: ADVANCED FUNCTION ARGUMENTS")
print("="*60)

# 1. Functions with default arguments
def greet(name, greeting="Hello"):
    """Function with default parameter"""
    return f"{greeting}, {name}!"

print("Default arguments:")
print(greet("Alice"))  # Uses default greeting
print(greet("Bob", "Hi"))  # Custom greeting

# 2. *args - allows unlimited positional arguments
def add_numbers(*args):
    """Function that accepts any number of arguments"""
    print(f"Arguments received: {args}")
    return sum(args)

print("\n*args examples:")
print(f"add_numbers(1, 2): {add_numbers(1, 2)}")
print(f"add_numbers(1, 2, 3, 4, 5): {add_numbers(1, 2, 3, 4, 5)}")

# 3. **kwargs - allows unlimited keyword arguments
def create_profile(**kwargs):
    """Function that accepts any number of keyword arguments"""
    print(f"Profile created with: {kwargs}")
    profile = {}
    for key, value in kwargs.items():
        profile[key] = value
    return profile

print("\n**kwargs examples:")
profile1 = create_profile(name="Alice", age=25, city="New York")
profile2 = create_profile(name="Bob", occupation="Developer", hobby="Gaming")

# 4. Combining all types of arguments
def advanced_function(required_arg, default_arg="default", *args, **kwargs):
    """Function combining all argument types"""
    print(f"Required: {required_arg}")
    print(f"Default: {default_arg}")
    print(f"*args: {args}")
    print(f"**kwargs: {kwargs}")

print("\nCombined arguments:")
advanced_function("must_have", "custom", 1, 2, 3, extra="value", another="option")

# =============================================================================
# PART 2: TKINTER BASICS
# =============================================================================

print("\n" + "="*60)
print("PART 2: TKINTER GUI BASICS")
print("="*60)

class TKinterBasics:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Day 27: TKinter Basics")
        self.window.geometry("500x400")
        self.window.configure(bg="lightblue")
        
        # Counter for button clicks
        self.click_count = 0
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Title Label
        title_label = tk.Label(
            self.window,
            text="Welcome to TKinter!",
            font=("Arial", 16, "bold"),
            bg="lightblue",
            fg="darkblue"
        )
        title_label.pack(pady=10)
        
        # Information Label
        info_label = tk.Label(
            self.window,
            text="This demonstrates basic TKinter widgets",
            font=("Arial", 10),
            bg="lightblue"
        )
        info_label.pack(pady=5)
        
        # Entry widget for text input
        self.entry = tk.Entry(self.window, width=30, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.entry.insert(0, "Type something here...")
        
        # Button that responds to clicks
        self.click_button = tk.Button(
            self.window,
            text="Click Me!",
            command=self.button_clicked,
            bg="orange",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15
        )
        self.click_button.pack(pady=10)
        
        # Label to show button click results
        self.result_label = tk.Label(
            self.window,
            text="Click the button to see magic!",
            font=("Arial", 10),
            bg="lightblue",
            wraplength=400
        )
        self.result_label.pack(pady=10)
        
        # Another button to demonstrate entry interaction
        entry_button = tk.Button(
            self.window,
            text="Process Text",
            command=self.process_entry,
            bg="green",
            fg="white",
            font=("Arial", 10)
        )
        entry_button.pack(pady=5)
    
    def button_clicked(self):
        """Handle button click event"""
        self.click_count += 1
        
        # Using *args concept - different messages based on click count
        messages = [
            "First click! You're getting the hang of it!",
            "Second click! TKinter is fun, isn't it?",
            "Third click! You're becoming a GUI master!",
            "Multiple clicks! You really love clicking buttons!"
        ]
        
        if self.click_count <= len(messages) - 1:
            message = messages[self.click_count - 1]
        else:
            message = f"Click #{self.click_count}: {messages[-1]}"
        
        self.result_label.config(text=message)
        
        # Change button color based on clicks (using **kwargs concept)
        colors = {"bg": "red" if self.click_count % 2 == 0 else "orange"}
        self.click_button.config(**colors)
    
    def process_entry(self):
        """Process text from entry widget"""
        user_text = self.entry.get()
        
        # Demonstrate string manipulation
        processed_text = f"You entered: '{user_text}' (Length: {len(user_text)} characters)"
        self.result_label.config(text=processed_text)
        
        # Clear entry for next input
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Enter new text...")
    
    def run(self):
        """Start the GUI application"""
        print("Starting TKinter basics demo...")
        self.window.mainloop()

# =============================================================================
# PART 3: UNIT CONVERTER PROJECT
# =============================================================================

class UnitConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Unit Converter - Day 27 Project")
        self.window.geometry("400x300")
        self.window.configure(bg="white")
        
        # Conversion factors (using **kwargs concept for flexible conversions)
        self.conversions = {
            "miles_to_km": 1.60934,
            "km_to_miles": 0.621371,
            "gallons_to_liters": 3.78541,
            "liters_to_gallons": 0.264172,
            "pounds_to_kg": 0.453592,
            "kg_to_pounds": 2.20462
        }
        
        self.create_converter_widgets()
    
    def create_converter_widgets(self):
        """Create the unit converter interface"""
        
        # Title
        title = tk.Label(
            self.window,
            text="Unit Converter",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="darkgreen"
        )
        title.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.window, bg="white")
        input_frame.pack(pady=10)
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            width=15,
            font=("Arial", 14),
            justify="center"
        )
        self.input_entry.pack(side=tk.LEFT, padx=5)
        
        # Conversion type dropdown
        self.conversion_var = tk.StringVar()
        self.conversion_var.set("miles_to_km")
        
        conversion_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.conversion_var,
            values=list(self.conversions.keys()),
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        conversion_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calculate_btn = tk.Button(
            self.window,
            text="Calculate",
            command=self.convert_units,
            bg="darkgreen",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15
        )
        calculate_btn.pack(pady=20)
        
        # Result label
        self.result_label = tk.Label(
            self.window,
            text="Enter a value and click Calculate",
            font=("Arial", 12),
            bg="white",
            wraplength=350
        )
        self.result_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            self.window,
            text="Available conversions:\nmiles↔km, gallons↔liters, pounds↔kg",
            font=("Arial", 9),
            bg="white",
            fg="gray"
        )
        instructions.pack(pady=10)
    
    def convert_units(self, *args):  # Using *args for flexibility
        """Convert units based on selected conversion type"""
        try:
            # Get input value
            input_value = float(self.input_entry.get())
            conversion_type = self.conversion_var.get()
            
            # Get conversion factor
            factor = self.conversions[conversion_type]
            
            # Calculate result
            result = input_value * factor
            
            # Format result nicely
            from_unit, to_unit = self.get_unit_names(conversion_type)
            
            result_text = f"{input_value} {from_unit} = {result:.2f} {to_unit}"
            self.result_label.config(text=result_text, fg="darkgreen")
            
        except ValueError:
            self.result_label.config(
                text="Please enter a valid number",
                fg="red"
            )
        except Exception as e:
            self.result_label.config(
                text=f"Error: {str(e)}",
                fg="red"
            )
    
    def get_unit_names(self, conversion_type, **kwargs):  # Using **kwargs for future extensibility
        """Get human-readable unit names"""
        unit_mappings = {
            "miles_to_km": ("miles", "kilometers"),
            "km_to_miles": ("kilometers", "miles"),
            "gallons_to_liters": ("gallons", "liters"),
            "liters_to_gallons": ("liters", "gallons"),
            "pounds_to_kg": ("pounds", "kilograms"),
            "kg_to_pounds": ("kilograms", "pounds")
        }
        
        return unit_mappings.get(conversion_type, ("units", "units"))
    
    def run(self):
        """Start the unit converter"""
        print("Starting Unit Converter...")
        self.window.mainloop()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # GUI-based menu for selection
    def start_tkinter_basics():
        menu_window.destroy()
        demo = TKinterBasics()
        demo.run()

    def start_unit_converter():
        menu_window.destroy()
        converter = UnitConverter()
        converter.run()

    def start_both():
        menu_window.destroy()
        demo = TKinterBasics()
        demo.run()
        converter = UnitConverter()
        converter.run()

    menu_window = tk.Tk()
    menu_window.title("Day 27: Choose Demo")
    menu_window.geometry("350x250")
    menu_window.configure(bg="lightgray")

    label = tk.Label(menu_window, text="Day 27: TKinter GUI and Advanced Function Arguments", font=("Arial", 12, "bold"), bg="lightgray", wraplength=320)
    label.pack(pady=20)

    btn1 = tk.Button(menu_window, text="1. TKinter Basics Demo", command=start_tkinter_basics, width=25, bg="skyblue", font=("Arial", 11))
    btn1.pack(pady=8)

    btn2 = tk.Button(menu_window, text="2. Unit Converter Project", command=start_unit_converter, width=25, bg="lightgreen", font=("Arial", 11))
    btn2.pack(pady=8)

    btn3 = tk.Button(menu_window, text="3. Both (one after another)", command=start_both, width=25, bg="orange", font=("Arial", 11))
    btn3.pack(pady=8)

    menu_window.mainloop()