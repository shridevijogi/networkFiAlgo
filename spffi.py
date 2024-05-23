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
selected_items = ""
selected_items1 = ""
l = []

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)
main_frame.configure(background='teal')  # Set the desired background color


# Create the frame for graph visualization
graph_frame = Frame(main_frame, width=600)
graph_frame.pack(side=RIGHT, padx=10,pady=10, fill=BOTH, expand=True)



# Create the right frame for user input
left_frame = Frame(main_frame, width=300)
left_frame.pack(side=LEFT, padx=10,pady=10)

# Create the figure and canvas
fig = plt.figure(figsize=(7, 7), dpi=100)
ax = fig.add_subplot(111)
canvas = None


root.after(1, lambda: root.focus_force())
root.after(2, lambda: textbox2.focus_set())



def addnode():
    node = textbox2.get()
    if not node:
        messagebox.showerror("Error", "Node can't be empty.")
        return
    if not re.match(r"^[A-Za-z]+$", node):
        messagebox.showerror("Error", "Node must contain only alphabetic characters.")
        return
    node = textbox2.get()
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
        messagebox.showerror("Error", "Please enter from node.")
        return
    if not re.match(r"^[A-Za-z]+$", selected_node):
        messagebox.showerror("Error", "Node must contain only alphabetic characters.")
        return
    selected_node1 = listbox.get(listbox.curselection())
    snode.delete(0, END)  # Clear the select node entry widget
    # Set the focus to the select node entry widget after a small delay
    root.after(10, lambda: snode.focus_set())
    weight = wt.get()
    if not weight or not weight.isdigit():
        messagebox.showerror("Error", "Please enter a valid weight (integer).")
        return
    weight = int(weight)
    G.add_edge(selected_node, selected_node1, weight=weight)
    edges.append((selected_node, selected_node1, weight))
    wt.delete(0, END)
    root.after(1, lambda: root.focus_force())
    root.after(2, lambda: wt.focus_set())
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
        messagebox.showerror("Error", "Please enter valid source and destination nodes.")
        return
    if not re.match(r"^[A-Za-z]+$", sn) or not re.match(r"^[A-Za-z]+$", dn):
        messagebox.showerror("Error", "Node must contain only alphabetic characters.")
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
            engine.say(f"Going from {node1} to {node2} with weight {G[node1][node2]['weight']}")
            engine.runAndWait()

            # Pause for a moment to visualize the step
            root.after(1000)

         
        ax.text(0.03, 0.97, f"Shortest path b/w {sn} and {dn} is calculated using Dijkstra's algorithm and is highlighted in red ", fontfamily="Times New Roman", fontsize=13,
                color='teal', weight='bold', ha='left', va='top', transform=fig.transFigure, fontstyle='italic')
        

        ax.text(0.03, 0.92, f"Here it calculates the Shortest Best Path by summing the edge weights ", fontfamily="Times New Roman", fontsize=13,
                color='brown', weight='bold', ha='left', va='top', transform=fig.transFigure, fontstyle='italic')
       
        ax.text(0.03, 0.88, f"and highlights the path whose sum is less compared to the other paths ", fontfamily="Times New Roman", fontsize=13,
                color='brown', weight='bold', ha='left', va='top', transform=fig.transFigure, fontstyle='italic')
    
        # Display the total distance at the top left corner
        ax.text(0.03, 0.83, f"Total Distance here is  {path_length} which is considered as the best path", fontfamily="Times New Roman", fontsize=13,
                color='teal', weight='bold', ha='left', va='top', transform=fig.transFigure, fontstyle='italic')


        # Read the total distance aloud
        engine.say("Shortest path b/w the {} and {} is calculted using djkstraa's slgorithm and is highlighted in red".format(sn, dn, path_length))
        engine.say("Here it calculates the Shortest Best Path by summing the edge weights and highlights the path whose sum is less compared to the other paths ")
        engine.say(" Total Distance here is  {} which is considered as the best path".format(path_length))
        engine.runAndWait()

        # Redraw the canvas 
        canvas.draw()
    else:
        engine.say("Please enter valid source and destination nodes.")
        engine.runAndWait()


# Create labels and input widgets in the right frame
label2 = Label(left_frame, font=("Times New Roman", 17), text="NODE NAME")
label2.grid(row=1, column=0)

textbox2 = Entry(left_frame, width=30)
textbox2.grid(row=1, column=1)

but = Button(left_frame, text="Add",font=("Times New Roman", 17), command=addnode)
but.grid(row=2, column=1)

label11 = Label(left_frame, text="From-node", font=("Times New Roman", 17))
label11.grid(row=3, column=0)

snode = Entry(left_frame, width=30)
snode.grid(row=4, column=0)

labelto = Label(left_frame, text="To-node", font=("Times New Roman", 17))
labelto.grid(row=3, column=1)

listbox = Listbox(left_frame, width=25, height=10, font=("Times New Roman", 16))
listbox.grid(row=4, column=1)


labelw = Label(left_frame, text="Weight", font=("Times New Roman", 17))
labelw.grid(row=3, column=2)

wt = Entry(left_frame, width=30)
wt.grid(row=4, column=2)

labelw1 = Label(left_frame, text="SOURCE", font=("Times New Roman", 17))
labelw1.grid(row=5, column=0)

wt1 = Entry(left_frame, width=30)
wt1.grid(row=6, column=0)

labelw2 = Label(left_frame, text="DESTINATION", font=("Times New Roman", 17))
labelw2.grid(row=5, column=2)

wt2 = Entry(left_frame, width=30)
wt2.grid(row=6, column=2)

but1 = Button(left_frame, text="Add_Path", font=("Times New Roman", 17), command=addpath)
but1.grid(row=7, column=1)

but2 = Button(left_frame, text="CreateGraph", font=("Times New Roman", 17), command=shortestpath)
but2.grid(row=10, column=1)

root.mainloop()
