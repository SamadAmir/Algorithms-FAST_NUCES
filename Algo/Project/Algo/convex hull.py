import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as visualizer
from functools import reduce
from heapq import heappop, heappush
import math
from tkinter import filedialog
import random


class GeometricAlgorithms:
    @classmethod
    def convex_hull_graham(cls, canvas=None, speed=None):
        if canvas is None or speed is None:
            return
    
        canvas.delete("geometric")
        points = [(canvas.coords(e)[0] + 3, canvas.coords(e)[1] + 3, e)
                  for e in canvas.find_withtag("point")]
    
        if len(points)<3:
            return
    
        # Adapted Graham's scan algorithm
        def cmp(a, b):
            return (a > b) - (a < b)
    
        def turn(p, q, r):
            return cmp((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]), 0)
    
        def _keep_left(hull, r):
            while len(hull) > 1 and turn(hull[-2], hull[-1], r) != 1:  # Change to 1 for TURN_LEFT
                hull.pop()
    
            if not len(hull) or hull[-1] != r:
                hull.append(r)
                if len(hull) > 1:
                    canvas.create_line(r[0], r[1], hull[-2][0], hull[-2][1], width=2, fill="orange", tag="geometric temp")
                    canvas.update()
                    canvas.after(int(100 / speed.get()))  # Introduce a delay of 100 milliseconds
    
            return hull

        # Store coordinates of convex hull points
        convex_hull_points = []
        
        # Sort points and build convex hull for the lower hull
        points = sorted(points)
        lower_hull = reduce(_keep_left, points, [])
        # Store coordinates of lower hull points
        convex_hull_points.extend(lower_hull)
    
        # Visualize the convex hull for the lower hull
        for i in range(1, len(lower_hull) - 1):
            canvas.create_line(lower_hull[i][0], lower_hull[i][1], lower_hull[i + 1][0], lower_hull[i + 1][1], width=3, fill="black", tag="geometric")
            canvas.update()
            canvas.delete("temp")
            canvas.after(int(100 / speed.get()))  # Introduce a delay of 100 milliseconds
    
        # Build convex hull for the upper hull
        upper_hull = reduce(_keep_left, reversed(points), [])
        # Store coordinates of upper hull points
        convex_hull_points.extend(upper_hull)
    
        # Visualize the convex hull for the upper hull
        for i in range(1, len(upper_hull) - 1):
            canvas.create_line(upper_hull[i][0], upper_hull[i][1], upper_hull[i + 1][0], upper_hull[i + 1][1], width=3, fill="black", tag="geometric")
            canvas.update()
            canvas.delete("temp")
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds

        # Visualize the upper hull
        for i in range(1, len(upper_hull)):
            canvas.create_line(upper_hull[i-1][0], upper_hull[i-1][1], upper_hull[i][0], upper_hull[i][1], width=3, fill="black", tag="geometric")
            canvas.update()
            canvas.delete("temp")
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
        
        # Visualize the connecting line between upper and lower hulls
        canvas.create_line(upper_hull[-1][0], upper_hull[-1][1], lower_hull[0][0], lower_hull[0][1], width=3, fill="black", tag="geometric")
        canvas.update()
        canvas.delete("temp")
        canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds

        # Store coordinates of the last connecting point
        convex_hull_points.append(lower_hull[0])
        
        # Visualize the lower hull
        for i in range(1, len(lower_hull)):
            canvas.create_line(lower_hull[i-1][0], lower_hull[i-1][1], lower_hull[i][0], lower_hull[i][1], width=3, fill="black", tag="geometric")
            canvas.update()
            canvas.delete("temp")
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds

        for x, y, _ in convex_hull_points:
            canvas.create_text(x + 20, y + 20, text=f"({int(x)}, {int(y)})", font=("Arial", 10), fill="black", tag="geometric")


    
    @classmethod
    def convex_hull_jarvis_march(cls, canvas=None, speed=None):
        if canvas is None or speed is None:
            return

        canvas.delete("geometric")
        points = [(canvas.coords(e)[0] + 3, canvas.coords(e)[1] + 3, e)
                  for e in canvas.find_withtag("point")]

        if len(points)<3:
            return

        current_point = min(points, key=lambda x: x[0])
        convex_hull = []

        # Store coordinates of convex hull points
        convex_hull_points = []

        while True:
            convex_hull.append(current_point)
            if len(convex_hull) > 1:
                points.remove(convex_hull[-1])

            endpoint = points[0]
            canvas.create_line(convex_hull[-1][0], convex_hull[-1][1], endpoint[0], endpoint[1],
                               width=1, fill="blue", dash=(3, 1), tag="geometric dashed")

            for j in range(len(points)):
                position = ((points[j][0] - convex_hull[-1][0]) * (endpoint[1] - convex_hull[-1][1]) -
                             (points[j][1] - convex_hull[-1][1]) * (endpoint[0] - convex_hull[-1][0]))

                canvas.create_line(convex_hull[-1][0], convex_hull[-1][1], points[j][0], points[j][1],
                                   fill="orange", dash=(10, 10), tag="geometric temp")
                canvas.update()
                time.sleep(1 / speed.get())

                if (endpoint == current_point) or (position > 0):
                    canvas.delete("dashed")
                    canvas.delete("temp")
                    endpoint = points[j]
                    canvas.create_line(convex_hull[-1][0], convex_hull[-1][1], endpoint[0],
                                       endpoint[1], width=2, fill="grey", dash=(3, 1), tag="geometric dashed")
                    canvas.update()
                    time.sleep(1 / speed.get())
                canvas.delete("temp")

            current_point = endpoint
            canvas.create_line(convex_hull[-1][0], convex_hull[-1][1], endpoint[0], endpoint[1],
                               width=3, fill="black", tag="geometric")
            
            # Store coordinates of the current point in the convex hull
            convex_hull_points.append(current_point)
            
            if endpoint == convex_hull[0]:
                break

        polygon_points = [(e[0], e[1]) for e in convex_hull]
        canvas.create_polygon(*polygon_points, width=4, outline="purple", fill="yellow",
                              stipple="gray50", tag="geometric")
        for x, y, _ in convex_hull_points:
            canvas.create_text(x + 10, y - 10, text=f"({int(x)}, {int(y)})", font=("Arial", 10), fill="black", tag="geometric")

    @classmethod
    def convex_hull_quickhull(cls, canvas=None, speed=None):
        if canvas is None or speed is None:
            return

        canvas.delete("geometric")
        canvas.delete("temp")
        canvas.delete("dashed")
        convex_hull = []
        points = [(canvas.coords(e)[0] + 3, canvas.coords(e)[1] + 3, e)
                  for e in canvas.find_withtag("point")]

        if len(points) <3 :
            return

        # Store coordinates of convex hull points
        convex_hull_points = []

        point_a = min(points, key=lambda x: x[0])
        points.remove(point_a)
        point_b = max(points, key=lambda x: x[0])
        points.remove(point_b)

        canvas.create_line(point_a[0], point_a[1], point_b[0], point_b[1],
                           width=3, tag=f"geometric {point_a[0]}_{point_a[1]}_{point_b[0]}_{point_b[1]}")
        canvas.create_line(point_a[0], point_a[1], point_b[0], point_b[1],
                           width=3, tag=f"geometric {point_b[0]}_{point_b[1]}_{point_a[0]}_{point_a[1]}")
        canvas.update()
        time.sleep(1 / speed.get())

        points_set1 = [e for e in points if ccw(point_a, e, point_b) > 0]
        points_set2 = [e for e in points if ccw(point_a, e, point_b) < 0]

        hull_set1 = cls.find_hull(points_set1, point_a, point_b, canvas, speed)
        hull_set2 = cls.find_hull(points_set2, point_b, point_a, canvas, speed)

        convex_hull = [point_a] + hull_set1 + [point_b] + hull_set2

        # Store coordinates of the convex hull points
        convex_hull_points.extend(convex_hull)

        polygon_points = [(e[0], e[1]) for e in convex_hull]
        canvas.create_polygon(*polygon_points, fill="yellow", outline="black", width=4, stipple="gray50", tag="geometric")

        for x, y, _ in convex_hull_points:
            canvas.create_text(x + 10, y - 10, text=f"({int(x)}, {int(y)})", font=("Arial", 10), fill="black", tag="geometric")

    @classmethod
    def find_hull(cls, points, p, q, canvas, speed):
        if not points:
            return []
        mid = ((p[0] + q[0]) // 2, (p[1] + q[1]) // 2)

        c = max(points, key=lambda e: math.fabs(ccw(p, e, q)))
        canvas.delete(f"{p[0]}_{p[1]}_{q[0]}_{q[1]}")
        canvas.create_line(p[0], p[1], c[0], c[1], width=3, tag=f"geometric {p[0]}_{p[1]}_{c[0]}_{c[1]}")
        canvas.create_line(c[0], c[1], q[0], q[1], width=3, tag=f"geometric {c[0]}_{c[1]}_{q[0]}_{q[1]}")
        canvas.update()
        time.sleep(1 / speed.get())

        set1 = [e for e in points if (ccw(p, e, c) * ccw(p, mid, c)) < 0]
        set2 = [e for e in points if (ccw(q, e, c) * ccw(q, mid, c)) < 0]

        l1 = cls.find_hull(set1, p, c, canvas, speed)
        l2 = cls.find_hull(set2, c, q, canvas, speed)
        return l1 + [c] + l2


    #------------------------------Quick Elimination Algorithm for Convex Hull-----------------------------
    @classmethod
    def convex_hull_SUS_algorithm(cls, canvas=None, speed=None):
        if canvas is None or speed is None:
            return
    
        canvas.delete("geometric")
        points = [(canvas.coords(e)[0] + 3, canvas.coords(e)[1] + 3, e) for e in canvas.find_withtag("point")]
    
        if len(points)<3:
            return
    
        # SUS Algorithm for Convex Hull
        def next_to_top(stack):
            return stack[-2]
    
        def ccw(p1, p2, p3):
            pos = ((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]))
            return -pos
    
        stack = []

    
        # Sort points based on y-coordinates
        lower_half = sorted(points, key=lambda p: (p[1], p[0]))
        upper_half = sorted(points, key=lambda p: (-p[1], p[0]))
    
        # Add the first two points of the lower half to the convex hull
        stack.append(lower_half[0])
        stack.append(lower_half[1])
    
        # Build the convex hull using the SUS algorithm for the lower half
        for i in range(2, len(lower_half)):
            while len(stack) > 1 and ccw(next_to_top(stack), stack[-1], lower_half[i]) <= 0:
                stack.pop()
                canvas.delete("temp")
                canvas.create_line(stack[-1][0], stack[-1][1], lower_half[i][0], lower_half[i][1], width=2, fill="orange",
                                   tag="geometric temp")
                canvas.update()
                canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
    
            stack.append(lower_half[i])
            canvas.create_line(stack[-2][0], stack[-2][1], stack[-1][0], stack[-1][1], width=2, fill="orange",
                               tag="geometric temp")
            canvas.update()
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
    
        # Visualize the convex hull for the lower half
        for i in range(1, len(stack)):
            canvas.create_line(stack[i-1][0], stack[i-1][1], stack[i][0], stack[i][1], width=3, fill="black", tag="geometric")
            canvas.update()
            canvas.delete("temp")
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
    
        # Add the first point of the upper half to the convex hull
        stack.append(upper_half[0])
        canvas.create_line(stack[-2][0], stack[-2][1], stack[-1][0], stack[-1][1], width=2, fill="orange", tag="geometric temp")
        canvas.update()
        canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds#
    
        # Build the convex hull using the SUS algorithm for the upper half
        for i in range(1, len(upper_half)):
            while len(stack) > 1 and ccw(next_to_top(stack), stack[-1], upper_half[i]) <= 0:
                stack.pop()
                canvas.delete("temp")
                canvas.create_line(stack[-1][0], stack[-1][1], upper_half[i][0], upper_half[i][1], width=2, fill="orange",
                                   tag="geometric temp")
                canvas.update()
                canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
    
            stack.append(upper_half[i])
            canvas.create_line(stack[-2][0], stack[-2][1], stack[-1][0], stack[-1][1], width=2, fill="orange",
                               tag="geometric temp")
            canvas.update()
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
    
        # Visualize the convex hull for the upper half
        for i in range(1, len(stack)):
            canvas.create_line(stack[i-1][0], stack[i-1][1], stack[i][0], stack[i][1], width=3, fill="black", tag="geometric")
            canvas.update()
            canvas.delete("temp")
            canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds
        
        # Connect the last point of the upper half to the first point of the lower half
        canvas.create_line(stack[-1][0], stack[-1][1], lower_half[0][0], lower_half[0][1], width=3, fill="black", tag="geometric")
        canvas.update()
        canvas.delete("temp")
        canvas.after(int(100 / speed.get())) # Introduce a delay of 100 milliseconds


    #---------------BruteForceBy SUS------------------------------
    @classmethod
    def convex_hull_bruteforce(cls, canvas=None, speed=None):
        if canvas is None or speed is None:
            return
    
        points = [(canvas.coords(e)[0] + 3, canvas.coords(e)[1] + 3) for e in canvas.find_withtag("point")]
    
        if len(points) < 3:
            return

    
        def is_above(p, a, b):
            cross_product = (p[0] - a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0] - a[0])
            
            if cross_product == 0:
                # Points are collinear, check distance
                dist_pa = (p[0] - a[0])**2 + (p[1] - a[1])**2
                dist_pb = (p[0] - b[0])**2 + (p[1] - b[1])**2
                return dist_pa > dist_pb
            
            return cross_product < 0
    
        def draw_line(p1, p2, color):
            x_values = [p1[0], p2[0]]
            y_values = [p1[1], p2[1]]
            canvas.create_line(x_values[0], y_values[0], x_values[1], y_values[1], width=3, fill=color, tag="geometric")
            canvas.update()
            canvas.after(int(100 / speed.get()))  # Introduce a delay based on the animation speed
    
        # Delete all lines on the canvas
        canvas.delete("geometric")
    
        # Sort points based on x-coordinates
        points.sort()
    
        # Initialize the convex hull
        convex_hull = [points[0]]
    
        # Draw the initial point
        canvas.create_oval(points[0][0] - 2, points[0][1] - 2, points[0][0] + 2, points[0][1] + 2, fill="red", tags=("point",))
    
        # Build the upper hull
        for i in range(1, len(points)):
            convex_hull.append(points[i])
            draw_line(convex_hull[-2], convex_hull[-1], "blue")
    
            while len(convex_hull) > 2 and not is_above(convex_hull[-3], convex_hull[-2], convex_hull[-1]):
                canvas.delete("geometric")
                convex_hull.pop(-2)
                draw_line(convex_hull[-2], convex_hull[-1], "blue")
    
        # Build the lower hull
        for i in range(len(points) - 2, -1, -1):
            convex_hull.append(points[i])
            draw_line(convex_hull[-2], convex_hull[-1], "green")
    
            while len(convex_hull) > 2 and not is_above(convex_hull[-3], convex_hull[-2], convex_hull[-1]):
                canvas.delete("geometric")
                convex_hull.pop(-2)
                draw_line(convex_hull[-2], convex_hull[-1], "green")
    
        # Draw the final convex hull polygon
        convex_hull_polygon = canvas.create_polygon(
            [item for sublist in convex_hull for item in sublist], outline="black", fill="", width=3, tags="geometric"
        )
    
        canvas.update()
        canvas.after(int(100 / speed.get()))  # Introduce a delay based on the animation speed



    #---------MADE BY SUS-------------
    @classmethod
    def visualization_made_by_SUS(cls, canvas=None):
        if canvas is None:
            return

        canvas.delete("geometric")
        canvas.create_text(500, 200, text="Made By Samad Umer Sandesh",
                           font=("Verdana", 18, "bold italic underline"), fill="Green", tag="geometric")
        
    @classmethod
    def add_point_on_click(cls,event,canvas):
        x,y=event.x,event.y
        canvas.create_oval(x-2,y-2,x+2,y+2,fill="red",tags=("point",))
    
    @classmethod
    def add_points_from_file(cls,canvas):
        file_path = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("Text files","*.txt")])
        if file_path:
          with open(file_path,'r') as file:
            for line in file:
                x,y=map(int,line.strip().split())
                canvas.create_oval(x-2,y-2,x+2,y+2,fill="red",tags=("point",))
    
    @classmethod
    def generate_random_points(cls,canvas):
        canvas.delete("point")
        for _ in range(30):  # Add more or fewer points as needed
           x, y = random.randint(100, 800), random.randint(15, 400)
           canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", tags=("point",))


def next_to_top(stack):
    return stack[-2]

def ccw(p1, p2, p3):
    pos = ((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]))
    return -pos

root = visualizer.Tk()
root.title("Geometric Algorithms Visualization")
root.configure(bg="red")

canvas = visualizer.Canvas(root, width=1000, height=430)
canvas.pack()



canvas.bind("<Button-1>",lambda event:GeometricAlgorithms.add_point_on_click(event,canvas))


# Button to start the Jarvis March algorithm
jarvis_march_button = visualizer.Button(root, text="Jarvis March",
                                        command=lambda: GeometricAlgorithms.convex_hull_jarvis_march(canvas, speed),
                                        font=("Arial", 10), bg="lightgray", fg="black", highlightbackground="darkgray")
jarvis_march_button.pack(side="left", padx=10, pady=10)


# Button to start the Quick Hull algorithm
quickhull_button = visualizer.Button(root, text="Quick Hull",
                                     command=lambda: GeometricAlgorithms.convex_hull_quickhull(canvas, speed),
                                     font=("Arial", 10), bg="lightgray", fg="black", highlightbackground="darkgray")
quickhull_button.pack(side="left", padx=10, pady=10)

# Button to start the Graham Scan algorithm
graham_scan_button = visualizer.Button(root, text="Graham Scan",
                                       command=lambda: GeometricAlgorithms.convex_hull_graham(canvas, speed),
                                       font=("Arial", 10), bg="lightgray", fg="black", highlightbackground="darkgray")
graham_scan_button.pack(side="left", padx=10, pady=10)

# Button to start the SUS Convex Hull algorithm
SUS_convex_hull_button = visualizer.Button(root, text="Quick Elimination",
                                           command=lambda: GeometricAlgorithms.convex_hull_SUS_algorithm(canvas, speed),
                                           font=("Arial", 10), bg="lightgray", fg="black", highlightbackground="darkgray")
SUS_convex_hull_button.pack(side="left", padx=10, pady=10)

#brute force button
SUS_bruteforce_button = visualizer.Button(root, text="Bruteforce Convex Hull",
                                          command=lambda: GeometricAlgorithms.convex_hull_bruteforce(canvas, speed),
                                          font=("Arial", 10), bg="lightgray", fg="black",
                                          highlightbackground="darkgray")
SUS_bruteforce_button.pack(side="left", padx=10, pady=10)

#made by SUS button
SUS_visualization_button = visualizer.Button(root, text="Visualization Made By SUS",
                                             command=lambda: GeometricAlgorithms.visualization_made_by_SUS(canvas),
                                             font=("Arial", 10), bg="lightgray", fg="black",
                                             highlightbackground="darkgray")
SUS_visualization_button.pack(side="left", padx=10, pady=10)

add_points_button = visualizer.Button(root, text="Add Points from File",
                                      command=lambda: GeometricAlgorithms.add_points_from_file(canvas),
                                      font=("Arial", 10), bg="lightgray", fg="black", highlightbackground="darkgray")
add_points_button.pack(side="left", padx=10, pady=10)

random_points_button = visualizer.Button(root,text="Add Points Randomly",
                                         command=lambda:GeometricAlgorithms.generate_random_points(canvas),
                                         font=("Arial",10),bg="lightgray",fg="black",highlightbackground="darkgray")
random_points_button.pack(side="left",padx=10,pady=10)

# Scale to control animation speed
speed = visualizer.DoubleVar()
speed_scale = visualizer.Scale(root, from_=1, to=101, orient="horizontal", label="Change Speed", variable=speed,
                               tickinterval=20, font=("Arial", 7), bg="lightgray", fg="black",
                               highlightbackground="darkgray", sliderlength=10, troughcolor="lightblue",
                               activebackground="blue", sliderrelief="raised")
speed_scale.pack(side="right", padx=10, pady=10)

root.mainloop()
