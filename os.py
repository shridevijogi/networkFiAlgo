import heapq
import tkinter as tk
import math
from tkinter import Canvas
from tkinter import messagebox
import re


class Graph:
    def __init__(self):
        self.vertices = {}
        self.node_coordinates = {}

    def add_vertex(self, name):
        if name not in self.vertices:
            self.vertices[name] = {}

    def add_edge(self, start, end, weight):
        if start not in self.vertices:
            self.add_vertex(start)
        if end not in self.vertices:
            self.add_vertex(end)
        self.vertices[start][end] = weight
        self.vertices[end][start] = weight

    def shortest_path(self, start, finish):
        distances = {}
        previous = {}
        heap = []

        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(heap, (0, vertex))
            else:
                distances[vertex] = float('inf')
                heapq.heappush(heap, (float('inf'), vertex))
            previous[vertex] = None

        while heap:
            current_distance, current_vertex = heapq.heappop(heap)

            if current_vertex == finish:
                path = []
                while current_vertex:
                    path.append(current_vertex)
                    current_vertex = previous[current_vertex]
                path.append(start)
                return path[::-1], distances, previous

            for neighbor, weight in self.vertices[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    for index, (dist, vert) in enumerate(heap):
                        if vert == neighbor:
                            heap[index] = (distance, neighbor)
                            heapq.heapify(heap)
                            break

        return None, None, None

    def generate_topology(self):
        # Arrange nodes in a linear order
        vertices = list(self.vertices.keys())
        num_vertices = len(vertices)
        num_rows = math.ceil(math.sqrt(num_vertices))

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        for i in range(num_vertices):
            row = i // num_rows
            col = i % num_rows
            x = col * (canvas_width / (num_rows + 1)) + (canvas_width / (num_rows + 1))
            y = row * (canvas_height / (num_rows + 1)) + (canvas_height / (num_rows + 1))
            self.node_coordinates[vertices[i]] = (x, y)

        # Generate a fully connected topology based on the weights of the edges
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                start = vertices[i]
                end = vertices[j]
                if end in self.vertices[start]:
                    weight = self.vertices[start][end]
                    self.add_edge(start, end, weight)

    def draw_graph(self, canvas, shortest_path=None, start_vertex=None, end_vertex=None):
        edge_list = set()
        canvas.delete('all')
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        for vertex in self.vertices:
            if vertex in self.node_coordinates:
                x, y = self.node_coordinates[vertex]
                node_radius = 30
                canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill='lightblue')
                canvas.create_text(x, y, text=vertex)
                for neighbor, weight in self.vertices[vertex].items():
                    if neighbor in self.node_coordinates:
                        x1, y1 = self.node_coordinates[vertex]
                        x2, y2 = self.node_coordinates[neighbor]
                        color = 'black'
                        arrow_shape = (8, 10, 3)
                        if shortest_path is not None and ((vertex, neighbor) in shortest_path or (neighbor, vertex) in shortest_path):
                            color = 'red'
                            arrow_shape = (12, 14, 6)
                        canvas.create_line(x1, y1, x2, y2, fill=color, arrow=tk.LAST, arrowshape=arrow_shape)
                        edge_list.add((vertex, neighbor))
                        edge_list.add((neighbor, vertex))
                        # Display weight above the edge
                        weight_x = (x1 + x2) / 2
                        weight_y = (y1 + y2) / 2
                        canvas.create_text(weight_x, weight_y, text=str(weight))

        if shortest_path is not None:
            for i in range(len(shortest_path) - 1):
                current_vertex = shortest_path[i]
                next_vertex = shortest_path[i + 1]
                if current_vertex in self.node_coordinates and next_vertex in self.node_coordinates:
                    x1, y1 = self.node_coordinates[current_vertex]
                    x2, y2 = self.node_coordinates[next_vertex]
                    canvas.create_line(x1, y1, x2, y2, fill='red', width=2)

        if start_vertex and start_vertex in self.node_coordinates:
            x, y = self.node_coordinates[start_vertex]
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline='green', width=2)
        if end_vertex and end_vertex in self.node_coordinates:
            x, y = self.node_coordinates[end_vertex]
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline='brown', width=2)


# GUI setup
window = tk.Tk()
window.title("Open Shortest Path GUI")
window.configure(background="mint cream")

frame = tk.Frame(window)
frame.pack(side=tk.RIGHT)


canvas = Canvas(frame, width=800, height=700, bg='orange')
canvas.pack(side=tk.LEFT)

graph = Graph()


def add_node():
    node_name = node_entry.get()
    if not node_name:
        messagebox.showerror("Error", "Node name can't be empty")
        return
    
    if not re.match("^[a-zA-Z]$", node_name):
        messagebox.showerror("Error", "Enter a valid node name")
        return
    
    graph.add_vertex(node_name)
    graph.generate_topology()
    canvas.delete('all')
    graph.draw_graph(canvas)
    node_entry.delete(0, tk.END)


def add_edge():
    start = from_entry.get()
    end = to_entry.get()
    weight = weight_entry.get()
    
    if not (start and end and weight):
        messagebox.showerror("Error", "All textboxes must be filled with valid values")
        return
    if not re.match("^[a-zA-Z]$", start):
        messagebox.showerror("Error", "Enter a valid node name")
        return
    if not re.match("^[a-zA-Z]$", end):
        messagebox.showerror("Error", "Enter a valid node name")
        return
    if not weight.isdigit():
        messagebox.showerror("Error", "Enter a valid value for weight")
        return
    
    graph.add_edge(start, end, int(weight))
    graph.generate_topology()
    canvas.delete('all')
    graph.draw_graph(canvas)
    from_entry.delete(0, tk.END)
    to_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)


def find_shortest_path():
    start_vertex = start_entry.get()
    end_vertex = end_entry.get()

    if not (start_vertex and end_vertex):
        messagebox.showerror("Error", "Start vertex and end vertex can't be empty")
        return
    if not re.match("^[a-zA-Z]$", start_vertex):
        messagebox.showerror("Error", "Enter a valid node name")
        return
    if not re.match("^[a-zA-Z]$", end_vertex):
        messagebox.showerror("Error", "Enter a valid node name")
        return
    
    shortest_path, _, _ = graph.shortest_path(start_vertex, end_vertex)
    if shortest_path:
        canvas.delete('all')
        graph.draw_graph(canvas, shortest_path)
        result_text.set(f"Shortest path from {start_vertex} to {end_vertex}: {' -> '.join(shortest_path)}")
    else:
        result_text.set(f"No path found from {start_vertex} to {end_vertex}")


def generate_topology():
    graph.generate_topology()
    canvas.delete('all')
    graph.draw_graph(canvas)


def on_canvas_resize(event):
    canvas.delete('all')
    graph.draw_graph(canvas)


canvas.bind("<Configure>", on_canvas_resize)


node_label = tk.Label(window, text="Node Name:", font=("Times New Roman", 12, "italic"), fg="teal")
node_label.place(x=10, y=20)

node_entry = tk.Entry(window)
node_entry.place(x=100, y=20)
node_entry.focus_set()  # Set focus on the entry widget

add_node_button = tk.Button(window, text="Add Node", font=("Times New Roman", 12, "italic"), fg="teal", command=add_node)
add_node_button.place(x=230, y=10)

from_label = tk.Label(window, text="From Node:", font=("Times New Roman", 12, "italic"), fg="teal")
from_label.place(x=10, y=60)

from_entry = tk.Entry(window)
from_entry.place(x=100, y=60)

to_label = tk.Label(window, text="To Node:", font=("Times New Roman", 12, "italic"), fg="teal")
to_label.place(x=10, y=100)

to_entry = tk.Entry(window)
to_entry.place(x=100, y=100)

weight_label = tk.Label(window, text="Weight:", font=("Times New Roman", 12, "italic"), fg="teal")
weight_label.place(x=10, y=140)

weight_entry = tk.Entry(window)
weight_entry.place(x=100, y=140)

add_edge_button = tk.Button(window, text="Add Edge", font=("Times New Roman", 12, "italic"), fg="teal", command=add_edge)
add_edge_button.place(x=230, y=130)


start_label = tk.Label(window, text="Start Vertex:", font=("Times New Roman", 12, "italic"), fg="teal",)
start_label.place(x=10, y=180)

start_entry = tk.Entry(window)
start_entry.place(x=100, y=180)

end_label = tk.Label(window, text="End Vertex:", font=("Times New Roman", 12, "italic"), fg="teal",)
end_label.place(x=10, y=220)

end_entry = tk.Entry(window)
end_entry.place(x=100, y=220)

find_shortest_path_button = tk.Button(window, text="Find Shortest Path", font=("Times New Roman", 12, "italic"), fg="teal", command=find_shortest_path)
find_shortest_path_button.place(x=230, y=210)

result_text = tk.StringVar()
result_label = tk.Label(window, textvariable=result_text, font=("Times New Roman", 12, "bold"), fg="teal")
result_label.place(x=10, y=260)



window.mainloop()
