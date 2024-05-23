import turtle
import tkinter as tk
from tkinter import messagebox
import pyttsx3

def calculate_parity():
    binary_string = entry.get()

    if not binary_string:
        show_error_message("Please enter a binary string.")
        return

    if not all(bit in ('0', '1') for bit in binary_string):
        show_error_message("Binary string can only contain 0's and 1's.")
        return

    parity_bit = binary_string.count('1') % 2

    # Clear the screen
    turtle_screen.clear()

    # Calculate starting position for blocks
    num_bits = len(binary_string)
    block_size = 80
    total_width = num_bits * block_size
    x_start = -total_width / 2
    y = 0

    # Draw blocks
    for bit in binary_string:
        if bit == '1':
            color = 'green'
        else:
            color = 'red'
        draw_block(x_start, y, block_size, color, bit)
        x_start += block_size

    # Calculate position for parity bit
    x_parity = x_start + (block_size / 2)

    # Draw parity bit
    parity_label = "P=1" if parity_bit == 1 else "P=0"
    draw_block(x_parity, y, block_size, 'blue' if parity_bit == 1 else 'white', parity_label)

    # Add note to the turtle graphics
    note = "Note: If the number of 1's is odd, the parity bit is represented by a blue block labeled 'P=1'. Else, it is represented by a white block labeled 'P=0'."
    turtle.penup()
    turtle.goto(0, 200)
    turtle.pendown()
    turtle.color("teal") 
    turtle.write(note, align='center', font=('Arial', 11, 'italic'))

    # Generate audio for the note
    engine = pyttsx3.init()
    engine.say(note)
    engine.runAndWait()

def draw_block(x, y, size, color, label):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(x + size / 2, y + size + 10)
    turtle.pendown()
    turtle.write(label, align='center', font=('Arial', 12, 'normal'))
    
def show_error_message(message):
    messagebox.showerror("Error", message)
    entry.delete(0, tk.END)  # Clear the entry widget

# Create GUI window
window = tk.Tk()
window.title("Parity Bit Simulation")
window.geometry("800x400")
window.configure(bg="teal")

# Create frame for user input
input_frame = tk.Frame(window)
input_frame.pack(side=tk.LEFT, padx=10)

# Create label for binary string
label = tk.Label(input_frame, text="Enter binary string:", font=("Times New Roman", 14))
label.pack()

# Create entry for binary string
entry = tk.Entry(input_frame, font=("Times New Roman", 14))
entry.pack(pady=20)  # Add vertical padding of 10 pixels
entry.focus()

# Create button to calculate parity
button = tk.Button(input_frame, text="Calculate", command=calculate_parity, bg="teal", font=("Times New Roman", 14))
button.pack()

# Create turtle graphics window
turtle_frame = tk.Frame(window)
turtle_frame.pack(side=tk.RIGHT, padx=10)

# Initialize turtle graphics
turtle_canvas = tk.Canvas(turtle_frame, width=1000, height=800)
turtle_canvas.pack()

turtle_screen = turtle.TurtleScreen(turtle_canvas)
turtle_screen.bgcolor("white")

turtle = turtle.RawTurtle(turtle_screen)
turtle.speed(3)

# Run GUI
window.mainloop()
