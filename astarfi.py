import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import messagebox

# Set the backend back to the default
import matplotlib
matplotlib.use("TkAgg")

import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()


G = nx.Graph()
selected_items = ""
selected_items1 = ""
l = []
heuristics = {}
shortest_path=[]
total_cost=[]
goal_heuristic=[]
final_optimal_goal_path=[]
heuristic=[]
sum_cost=[]
listboxto = None  # Declare listboxto as a global variable


def addnode():
    global listboxto  # Access the global variable
    text = textbox2.get()
    if not text.isalpha():
        if not text:
            messagebox.showerror("Invalid input", "Please enter a node name")
        else:
            messagebox.showerror("Invalid input", "Node name should only contain alphabets")
        return
    l.append(text)
    G.add_node(text)
    textbox2.delete(0, END)

    listboxto.insert(END, text)

def add_heuristic():
    selected_item = listboxto.get(listboxto.curselection())
    heuristic_str = textbox_heuristic.get()
    if not heuristic_str.isdigit():
        messagebox.showerror("Invalid input", "Heuristic value must be a number")
        return
    heuristic = int(heuristic_str)
    heuristics[selected_item] = heuristic
    print("Heuristic for", selected_item, ":", heuristic)

    # Clear the textbox
    textbox_heuristic.delete(0, END)
    # Set focus back to the textbox
    textbox_heuristic.focus_set()

    
def addpath():
    selected_items = snode.get()
    selected_items1 = listboxto.get(listboxto.curselection())
    weight_str = wt.get()

    if not selected_items:
        messagebox.showerror("Invalid input", "Please select a 'from' node.")
        return

    if not selected_items1:
        messagebox.showerror("Invalid input", "Please select a 'to' node.")
        return
    
    if not validate_input(selected_items):
        messagebox.showerror("Invalid Input", "From Node should only contain alphabets")
        return

    if not weight_str.isdigit():
        messagebox.showerror("Invalid input", "Weight must be a positive integer.")
        return

    weight = int(weight_str)
    G.add_edge(selected_items, selected_items1, weight=weight)
    print(selected_items, selected_items1)

    # Clear the entry fields
    snode.delete(0, END)
    wt.delete(0, END)
    # Set focus back to the snode entry field
    snode.focus_set()

    draw_graph()


def a_star_path(graph, start, goal):
    open_set = {start}
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristics[start]}

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in graph[current]:
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristics[neighbor]

    return None

def validate_input(node):
    return node.isalpha()

def draw_graph():
    canvas.figure.clf()  # Clear the previous figure
    global shortest_path
    global total_cost
    global sum_cost
    global goal_heuristic
    global final_optimal_cost_path
    

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_size=12, font_color='Blue'
    )

    source_node = wt1.get()
    destination_node = wt2.get()

    if source_node and destination_node:
        if validate_input(source_node) and validate_input(destination_node):
            shortest_path = a_star_path(G, source_node, destination_node)

            # Highlight the final shortest path
            if shortest_path:
                shortest_path_edges = list(zip(shortest_path, shortest_path[1:]))
                

                # Iterate over each edge of the shortest path
                for i, edge in enumerate(shortest_path_edges):
                    # Draw the current edge in red color
                    nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='r', width=5)

                    # Pause for a short duration to create a blinking effect
                    plt.pause(0.5)
                    plt.draw()

                    engine.say(f"Going from {edge[0]} to {edge[1]} with weight {G[edge[0]][edge[1]]['weight']}")
                    engine.runAndWait()


                    # Remove the current edge from the plot
                    nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='b', width=1)

                    # Pause for a short duration to create a blinking effect
                    plt.pause(0.5)
                    plt.draw()

                    # Increase the width of the current edge to highlight it
                    nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='r', width=7)

                    # Pause for a short duration to create a blinking effect
                    plt.pause(0.5)
                    plt.draw()

                nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='r', node_size=500)

                # Calculate the total cost of the shortest path
                total_cost = sum(G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))

                # Get the heuristic value of the goal node
                goal_heuristic = heuristics[shortest_path[-1]]

                # Close the figure window after 1 second
                root.after(100, lambda: plt.close())


                # Add a note to the canvas with the optimal cost path
                canvas.figure.text(0.02, 0.85, f"Optimal Cost Path (f(n)): {shortest_path} (Total Cost: {total_cost} (g(n)), Heuristic Value: {goal_heuristic} (h(n), Sum: {total_cost + goal_heuristic})",
                         fontsize=12, fontweight='bold')

                

                # Calculate the sum of total cost and goal heuristic
                final_optimal_cost_path = total_cost + goal_heuristic

                # Add a note to the canvas with the final optimal cost path
                canvas.figure.text(0.02, 0.75, f"Optimal Cost Path (f(n) = g(n) + h(n)): {final_optimal_cost_path}",
                         transform=canvas.figure.gca().transAxes, fontsize=12, fontweight='bold')


                #display heuristic
                canvas.figure.text(0.02,0.65, "Heuristic values:",transform=canvas.figure.gca().transAxes, fontsize=12, fontweight='bold',bbox=dict(facecolor='white',edgecolor='black',boxstyle='round,pad=0.5'))
                y=0.6
                for node, heuristic in heuristics.items():
                    canvas.figure.text(0.02, y, f"{node}: {heuristic}",transform=canvas.figure.gca().transAxes, fontsize=12)
                    y-=0.05

    canvas.draw_idle()  # Redraw the updated figure

def show_note():
    global shortest_path
    global heuristic
    global total_cost
    global sum_cost
    global final_optimal_cost_path
    global goal_heuristic
    source_node = wt1.get()
    destination_node = wt2.get()

    if source_node and destination_node:
        if validate_input(source_node) and validate_input(destination_node):
            shortest_path = a_star_path(G, source_node, destination_node)

            # Add a note to the canvas with the optimal cost path
            canvas.figure.text(0.02, 0.85, "Optimal Cost Path (f(n)): ...",
                     fontsize=12, fontweight='bold')

            # Add the right note
            right_note = """
            A* Search Algorithm

            At first, it traverses to the given node
            and then searches for the best shortest path.
            Based on that, the optimal cost path is calculated.

            f(n): Optimal cost path
            g(n): Sum of total costs based on weights
            of the best shortest path
            h(n): Heuristic value of the goal node

            f(n) = g(n) + h(n)
            """

            canvas.figure.text(0.95, 0.95, right_note, transform=canvas.figure.gca().transAxes, fontsize=10, fontweight='bold', ha='right', va='top')

            # Add a note on the Figure 1 window with the final optimal cost path
            canvas.figure.text(0.02, 0.75, f"Optimal Cost Path (f(n) = g(n){total_cost} + h(n){goal_heuristic}): {final_optimal_cost_path}",
            transform=canvas.figure.gca().transAxes, fontsize=12, fontweight='bold',bbox=dict(facecolor='white',edgecolor='black',boxstyle='round,pad=0.5'))

            canvas.figure.text(0.02,0.65, "Heuristic values:",transform=canvas.figure.gca().transAxes, fontsize=12, fontweight='bold',bbox=dict(facecolor='white',edgecolor='black',boxstyle='round,pad=0.5'))
            y=0.6
            for node, heuristic in heuristics.items():
                canvas.figure.text(0.02, y, f"{node}: {heuristic}",transform=canvas.figure.gca().transAxes, fontsize=12)
                y-=0.05
            
            canvas.draw_idle()  # Redraw the updated figure

def start_speech_engine():
    global shortest_path
    global heuristic
    global total_cost
    global goal_heuristic
    global sum_cost
    global final_optimal_cost_path
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    text = """Optimal Cost Path that is (f of (n)) {shortest_path} : (Total Cost: {total_cost} which is (g of (n)) , Heuristic Value: {goal_heuristic} which is  (h of (n), Sum is :  {sum_cost})
        Optimal Cost Path (f of (n) = g of (n) + h of (n)) is : {final_optimal_cost_path}

        
        A star Search Algorithm

        At first, it traverses to the given node
        and then searches for the best shortest path.
        Based on that, the optimal cost path is calculated.

        f of (n) : Optimal cost path
        g of (n) : Sum of total costs based on weights of the best shortest path
        h of (n) : Heuristic value of the goal node

        f of (n) = g of (n) + h of (n)""".format(
            heuristic=heuristic,
            shortest_path=shortest_path,
            total_cost=total_cost,
            goal_heuristic=goal_heuristic,
            sum_cost=total_cost + goal_heuristic,
            final_optimal_cost_path=final_optimal_cost_path
        )


    # Set the properties for speech output
    engine.setProperty("rate", 150)  # Speed of speech
    engine.setProperty("volume", 0.8)  # Volume (0.0 to 1.0)

    # Say the text
    engine.say(text)
    engine.runAndWait()


def generate_graph():
    start_node=wt1.get()
    goal_node=wt2.get()
    if not validate_input(start_node) or not validate_input(goal_node):
        messagebox.showerror("Invalid Input", "Invalid start or goal node. only alphabets are allowed")
        return
    draw_graph()
    
    # Close the figure window after 1 second
    root.after(1000, lambda: plt.close())
    
    # Show the note on the canvas after the figure window is closed
    root.after(1000, show_note)
    
    # Start the speech engine after a delay
    root.after(2000, start_speech_engine)


# Create the main window
root = Tk()
root.geometry("1000x800")
root.configure(bg="peach puff")


root.after(1, lambda: root.focus_force())
root.after(2, lambda: textbox2.focus_set())


# Create labels
label2 = Label(root, text="NODE NAME")
label2.grid(row=1, column=0)

textbox2 = Entry(root, width=30)
textbox2.grid(row=1, column=1)

but = Button(root, text="Add", command=addnode)
but.grid(row=2, column=1)

label3 = Label(root, text="Heuristic Value")
label3.grid(row=3, column=0)


textbox_heuristic = Entry(root, width=30)
textbox_heuristic.grid(row=3, column=1)
but_heuristic = Button(root, text="Add Heuristic", command=add_heuristic)
but_heuristic.grid(row=4, column=1)

label_from = Label(root, text="From Node")
label_from.grid(row=5, column=0)

snode = Entry(root, width=30)
snode.grid(row=6, column=0)

label_to = Label(root, text="To Node")
label_to.grid(row=5, column=1)

listboxto = Listbox(root)
listboxto.grid(row=6, column=1)

label_weight = Label(root, text="Weight")
label_weight.grid(row=7, column=1)

wt = Entry(root, width=30)
wt.grid(row=8, column=1)

label11 = Label(root, text="START NODE")
label11.grid(row=9, column=0)

wt1 = Entry(root, width=30)
wt1.grid(row=10, column=0)

label_dest = Label(root, text="GOAL NODE")
label_dest.grid(row=9, column=1)

wt2 = Entry(root, width=30)
wt2.grid(row=10, column=1)

but_path = Button(root, text="Add Path", command=addpath)
but_path.grid(row=11, column=1)

but_grap = Button(root, text="Generate Graph", command=generate_graph)
but_grap.grid(row=12, column=1)


fig, ax = plt.subplots(figsize=(10, 5))

# Create the Canvas for graph visualization
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=8, padx=10, pady=10)

# Pack the root and start the event loop
root.mainloop()
