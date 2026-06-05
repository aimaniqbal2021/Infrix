import tkinter as tk
import turtle

def draw_heart():
    t.clear()
    t.penup()
    t.goto(0, -100)
    t.pendown()

    t.color("red")
    t.fillcolor("red")

    t.begin_fill()

    t.left(140)
    t.forward(180)

    t.circle(-90, 200)
    t.left(120)
    t.circle(-90, 200)

    t.forward(180)

    t.end_fill()

    t.hideturtle()

# Create Tkinter Window
root = tk.Tk()
root.title("Heart Drawing App")
root.geometry("800x700")

# Canvas for Turtle
canvas = tk.Canvas(root, width=700, height=600)
canvas.pack()

screen = turtle.TurtleScreen(canvas)
screen.bgcolor("white")

t = turtle.RawTurtle(screen)
t.speed(3)

# Button
btn = tk.Button(
    root,
    text="Draw Heart ❤️",
    font=("Arial", 14),
    command=draw_heart
)
btn.pack(pady=10)

root.mainloop()