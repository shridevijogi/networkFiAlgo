
import turtle
import pyttsx3
import tkinter as tk
from tkinter import messagebox

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Create the main window
window = tk.Tk()
window.title("Checksum Simulation")
window.configure(bg="light yellow")



# Create the turtle graphics canvas
canvas = turtle.ScrolledCanvas(window, width=1000, height=800)
canvas.pack(side=tk.LEFT)

# Create the turtle graphics screen
screen = turtle.TurtleScreen(canvas)
screen.bgcolor("light pink")

# Create the turtle graphics turtle
t = turtle.RawTurtle(screen)

def simulate():
    # Retrieve values from input fields
    message1 = message1_entry.get()
    message2 = message2_entry.get()

    # Validate user input
    if not message1 or not message2:
        messagebox.showerror("Error", "Please enter valid bits for both binary messages.")
        return

    def validate_input(input_str):
        for char in input_str:
            if char not in ('0', '1'):
                return False
        return True

    if not validate_input(message1) or not validate_input(message2):
        messagebox.showerror("Error", "Please enter valid bits (0s and 1s) for both binary messages.")
        return

    # Convert input strings to lists of integers
    binary_message1 = [int(x) for x in message1]
    binary_message2 = [int(x) for x in message2]

    # Validate user input
    def validate_input(input_str):
        for char in input_str:
            if char not in ('0', '1'):
                return False
        return True

    # Convert input strings to lists of integers
    if validate_input(message1) and validate_input(message2):
        binary_message1 = [int(x) for x in message1]
        binary_message2 = [int(x) for x in message2]

        # Calculate the length of the messages
        n = len(binary_message1)

        # Set up Turtle graphics
        t.reset()
        t.speed(1)#adjust the tracer value to control the animation speed

        # Write the note explaining the checksum calculation
       
        t.penup()
        t.goto(-500, 180)
        t.pendown()
        t.color("brown")
        t.write("Checksum value is calculated by making the one's complement \n"
                "of the results obtained by XOR operation of the given input message.",
                align="left", font=("arial", 16, "italic"))
        t.color("black")
        engine.say("Checksum value is calculated by making the one's complement of the results obtained by XOR operation of the given input message.")
        engine.runAndWait()


       
        # Draw binary messages on the screen
        for i in range(n):
            t.penup()
            t.goto(i * 50, 10)
            t.pendown()
            t.write(str(binary_message1[i]), align="center", font=("Arial", 12, "normal"))
            t.penup()
            t.goto(i * 50, -50)
            t.pendown()
            t.write(str(binary_message2[i]), align="center", font=("Arial", 12, "normal"))

        #enable screen updates
        screen.update  
           
        # Initialize the result box
        result_box = [0] * n

        # Perform XOR operation on the messages and store results in the result box
        for i in range(n):
            result = binary_message1[i] ^ binary_message2[i]
            t.penup()
            t.goto(i * 50, -100)
            t.pendown()
            t.write(str(result), align="center", font=("Arial", 12, "normal"))
            result_box[i] = result

            # Draw a line after simulating message2
            t.penup()
            t.goto(i * 50, -80)
            t.pendown()
            t.forward(50)

            # Draw a line before the rectangular shape
            t.penup()
            t.goto(i * 50, -120)
            t.pendown()
            t.forward(50)

        # Draw a rectangular shape for the result
        t.penup()
        t.goto(0, -160)
        t.pendown()
        t.setheading(0)
        t.fillcolor("grey")
        t.begin_fill()
        t.forward(n * 50)
        t.right(90)
        t.forward(80)
        t.right(90)
        t.forward(n * 50)
        t.right(90)
        t.forward(80)
        t.right(90)
        t.end_fill()

                # Perform one's complement operation on the result message
        complement_message = []
        for i in range(len(result_box) - 1, -1, -1):
            complement = int(not result_box[i])
            t.penup()
            t.goto(i * 50 + 20, -190)
            t.pendown()
            t.write(str(complement), align="center", font=("Arial", 12, "normal"))
            complement_message.append(complement)

        # Calculate the bounding box manually
        box_x = 0
        box_y = -160
        box_width = n * 50
        box_height = 80

        # Get coordinates of rectangular box
        note_x = box_x - 280
        note_y = box_y - 20

        # Write the note "Checksum value of given input" inside box
        t.penup()
        t.goto(note_x, note_y)
        t.pendown()
        t.color("brown")
        t.write("Checksum value of given input", align="left", font=("Arial italic", 12, "normal"))
        t.color("black")
        engine.say("Checksum value of given input")
        engine.runAndWait()

       

    else:
        messagebox.showerror("Error", "Invalid input! Please enter only 0s and 1s.")

def set_focus():
    message1_entry.focus_set()

# Set focus to the first input field after a delay
window.after(100, set_focus)


# Create input fields
message1_label = tk.Label(window, text="Binary Message 1:",fg="blue")
message1_label.pack()

message1_entry = tk.Entry(window)
message1_entry.pack()

message2_label = tk.Label(window, text="Binary Message 2:",fg="blue")
message2_label.pack()

message2_entry = tk.Entry(window)
message2_entry.pack()

# Create simulation button
simulate_button = tk.Button(window, text="Simulate", command=simulate)
simulate_button.pack()

# Run the main window
window.mainloop()

