
import turtle
import tkinter as tk
from tkinter import messagebox
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to draw a block with specified width and height
def draw_block(width, height):
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)
    turtle.end_fill()

# Function to draw a single bit with specified value (0 or 1)
def draw_bit(bit, position, is_error=False, is_last_error=False):
    turtle.pendown()
    if is_error:
        if is_last_error:
            turtle.fillcolor("red")  # Highlight last error position in red
        else:
            turtle.fillcolor("blue")  # Highlight other error positions in blue
        turtle.begin_fill()
    elif bit == 1:
        turtle.fillcolor("black")
    else:
        turtle.fillcolor("white")
    draw_block(40, 40)
    turtle.penup()
    turtle.forward(50)
    turtle.goto(turtle.xcor() - 25, turtle.ycor() + 50)  # Position the label above the block
    turtle.write(f"{position}", align="center", font=("Arial", 12, "bold"))
    turtle.goto(turtle.xcor() + 25, turtle.ycor() - 50)  # Reset turtle position
    turtle.pendown()
    if is_error:
        turtle.end_fill()

# Function to simulate/visualize the Hamming code
def simulate_hamming_code():
    received_code = entry.get()

    if not received_code:
        # Display an error message if the entry label is empty
        messagebox.showerror("Error", "Binary string can't be empty.")
        return

    if not all(bit in ('0', '1') for bit in received_code) or len(received_code) != 7:
        # Display an error message if the input is not a valid binary string of length 7
        messagebox.showerror("Error", "Enter a valid 7-bit binary string (0s and 1s only).")
        return
    received_code = [int(bit) for bit in entry.get()]

   


    turtle.speed(12)
    turtle.penup()
    turtle.goto(-380, 0)

    # Display the explanation of black and white color representation
    turtle.write("1 - Black\n0 - White", align="right", font=("Arial", 12, "italic"))

    turtle.goto(-350, 0)

    for index, bit in enumerate(received_code):
        draw_bit(bit, index + 1)

    turtle.goto(-350, -100)

    # Calculate the intermediate bits
    i1 = received_code[0] ^ received_code[2] ^ received_code[4] ^ received_code[6]
    i2 = received_code[1] ^ received_code[2] ^ received_code[5] ^ received_code[6]
    i3 = received_code[3] ^ received_code[4] ^ received_code[5] ^ received_code[6]

    # Check for errors in intermediate bits
    error_i1 = bin(i1).count('1') % 2 == 1
    error_i2 = bin(i2).count('1') % 2 == 1
    error_i3 = bin(i3).count('1') % 2 == 1

    # Draw the intermediate bits with error highlighting
    draw_bit(i1, "p1=" + str(i1), is_error=error_i1)
    draw_bit(i2, "p2=" + str(i2), is_error=error_i2)
    draw_bit(received_code[2], "d3")
    draw_bit(i3, "p4=" + str(i3), is_error=error_i3)
    draw_bit(received_code[4], "d5")
    draw_bit(received_code[5], "d6")
    draw_bit(received_code[6], "d7")

    turtle.goto(-350, -200)

    # Calculate the error bit index based on the parity bits
    error_bit_index = i1 * 2 ** 0 + i2 * 2 ** 1 + i3 * 2 ** 2

    # Draw the last row of blocks, highlighting the error bit index
    turtle.penup()
    for i in range(1, 8):
        turtle.pendown()
        if i == error_bit_index:
            draw_bit(received_code[i - 1], "d" + str(i), is_error=True, is_last_error=True)
        else:
            draw_bit(received_code[i - 1], "d" + str(i), is_error=(i == error_bit_index), is_last_error=False)
    turtle.penup()

    turtle.goto(-200, -270)

    # Display the received code in the note
    # turtle.write(f"Received Code: {''.join(map(str, received_code))}", align="center", font=("Arial", 12, "bold"))

    # Display the error bit index in the GUI
    turtle.color("teal")
    if error_bit_index == 0:
        turtle.write("Note: No error in received code", align="center", font=("Times New Roman", 14, "italic"))
        engine.say("No error in recieved code")
        engine.runAndWait()

        # Display the parity bit calculations
        turtle.goto(30, 280)
        turtle.write("Note: Detecting error in parity bits (1 means error exists, 0 means no error)", align="left",
                 font=("Times New Roman", 13, "italic"))
        turtle.goto(40, 250)
        engine.say("Detecting error in parity bits (1 means error exists, 0 means no error")
        engine.runAndWait()

        # Display the received code in the note
        received_code_text = "Received Code: {}".format(''.join(map(str, received_code)))
        turtle.write(received_code_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 220)
        engine.say(received_code_text)
        engine.runAndWait()

        
         # Display the calculations of P1, P2, and P4 with their actual values
        p1_text = "P1 = {} ⊕ {} ⊕ {} ⊕ {} = {}".format(received_code[0], received_code[2], received_code[4], received_code[6], i1)
        turtle.write(p1_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 190)
        engine.say("P1 = {} xor {} xor {} xor {} = {}".format(received_code[0], received_code[2], received_code[4], received_code[6], i1))
        engine.runAndWait()

        p2_text = "P2 = {} ⊕ {} ⊕ {} ⊕ {} = {}".format(received_code[1], received_code[2], received_code[5], received_code[6], i2)
        turtle.write(p2_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 160)
        engine.say("P2 = {} xor {} xor {} xor {} = {}".format(received_code[1], received_code[2], received_code[5], received_code[6], i2))
        engine.runAndWait()

        p4_text = "P4 = {} ⊕ {} ⊕ {} ⊕ {} = {}".format(received_code[3], received_code[4], received_code[5], received_code[6], i3)
        turtle.write(p4_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 130)
        engine.say("P4 = {} xor {} xor {} xor {} = {}".format(received_code[3], received_code[4], received_code[5], received_code[6], i3))
        engine.runAndWait()

        
    else:
        # Display the error bit index in the Tkinter window
        error_bit_index_text = "Error bit index: {}".format(error_bit_index)
        turtle.write(error_bit_index_text, align="center", font=("Times New Roman", 14, "italic"))
        engine.say(error_bit_index_text)
        engine.runAndWait()

        # Display the note about detecting errors
        turtle.goto(40, -90)
        turtle.color("teal")
        turtle.write("Note: The blue colored blocks represent errors in parity bits", align="left", font=("Times New Roman", 14, "italic"))
        engine.say("The blue colored blocks represent errors in parity bits ")
        engine.runAndWait()


        # Display the note about error in received code representation
        turtle.goto(40, -190)
        turtle.write("Note: The red colored block represents an error in the received code", align="left",
                     font=("Times New Roman", 14, "italic"))
        engine.say("The red colored block represents an error in the received code")
        engine.runAndWait()

        # Calculate the error in the received code using XOR operation
       
        corrected_code = received_code.copy()
        corrected_code[error_bit_index - 1] = 1 - corrected_code[error_bit_index - 1]

        # Calculate the error in the received code using XOR operation
       
        corrected_code = received_code.copy()
        corrected_code[error_bit_index - 1] = 1 - corrected_code[error_bit_index - 1]



        # Display the parity bit calculations
        turtle.goto(30, 280)
        turtle.write("Note: Detecting error in parity bits (1 means error exists, 0 means no error)", align="left",
                 font=("Times New Roman", 13, "italic"))
        turtle.goto(40, 250)
        engine.say("Detecting error in parity bits (1 means error exists, 0 means no error")
        engine.runAndWait()

        # Display the received code in the note
        received_code_text = "Received Code: {}".format(''.join(map(str, received_code)))
        turtle.write(received_code_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 220)
        engine.say(received_code_text)
        engine.runAndWait()


        # Display the calculations of P1, P2, and P4 with their actual values
        p1_text = "P1 = {} ⊕ {} ⊕ {} ⊕ {} = {}".format(received_code[0], received_code[2], received_code[4], received_code[6], i1)
        turtle.write(p1_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 190)
        engine.say("P1 = {} xor {} xor {} xor {} = {}".format(received_code[0], received_code[2], received_code[4], received_code[6], i1))
        engine.runAndWait()

        p2_text = "P2 = {} ⊕ {} ⊕ {} ⊕ {} = {}".format(received_code[1], received_code[2], received_code[5], received_code[6], i2)
        turtle.write(p2_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 160)
        engine.say("P2 = {} xor {} xor {} xor {} = {}".format(received_code[1], received_code[2], received_code[5], received_code[6], i2))
        engine.runAndWait()

        p4_text = "P4 = {} ⊕ {} ⊕ {} ⊕ {} = {}".format(received_code[3], received_code[4], received_code[5], received_code[6], i3)
        turtle.write(p4_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 130)
        engine.say("P4 = {} xor {} xor {} xor {} = {}".format(received_code[3], received_code[4], received_code[5], received_code[6], i3))
        engine.runAndWait()



        # Display the calculation of error bit index with its actual value
        error_bit_index_text = "Error bit index = {} * 2 ** 0 + {} * 2 ** 1 + {} * 2 ** 2 = {}".format(i1, i2, i3, error_bit_index)
        turtle.write(error_bit_index_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 70)
        engine.say(error_bit_index_text)
        engine.runAndWait()

        # Display the corrected code with its actual value
        corrected_code_text = "Corrected Code: {}".format(''.join(map(str, corrected_code)))
        turtle.write(corrected_code_text, align="left", font=("Times New Roman", 14, "italic"))
        turtle.goto(40, 40)
        engine.say(corrected_code_text)
        engine.runAndWait()

        
        turtle.write("Error Corrected!", align="left", font=("Times New Roman", 14, "italic"))
        engine.say("Error Corrected!")
        engine.runAndWait()

    


    root.mainloop()

# Create the main frame
root=tk.Tk()
frame = tk.Frame(root)
frame.pack()
frame.configure(background="mint cream")
# Create the left section for the GUI
gui_frame = tk.Frame(frame)
gui_frame.pack(side=tk.LEFT)
gui_frame.configure(background="mint cream")


# Create a label and an entry field for the user input
label = tk.Label(gui_frame, text="Enter the received 7-bit Hamming code:", font=("Times New Roman", 12, "italic"), fg="teal" , bg="mint cream")
label.pack()
entry = tk.Entry(gui_frame)
entry.pack()
entry.focus_set()  # Set initial focus to the entry widget


# Create a button to start the simulation
button = tk.Button(gui_frame, text="Simulate", font=("Times New Roman", 13, "italic"), fg="teal", bg="mint cream", command=simulate_hamming_code)
button.pack()

# Create the right section for the turtle graphics
canvas = tk.Canvas(frame, width=1150, height=700)
canvas.pack(side=tk.RIGHT)

# Create a turtle screen for drawing
screen = turtle.TurtleScreen(canvas)
screen.bgcolor("white")

# Create a turtle for drawing
turtle = turtle.RawTurtle(screen)
turtle.speed(10)

# Start the main event loop
root.mainloop()
