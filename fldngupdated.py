import random
import math
import tkinter as tk
import turtle
from tkinter import messagebox

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)


# Define the network topology as a dictionary
network = {}

# Store the node positions globally
node_positions = {}

# Store the edge IDs globally
edge_ids = {}

# Flag to check if the topology is created
topology_created = False

# Set a random seed for consistent network structures
random.seed(42)


def create_network_topology(num_nodes):
    global network, node_positions, edge_ids, topology_created
    # Store the network topology, node positions, and edge IDs globally
    network = {}

    # Generate node labels
    nodes = [chr(ord('A') + i) for i in range(num_nodes)]

    # Create random connections between nodes
    for node in nodes:
        # Ensure each node is connected to at least one other node
        neighbors = set(nodes) - {node}
        num_neighbors = random.randint(1, num_nodes - 1)  # Randomly select the number of neighbors
        network[node] = random.sample(list(neighbors), num_neighbors)

    # Fixed positions for the nodes
    node_positions = {}
    angle = 360 / num_nodes
    radius = 200
    for i, node in enumerate(nodes):
        x = radius * math.cos(math.radians(i * angle))
        y = radius * math.sin(math.radians(i * angle))
        node_positions[node] = (x, y)

    turtle.clear()

    edge_ids = {}
    for node in network:
        turtle.penup()
        turtle.goto(*get_center(node_positions[node]))
        turtle.pendown()
        turtle.fillcolor('blue')
        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(20)
            turtle.right(90)
        turtle.end_fill()

        # Label the nodes with letters
        turtle.penup()
        turtle.goto(*get_center(node_positions[node]))
        turtle.pendown()
        turtle.write(node, align='center', font=('Arial', 12, 'normal'))

        for neighbor in network[node]:
            edge_ids[(node, neighbor)] = (node_positions[node], node_positions[neighbor])
            edge_ids[(neighbor, node)] = (node_positions[neighbor], node_positions[node])

            # Draw lines between nodes
            turtle.penup()
            turtle.goto(*get_center(node_positions[node]))
            turtle.pendown()
            turtle.color('black')
            turtle.speed(4)
            turtle.goto(*get_center(node_positions[neighbor]))
            turtle.speed(0)
            turtle.penup()  # Add this line to lift the pen after drawing the line
            turtle_screen.update()

    topology_created = True
    show_simulation_controls()


def get_center(position):
    if position:
        return position[0], position[1]
    else:
        return 0, 0


def create_topology_button_click():
    num_nodes = num_nodes_entry.get()
    if not num_nodes:
        messagebox.showerror("Error", "Number of nodes can't be empty.")
        return

    try:
        num_nodes = int(num_nodes)
    except ValueError:
        messagebox.showerror("Error", "Number of nodes must be a valid integer.")
        return

    create_network_topology(num_nodes)


def show_simulation_controls():
    # Clear the existing controls
    for widget in simulation_controls_frame.winfo_children():
        widget.pack_forget()

    num_nodes_label.pack(in_=simulation_controls_frame, pady=5)
    num_nodes_entry.pack(in_=simulation_controls_frame, pady=5)
    create_topology_button.pack(in_=simulation_controls_frame, pady=5)

    if topology_created:  # Show the controls only if the topology is created
        source_label.pack(in_=simulation_controls_frame, pady=5)
        source_entry.pack(in_=simulation_controls_frame, pady=5)
        data_label.pack(in_=simulation_controls_frame, pady=5)
        data_entry.pack(in_=simulation_controls_frame, pady=5)
        run_button.pack(in_=simulation_controls_frame, pady=5)

        # Set focus on the source entry box
        source_entry.focus_set()
    else:
        # Set focus on the num_nodes_entry box
        num_nodes_entry.focus_set()

    turtle_screen.update()



def highlight_path(src, dest):
    if (src, dest) in edge_ids:
        turtle.penup()
        turtle.color('red')
        turtle.speed(1)
        turtle.goto(*edge_ids[(src, dest)][0])
        turtle.pendown()
        turtle.goto(*edge_ids[(src, dest)][1])
        turtle.penup()  # Add this line to lift the pen after drawing the path
        turtle_screen.update()

        #calculate the midpoint of the path
        x_mid=(edge_ids[(src, dest)][0][0] + edge_ids[(src, dest)][1][0])/2

        y_mid=(edge_ids[(src, dest)][0][1] + edge_ids[(src, dest)][1][1])/2

        #access 'data' variable
        data = data_entry.get()

        #write the data as a label along with path
        turtle.goto(x_mid, y_mid)
        turtle.pendown()
        turtle.color('black')
        turtle.write(data, align='center', font=('Arial',10,'normal'))
        turtle.penup()
        turtle_screen.update()


def flooding(src, data):
    # Perform flooding simulation
    flooded_nodes = set()
    queue = [src]
    while queue:
        node = queue.pop(0)
        if node not in flooded_nodes:
            flooded_nodes.add(node)
            queue.extend(network[node])  # Access the globally stored network
    return flooded_nodes


# Define a function to handle the button click event
def run_simulation():
    global topology_created
    # Check if both the source node and data fields are filled in
    if not source_var.get():
        messagebox.showerror("Error", "Source node can't be empty.")
        return
    if not data_entry.get():
        messagebox.showerror("Error", "Data can't be empty.")
        return


    # Check if the source node is a capital letter
    source_node = source_var.get()
    if not source_node.isalpha() or not source_node.isupper():
        messagebox.showerror("Error", "Source node must be a capital letter.")
        return

    # Check if the data is a valid integer
    data = data_entry.get()
    try:
        int(data)
    except ValueError:
        messagebox.showerror("Error", "Data must be a valid integer.")
        return

    # Get the selected source node and data from the GUI
    src = source_var.get()
    data = data_entry.get()

    # Clear the canvas and create the network topology visualization if it hasn't been created already
    if not topology_created:
        turtle.clear()
        num_nodes = int(num_nodes_entry.get())
        create_network_topology(num_nodes)

    # Simulate the transmission of the data from the source node
    flooded_nodes = flooding(src, data)

    # Highlight the paths in red
    for node in flooded_nodes:
        if node != src:
            if (src, node) in edge_ids:
                highlight_path(src, node)

    # Set focus on the data entry box
    data_entry.focus_set()

    turtle_screen.update()


root = tk.Tk()
root.title("Flooding Routing Simulation")
root.geometry("900x800")  # Set the initial window size

# Allow both horizontal and vertical resizing
root.resizable(True, True)


# Custom styles
label_style = {'font': ('Times New Roman', 13, 'italic')}
entry_style = {'font': ('Times New Roman', 13, 'italic')}
button_style = {'font': ('Times New Roman', 13, 'italic')}

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

canvas_frame = tk.Frame(root)
canvas_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=8)


simulation_controls_frame = tk.Frame(root)
simulation_controls_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

simulation_controls_frame.configure(background="mint cream")

canvas = tk.Canvas(canvas_frame, width=1200, height=1000)
canvas.pack(side=tk.LEFT)

turtle_screen = turtle.TurtleScreen(canvas)
turtle_screen.bgcolor("light green")

window_width = 1200
window_height = 1000
turtle_screen.screensize(window_width, window_height)
turtle_screen.setworldcoordinates(-window_width / 2, -window_height / 2, window_width / 2, window_height / 2)

turtle = turtle.RawTurtle(turtle_screen)
turtle.speed(0)
turtle.hideturtle()

num_nodes_label = tk.Label(simulation_controls_frame, text="Enter number of nodes:", fg="teal", **label_style)

num_nodes_entry = tk.Entry(simulation_controls_frame, **entry_style)

create_topology_button = tk.Button(simulation_controls_frame, text="Create Network Topology", fg="teal",
                                   command=create_topology_button_click, **button_style)

source_var = tk.StringVar()
source_label = tk.Label(simulation_controls_frame, text="Source Node:", fg="teal", **label_style)

data_var = tk.StringVar()
data_label = tk.Label(simulation_controls_frame, text="Data:", fg="teal", **label_style)

source_entry = tk.Entry(simulation_controls_frame, textvariable=source_var, **entry_style)
data_entry = tk.Entry(simulation_controls_frame, textvariable=data_var, **entry_style)
run_button = tk.Button(simulation_controls_frame, text="Run Simulation", fg="teal", command=run_simulation,
                       **button_style)

show_simulation_controls()

root.mainloop()
