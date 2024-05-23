from tkinter import *
from PIL import ImageTk, Image
import os
import subprocess
from turtle import *


def run_file1():
    subprocess.Popen(["python", "parityfi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file2():
    subprocess.Popen(["python", "2dparityfi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file3():
    subprocess.Popen(["python", "distancefi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file4():
    subprocess.Popen(["python", "checksumfi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file5():
    subprocess.Popen(["python", "astarfi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file6():
    subprocess.Popen(["python", "hammcodefi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file7():
    subprocess.Popen(["python", "pathfi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file8():
    subprocess.Popen(["python", "spffi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file9():
    subprocess.Popen(["python", "os.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file10():
    subprocess.Popen(["python", "tq.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file11():
    subprocess.Popen(["python", "fldngupdated.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


def run_file12():
    subprocess.Popen(["python", "crcfi.py"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)


# Directly call the run_file functions using button commands
root = Tk()
root.state("zoomed")
root.geometry("874x985")
root.configure(background="black")
root.title("HOME PAGE")

root.state("zoomed")
root.geometry("874x985")
root.configure(background="black")
root.title("HOME PAGE")
global img
img1 = ImageTk.PhotoImage(file="C:/Users/surak/Downloads/picture_proj22.jpg")
lb = Label(root, image=img1)
lb.pack()
lb1 = Label(root, font=('peach puff', 35, 'italic'),
            text="Welcome to Networking Algorithm Simulation", background="rosy brown")
lb1.place(x=120, y=0)

btn1 = Button(root, text="Simple Parity Check", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file1, bg="teal")
btn1.place(x=880, y=70)
btn2 = Button(root, text="Two-Dimensional Parity Check", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file2, bg="teal")
btn2.place(x=880, y=120)
btn3 = Button(root, text="Distance Vector Routing Algorithm", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file3, bg="teal")
btn3.place(x=880, y=170)
btn4 = Button(root, text="Checksum", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file4, bg="teal")
btn4.place(x=880, y=220)
btn5 = Button(root, text="A Star Algorithm", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file5, bg="teal")
btn5.place(x=880, y=270)
btn6 = Button(root, text="Hamming Code", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file6, bg="teal")
btn6.place(x=880, y=320)
btn7 = Button(root, text="Path Finding Algorithm", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file7, bg="teal")
btn7.place(x=880, y=370)
btn8 = Button(root, text="Shortest Path First", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file8, bg="teal")
btn8.place(x=880, y=420)
btn9 = Button(root, text="Open Shortest Path First", font=('Cooper Black', 16, 'italic'),
              background="white", width=27, command=run_file9, bg="teal")
btn9.place(x=880, y=470)
btn10 = Button(root, text="Minimum Spanning Tree", font=('Cooper Black', 16, 'italic'),
               background="white", width=27, command=run_file10, bg="teal")
btn10.place(x=880, y=520)
btn11 = Button(root, text="Flooding Routing Algorithm", font=('Cooper Black', 16, 'italic'),
               background="white", width=27, command=run_file11, bg="teal")
btn11.place(x=880, y=570)
btn12 = Button(root, text="Cyclic Redundancy Check", font=('Cooper Black', 16, 'italic'),
               background="white", width=27, command=run_file12, bg="teal")
btn12.place(x=880, y=620)

root.mainloop()
