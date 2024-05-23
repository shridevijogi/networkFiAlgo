import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

# Initialize the text-to-speech engine
import pyttsx3
engine = pyttsx3.init()

root = Tk()
root.geometry("1000x600")
root.configure(bg='lavender')

G = nx.Graph()
nodes = []
edges = []

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)
main_frame.configure(background='teal')  # Set the desired background color


graph_frame = Frame(main_frame, width=600)
graph_frame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)
graph_frame.configure(background='lavender')  # Set the desired background color

calc_frame = Frame(main_frame, width=300)
calc_frame.pack(side=LEFT, padx=10, pady=10)

fig = plt.figure(figsize=(9, 12), dpi=120)
ax = fig.add_subplot(111)
canvas = None

root.after(1, lambda: root.focus_force())
root.after(2, lambda: textbox2.focus_set())


def addnode():
    node = textbox2.get()
    if not node:
        messagebox.showerror("Error", "Please enter a node.")
        return

    if not re.match("^[a-zA-Z]+$", node):
        messagebox.showerror("Error", "Node can only contain alphabets.")
        return
    nodes.append(node)
    G.add_node(node)
    textbox2.delete(0, END)
    listbox.insert(END, node)
    root.after(1, lambda: root.focus_force())
    root.after(2, lambda: textbox2.focus_set())
    draw_graph()


def addpath():
    selected_node = snode.get()
    if not selected_node:
        messagebox.showerror("Error", "Please enter a node.")
        return

    if not re.match("^[a-zA-Z]+$", selected_node):
        messagebox.showerror("Error", "Node can only contain alphabets.")
        return

    selected_indices = listbox.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "Please select a destination node.")
        return

    selected_index = selected_indices[0]  # Assuming only single selection is allowed
    selected_node1 = listbox.get(selected_index)
    snode.delete(0, END)  # Clear the select node entry widget
    # Set the focus to the select node entry widget after a small delay
    root.after(10, lambda: snode.focus_set())

    weight = wt.get().strip()
    if not weight:
        messagebox.showerror("Error", "Please enter a weight.")
        return

    if not re.match("^[0-9]+$", weight):
        messagebox.showerror("Error", "Weight can only contain numerical values.")
        return

    weight = int(weight)

    wt.delete(0, END)  # Clear the weight entry widget
    root.after(1, lambda: root.focus_force())
    root.after(2, lambda: wt.focus_set())

    G.add_edge(selected_node, selected_node1, weight=weight)
    edges.append((selected_node, selected_node1, weight))
    
    draw_graph()

    # Set the focus on the select node entry widget when the program starts
    root.after(10, lambda: snode.focus_set())



def draw_graph():
    global G, nodes, edges, canvas, fig, ax

    # Clear the canvas if it exists
    if canvas:
        canvas.get_tk_widget().destroy()

    # Create a new canvas
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack()

    # Clear the previous graph
    ax.clear()

    # Draw the network graph
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, ax=ax)
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)},
        font_size=12,
        font_color="Blue",
        ax=ax,
    )

    # Redraw the canvas
    canvas.draw()


def find_path(source, destination):
    mst = nx.minimum_spanning_tree(G, algorithm="kruskal", weight="weight")
    try:
        path = nx.shortest_path(mst, source=source, target=destination)
        return path
    except nx.NetworkXNoPath:
        return None


def highlight_path(path, pos):
    if path:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color="r", width=5, ax=ax)
            canvas.draw()
            root.update()
            engine.say(f"Going from {edge[0]} to {edge[1]} with weight {G[edge[0]][edge[1]]['weight']}")
            engine.runAndWait()
            root.after(1000)
    else:
        engine.say("No path exists between the source and destination.")
        engine.runAndWait()


def find_and_highlight_path():
    source = wt1.get()
    destination = wt2.get()
    if not source or not destination:
        messagebox.showerror("Error", "Please enter source and destination nodes.")
        return

    if not re.match("^[a-zA-Z]+$", source) or not re.match("^[a-zA-Z]+$", destination):
        messagebox.showerror("Error", "Source and destination nodes can only contain alphabets.")
        return
    path = find_path(source, destination)
    pos = nx.spring_layout(G, seed=42)
    highlight_path(path, pos)

    # Display the note in the same window
    note_text = "The path between {} and {} is highlighted in red using the greedy Kruskal algorithm in which we find ,\n".format(source, destination)
    note_text += "the minimum spanning tree (MST) and traverse it using Depth First Search (DFS) to find the shortest path."

    note_label = Label(graph_frame, text=note_text, font=("Arial", 14, "italic"), wraplength=500)
    note_label.place(x=20, y=8)  # Adjust the position of the label

    root.after(1000, read_note, note_text)  # Delay execution and call read_note after 1000 milliseconds

def read_note(note_text):
    engine.say(note_text)
    engine.runAndWait()


label1 = Label(calc_frame, text="Enter Node:", font=("Times New Roman", 13))
label1.pack(side=TOP, pady=(4, 4))

textbox2 = Entry(calc_frame, font=("Times New Roman", 13))
textbox2.pack(side=TOP, pady=(4, 4))

but1 = Button(calc_frame, text="Add Node", command=addnode, font=("Times New Roman", 13))
but1.pack(side=TOP, pady=(4, 4))

listbox = Listbox(calc_frame, width=25, height=10, font=("Times New Roman", 13))
listbox.pack(side=TOP, pady=(4, 4))


label2 = Label(calc_frame, text="Select node from listbox:", font=("Times New Roman", 13))
label2.pack(side=TOP, pady=(4, 4))

snode = Entry(calc_frame, font=("Times New Roman", 13))
snode.pack(side=TOP, pady=(4, 4))

label3 = Label(calc_frame, text="Weight:", font=("Times New Roman", 13))
label3.pack(side=TOP, pady=(4, 4))

wt = Entry(calc_frame, font=("Times New Roman", 13))
wt.pack(side=TOP, pady=(4, 4))

but2 = Button(calc_frame, text="Add Path", command=addpath, font=("Times New Roman", 13))
but2.pack(side=TOP, pady=(4, 4))

label4 = Label(calc_frame, text="Source Node:", font=("Times New Roman", 13))
label4.pack(side=TOP, pady=(4, 4))

wt1 = Entry(calc_frame, font=("Times New Roman", 13))
wt1.pack(side=TOP, pady=(4, 4))

label5 = Label(calc_frame, text="Destination Node:", font=("Times New Roman", 13))
label5.pack(side=TOP, pady=(4, 4))

wt2 = Entry(calc_frame, font=("Times New Roman", 13))
wt2.pack(side=TOP, pady=(4, 4))

but3 = Button(calc_frame, text="Find", command=find_and_highlight_path, font=("Times New Roman", 13))
but3.pack(side=TOP, pady=(4, 4))

root.mainloop()
