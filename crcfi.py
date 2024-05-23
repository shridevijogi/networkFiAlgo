import turtle
import tkinter as tk

def calculate_crc():
    """
    Calculates the CRC of a message using bitwise XOR operations.

    :return: binary CRC as a list of bits
    """
    bit = [int(x) for x in bit_entry.get()]
    poly = [int(x) for x in poly_entry.get()]

    x = 0
    y = 100
    x1 = 0
    y1 = 70
    y2 = 0
    x2 = 20
    # Append zeros to the message equal to the degree of the polynomial
    message = bit + [0] * (len(poly) - 1)
    for i in range(len(message)):
        turtle.penup()
        turtle.goto(x + i * 20, y)
        turtle.pendown()
        turtle.write(message[i], font=("Arial", 16, "normal"))
    for i in range(len(poly)):
        turtle.penup()
        turtle.goto(x1 + i * 20, y1)
        turtle.pendown()
        turtle.write(poly[i], font=("Arial", 16, "normal"))

    # Perform bitwise XOR of the message with the polynomial
    for i in range(len(message) - len(poly) + 1):
        y1 += -50
        y2 += -50

        if message[i]:
            for j in range(1, len(poly)):  # Ignore the first bit of the polynomial
                message[i + j] ^= poly[j]
                print(message[i+j])
                turtle.penup()
                turtle.goto(x1 + i * 20, y1)
                turtle.pendown()
                turtle.write(message[i + j], font=("Arial", 16, "normal"))

                x1 += 20
                turtle.goto(x2 + i * 20, y2)
                turtle.pendown()
                turtle.write(poly[j], font=("Arial", 16, "normal"))
                x2 += 20

    # Return the CRC as the remainder of the final message
    crc_result = message[-len(poly) + 1:]
    crc_output.config(state='normal')
    crc_output.delete(1.0, tk.END)
    crc_output.insert(tk.END, "".join([str(x) for x in crc_result]))
    crc_output.config(state='disabled')

    # Display the original message in the message_output text box
    original_message = bit_entry.get()
    message_output.config(state='normal')
    message_output.delete(1.0, tk.END)
    message_output.insert(tk.END, original_message)
    message_output.config(state='disabled')

    # Append the CRC to the original message
    message_with_crc = original_message + "".join([str(x) for x in crc_result])

    # Display the updated message in the message_with_crc_output text box
    message_with_crc_output.config(state='normal')
    message_with_crc_output.delete(1.0, tk.END)
    message_with_crc_output.insert(tk.END, message_with_crc)
    message_with_crc_output.config(state='disabled')


# Create a GUI window
root = tk.Tk()
root.title("CRC Calculator")
root.configure(bg='teal')

# Add bit input textbox and label
bit_label = tk.Label(root, text="Enter binary bit value:")
bit_label.grid(row=0, column=0)
bit_entry = tk.Entry(root)
bit_entry.grid(row=0, column=1)

# Add polynomial input textbox and label
poly_label = tk.Label(root, text="Enter polynomial:")
poly_label.grid(row=1, column=0)
poly_entry = tk.Entry(root)
poly_entry.grid(row=1, column=1)

# Add button to start CRC algorithm
calculate_button = tk.Button(root, text="Calculate CRC", command=calculate_crc)
calculate_button.grid(row=2, column=0, columnspan=2)

# Add output textbox and label for CRC value
crc_label = tk.Label(root, text="CRC:")
crc_label.grid(row=3, column=0)
crc_output = tk.Text(root, width=30, height=1, state='disabled')
crc_output.grid(row=3, column=1)

# Add output textbox and label for original message
original_message_label = tk.Label(root, text="Original Message:")
original_message_label.grid(row=4, column=0)
message_output = tk.Text(root, width=30, height=1, state='disabled')
message_output.grid(row=4, column=1)

# Add output textbox and label for message with CRC value added
message_with_crc_label = tk.Label(root, text="Message with CRC value added:")
message_with_crc_label.grid(row=5, column=0)
message_with_crc_output = tk.Text(root, width=30, height=1, state='disabled')
message_with_crc_output.grid(row=5, column=1)

root.mainloop()
