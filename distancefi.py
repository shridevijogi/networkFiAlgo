import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyttsx3
from tkinter import *

# Initialize the text-to-speech engine
engine = pyttsx3.init()

root = Tk()
root.geometry("1000x600")

G = nx.Graph()
nodes = []
edges = []

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)
main_frame.configure(background='peach puff')  # Set the desired background color


graph_frame = Frame(main_frame, width=600)
graph_frame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

calc_frame = Frame(main_frame, width=300)
calc_frame.pack(side=LEFT, padx=10, pady=10)

fig = plt.figure(figsize=(9, 9), dpi=120)
ax = fig.add_subplot(111)
canvas = None

root.after(1, lambda: root.focus_force())  
root.after(2, lambda: textbox2.focus_set())


def addnode():
    node = textbox2.get().strip()
    if not node:
        messagebox.showerror("Error", "Please enter a node.")
        return

    if not re.match("^[a-zA-Z]+$", node):
        messagebox.showerror("Error", "Node can only contain alphabets.")
        return
    if not re.match("^[a-zA-Z]$", node):
        messagebox.showerror("Error", "Please enter valid node name.")
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

    selected_node1 = listbox.get(listbox.curselection())
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
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)},
                                 font_size=12, font_color='Blue', ax=ax)

    # Redraw the canvas
    canvas.draw()

def shortestpath():
    sn = wt1.get()
    dn = wt2.get()
    if not sn or not dn:
        messagebox.showerror("Error", "Please enter source and destination nodes.")
        return

    if not re.match("^[a-zA-Z]+$", sn) or not re.match("^[a-zA-Z]+$", dn):
        messagebox.showerror("Error", "Source and destination nodes can only contain alphabets.")
        return
    if sn and dn:
        pos = nx.spring_layout(G, seed=42)
        shortest_path = nx.dijkstra_path(G, sn, dn, weight='weight')
        shortest_path_edges = list(zip(shortest_path, shortest_path[1:]))
        path_length = nx.dijkstra_path_length(G, sn, dn, weight='weight')

        # Highlight the shortest path step by step
        for i in range(len(shortest_path_edges)):
            edge = shortest_path_edges[i]
            node1, node2 = edge
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='r', width=5, ax=ax)

            for u, v, d in G.edges(data=True):
                if (u, v) in shortest_path_edges[:i + 1] or (v, u) in shortest_path_edges[:i + 1]:
                    x = (pos[u][0] + pos[v][0]) / 2
                    y = (pos[u][1] + pos[v][1]) / 2
                    ax.text(x, y, f"{d['weight']}", color='r')

            canvas.draw()
            root.update()
            engine.say(f"Distance between {node1} to {node2} is {G[node1][node2]['weight']}")
            engine.runAndWait()

            # Pause for a moment to visualize the step
            root.after(1000)

         
       # Display the total distance at the top left corner
        ax.text(0.05, 0.95, f"Total Distance: {path_length} which is determined by summing the edges assigned ", fontfamily="Times New Roman", fontsize=15,
                color='black', weight='bold', ha='left', va='top', transform=fig.transFigure)

        # Read the total distance aloud
        engine.say("Total distance between {} and {} is {} which is determined by summing the edges assigned".format(sn, dn, path_length))
        engine.runAndWait()

        # Redraw the canvas
        canvas.draw()
    else:
        engine.say("Please enter valid source and destination nodes.")
        engine.runAndWait()

label1 = Label(calc_frame, text="Enter Node:", font=("Times New Roman", 15))
label1.pack(side=TOP, pady=(3, 3))  

textbox2 = Entry(calc_frame, font=("Times New Roman", 15))
textbox2.pack(side=TOP, pady=(3, 3))

but1 = Button(calc_frame, text="Add Node", command=addnode, font=("Times New Roman", 15))
but1.pack(side=TOP, pady=(3, 3))

listbox = Listbox(calc_frame, width=25, height=8, font=("Times New Roman", 15))
listbox.pack(side=TOP, pady=(3, 3))


label2 = Label(calc_frame, text="Select node from listbox:", font=("Times New Roman", 15))
label2.pack(side=TOP, pady=(3, 3))

snode = Entry(calc_frame, font=("Times New Roman", 15))
snode.pack(side=TOP, pady=(3, 3))

label3 = Label(calc_frame, text="Weight:", font=("Times New Roman", 15))
label3.pack(side=TOP, pady=(3, 3))

wt = Entry(calc_frame, font=("Times New Roman", 15))
wt.pack(side=TOP, pady=(3, 3))

but2 = Button(calc_frame, text="Add Path", command=addpath, font=("Times New Roman", 15))
but2.pack(side=TOP, pady=(3, 3))

label4 = Label(calc_frame, text="Source Node:", font=("Times New Roman", 15))
label4.pack(side=TOP, pady=(3, 3))

wt1 = Entry(calc_frame, font=("Times New Roman", 15))
wt1.pack(side=TOP, pady=(3, 3))

label5 = Label(calc_frame, text="Destination Node:", font=("Times New Roman", 15))
label5.pack(side=TOP, pady=(3, 3))

wt2 = Entry(calc_frame, font=("Times New Roman", 15))
wt2.pack(side=TOP, pady=(3, 3))


but3 = Button(calc_frame, text="Find", command=shortestpath, font=("Times New Roman", 15))
but3.pack(side=TOP, pady=(5, 5))

root.mainloop()
