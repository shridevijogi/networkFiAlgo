import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import ttk
import re
import pyttsx3


def calculate_spanning_tree(network_graph):
    # Perform MST calculations
    spanning_tree = nx.minimum_spanning_tree(network_graph)
    return spanning_tree


def create_network_topology(nodes, edges_with_weights):
    network_graph = nx.Graph()
    network_graph.add_nodes_from(nodes)
    for edge, weight in edges_with_weights:
        node1, node2 = edge
        network_graph.add_edge(node1, node2, weight=float(weight))
    return network_graph


def display_network_topology(network_graph, pos, spanning_tree=None):
    if spanning_tree:
        # Create a list of edges to be drawn as a circle
        circle_edges = []

        # Create a list of edges to be drawn as non-circle edges
        non_circle_edges = []

        # Iterate over edges and classify them based on the presence in the spanning tree
        for edge in network_graph.edges():
            if edge in spanning_tree.edges():
                circle_edges.append(edge)
            else:
                non_circle_edges.append(edge)

        # Draw the circle edges
        nx.draw_networkx_edges(network_graph, pos, edgelist=circle_edges, edge_color='gray', alpha=0.3)

        # Draw the non-circle edges
        nx.draw_networkx_edges(network_graph, pos, edgelist=non_circle_edges, edge_color='gray')

    else:
        # Draw all edges if no spanning tree is provided
        nx.draw_networkx_edges(network_graph, pos, edge_color='gray')

    nx.draw_networkx_nodes(network_graph, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(network_graph, pos)

    labels = nx.get_edge_attributes(network_graph, 'weight')
    nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=labels)


def create_output_screen(node_positions):
    global figure1, figure2, combined_figure, output_window, figure1_canvas, figure2_canvas

    # Create the output window
    output_window = tk.Toplevel(root)
    output_window.title("Output")
    output_window.configure(background = 'light green')

    # Set the dimensions and position of the output window to center it on the screen
    screen_width = output_window.winfo_screenwidth()
    screen_height = output_window.winfo_screenheight()
    window_width = 800  # Adjust the width as needed
    window_height = 600  # Adjust the height as needed
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    output_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a combined figure to hold both network topology and minimum spanning tree
    combined_figure = plt.figure(figsize=(10, 5))

    # Plot the network topology on the left side
    network_topology_ax = combined_figure.add_subplot(121)
    display_network_topology(network_topology, node_positions)
    network_topology_ax.set_title('Network Topology')

    # Plot the minimum spanning tree on the right side
    spanning_tree_ax = combined_figure.add_subplot(122)
    display_network_topology(spanning_tree, node_positions)
    spanning_tree_ax.set_title('Minimum Spanning Tree')

    # Create a canvas for the combined figure
    figure_canvas = FigureCanvasTkAgg(combined_figure, master=output_window)
    figure_canvas.get_tk_widget().pack()

    def speak_text(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


    # Add a note to the minimum spanning tree plot
    spanning_tree_ax.text(
        -0.1,
        -0.1,
        "Note: Minimum Spanning Tree calculated by placing the edges in the increasing order of weights,\nbut the path should not form a closed structure",
        horizontalalignment='center',
        verticalalignment='center',
        transform=spanning_tree_ax.transAxes,
        fontsize=10,
        color='teal',
        style='italic'
    )

    # Speak the note
    #speak_text("Note: Minimum Spanning Tree calculated by placing the edges in the increasing order of weights, but the path should not form a closed structure")

    # Update the output window
    output_window.update()

    # Speak the note
    speak_text("Note: Minimum Spanning Tree calculated by placing the edges in the increasing order of weights, but the path should not form a closed structure")




def display_output_screen(spanning_tree, node_positions):
    # Clear the combined figure
    combined_figure.clear()

    # Plot the network topology on the left side
    network_topology_ax = combined_figure.add_subplot(121)
    display_network_topology(network_topology, node_positions)
    network_topology_ax.set_title('Network Topology')

    # Plot the minimum spanning tree on the right side
    spanning_tree_ax = combined_figure.add_subplot(122)
    display_network_topology(spanning_tree, node_positions)
    spanning_tree_ax.set_title('Minimum Spanning Tree')

    # Refresh the canvas
    figure_canvas.draw()


def main():
    global root, output_window, nodes, edges_with_weights, num_edges, edges_entry, weights_entry, network_topology, spanning_tree, figure_canvas, node_positions

    # Create the GUI
    root = tk.Tk()
    root.title("Minimum Spanning Tree")
    root.configure(background='light blue')

    nodes = []
    edges_with_weights = []
    num_edges = 0
    edges_entry = []
    weights_entry = []
    network_topology = None
    spanning_tree = None
    figure_canvas = None
    node_positions = None

    def add_node():
        node = node_entry.get()
        if not node:
            messagebox.showerror("Error", "Please enter a node!")
            return
        if not re.match("^[a-zA-Z]$", node):
            messagebox.showerror("Error", "Enter a valid node name")
            return

        nodes.append(node)
        node_entry.delete(0, tk.END)
        display_network()

    def add_edge():
        global num_edges

        num_edges += 1

        # Create edge entry
        edge_label = tk.Label(root, text=f"Enter edge {num_edges} in the format 'node1 node2':", font=("Times New Roman", 12, "italic"), fg="teal",)
        edge_label.pack()
        edge_entry = tk.Entry(root, font=("Times New Roman", 12, "italic"), fg="black",)
        edge_entry.pack()
        edges_entry.append(edge_entry)
        edge_entry.focus_set()  # Set focus on the edge entry box

        # Create weight entry
        weight_label = tk.Label(root, text=f"Enter the weight for edge {num_edges}:", font=("Times New Roman", 12, "italic"), fg="teal",)
        weight_label.pack()
        weight_entry = tk.Entry(root, font=("Times New Roman", 12, "italic"), fg="black",)
        weight_entry.pack()
        weights_entry.append(weight_entry)

    def validate_edges():
        available_nodes = set(nodes)  # Convert the nodes list to a set for efficient membership checking

        
        for i in range(num_edges):
            edge = edges_entry[i].get().split()
            if len(edge) != 2 or not re.match("^[a-zA-Z]+$", edge[0]) or not re.match("^[a-zA-Z]+$", edge[1]):
                messagebox.showerror("Error", "Enter valid values for edges (format: 'node1 node2')")
                return False
            if edge[0] not in available_nodes or edge[1] not in available_nodes:
                messagebox.showerror("Error", "Nodes entered in the edges are not available")
                return False
        return True

    def validate_weights(event):
        weight_entry = event.widget
        weight = weight_entry.get()
        if not re.match("^[0-9]*\.?[0-9]+$", weight):
            messagebox.showerror("Error", "Enter a valid weight value (numeric)")
            weight_entry.focus_set()

    def create_topology_and_calculate():
        global network_topology, node_positions, spanning_tree

        # Validate if any entry label is empty
        for i in range(num_edges):
            if not edges_entry[i].get() or not weights_entry[i].get():
                messagebox.showerror("Error", "Please enter a value for all edges and weights!")
                return
              

        
        # Validate the edge format
        if not validate_edges():
            return

        # Validate the weight format
        for weight_entry in weights_entry:
            weight = weight_entry.get()
            if not re.match("^[0-9]*\.?[0-9]+$", weight):
                messagebox.showerror("Error", "Enter a valid weight value (numeric)")
                return

        # Create the network topology
        edges_with_weights.clear()
        for i in range(num_edges):
            edge = edges_entry[i].get().split()
            weight = weights_entry[i].get()
            edges_with_weights.append((edge, weight))
        network_topology = create_network_topology(nodes, edges_with_weights)
        node_positions = nx.spring_layout(network_topology, seed=42)  # Use a fixed seed for consistent layout

        # Calculate the spanning tree
        spanning_tree = calculate_spanning_tree(network_topology)

        # Create and display the output screen
        create_output_screen(node_positions)

    def display_network():
        # Clear previous display
        for widget in root.winfo_children():
            if (
                widget != add_node_frame
                and widget != add_edge_frame
                and widget != calculate_frame
            ):
                widget.pack_forget()

        # Display nodes
        nodes_label = tk.Label(root, text="Nodes:", font=("Times New Roman", 12, "italic"), fg="teal",)
        nodes_label.pack()
        for node in nodes:
            node_text = tk.Label(root, text=node, font=("Times New Roman", 12, "italic"), fg="black")
            node_text.pack()

        # Display edges
        edges_label = tk.Label(root, text="Edges:", font=("Times New Roman", 12, "italic"), fg="teal",)
        edges_label.pack()
        for i, edge_entry in enumerate(edges_entry):
            edge_text = tk.Label(root, text=f"{edge_entry.get()} (Weight: {weights_entry[i].get()})", font=("Times New Roman", 12, "italic"), fg="teal",)
            edge_text.pack()

    # Add Node Frame
    add_node_frame = tk.Frame(root)
    add_node_frame.pack()

    node_label = tk.Label(add_node_frame, text="Add a node:", font=("Times New Roman", 12, "italic"), fg="teal",)
    node_label.pack(side=tk.LEFT)
    node_entry = tk.Entry(add_node_frame, font=("Times New Roman", 12, "italic"), fg="black",)
    node_entry.pack(side=tk.LEFT)
    node_entry.focus_set()
    add_node_button = tk.Button(add_node_frame, text="Add", font=("Times New Roman", 12, "italic"), fg="teal", command=add_node)
    add_node_button.pack(side=tk.LEFT)

    # Add Edge Frame
    add_edge_frame = tk.Frame(root)
    add_edge_frame.pack()

    add_edge_button = tk.Button(add_edge_frame, text="Add an edge", font=("Times New Roman", 12, "italic"), fg="teal", command=add_edge)
    add_edge_button.pack(side=tk.LEFT)

    # Calculate Frame
    calculate_frame = tk.Frame(root)
    calculate_frame.pack()

    calculate_button = tk.Button(
        calculate_frame,
        text="Create Network Topology and Calculate Minimum Spanning Tree",font=("Times New Roman", 12, "italic"), fg="teal",
        command=create_topology_and_calculate
    )
    calculate_button.pack()

    # Run the main Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
