import tkinter as tk
from tkinter import filedialog

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def onSegment(p, q, r):
    if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
        q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
        return True
    return False

def orientation(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:
        return 1
    elif val < 0:
        return 2
    else:
        return 0

def cross_product(p1, p2):
    return p1.x * p2.y - p1.y * p2.x

def subtract_points(p1, p2):
    return Point(p1.x - p2.x, p1.y - p2.y)

def on_segment(p, q, r):
    return min(p.x, r.x) <= q.x <= max(p.x, r.x) and min(p.y, r.y) <= q.y <= max(p.y, r.y)

def do_intersect_vector_method(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def doIntersectCCW(p1, q1, p2, q2):
    return do_intersect_vector_method(p1, q1, p2, q2)

def doIntersectCramers(p1, q1, p2, q2):
    A1 = q1.y - p1.y
    B1 = p1.x - q1.x
    C1 = A1 * p1.x + B1 * p1.y

    A2 = q2.y - p2.y
    B2 = p2.x - q2.x
    C2 = A2 * p2.x + B2 * p2.y

    determinant = A1 * B2 - A2 * B1

    if determinant == 0:
        return False, None  # Lines are parallel, no intersection point

    x = (C1 * B2 - C2 * B1) / determinant
    y = (C2 * A1 - C1 * A2) / determinant

    intersection_point = Point(x, y)

    if onSegment(p1, intersection_point, q1) and onSegment(p2, intersection_point, q2):
        return True, intersection_point

    return False, None

class LineSegmentVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Line Segment Intersection Visualizer")
        self.root.configure(bg="blue")

        self.canvas = tk.Canvas(self.root, width=1000, height=430, bg="white")
        self.canvas.pack()

        self.points = []
        self.lines = []
        self.intersection_point = None

        # Buttons to choose the method
        self.ccw_button = tk.Button(self.root, text="CCW Method", command=self.run_ccw,
                                    font=("Arial", 20), bg="lightgray", fg="black", highlightbackground="darkgray")
        self.cramers_button = tk.Button(self.root, text="Cramer's Method", command=self.run_cramers,
                                       font=("Arial", 20), bg="lightgray", fg="black", highlightbackground="darkgray")
        self.vector_button = tk.Button(self.root, text="Vector Method", command=self.run_vector_method,
                                       font=("Arial", 20), bg="lightgray", fg="black", highlightbackground="darkgray")
        self.SUS_button = tk.Button(self.root, text="Made by SUS", command=self.display_SUS,
                                    font=("Arial", 20), bg="lightgray", fg="black", highlightbackground="darkgray")


        self.ccw_button.pack(side="left", padx=20, pady=10)
        self.cramers_button.pack(side="left", padx=20, pady=10)
        self.vector_button.pack(side="left", padx=20, pady=10)
        self.load_button = tk.Button(self.root, text="Load Points from File", command=self.load_points_from_file,
                                     font=("Arial", 20), bg="lightgray", fg="black", highlightbackground="darkgray")
        self.load_button.pack(side="left", padx=20, pady=20)
        self.SUS_button.pack(side="left", padx=20, pady=10)




    def run_vector_method(self):
        self.reset_canvas()
        self.canvas.bind("<Button-1>", self.on_click_vector_method)

    def on_click_vector_method(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))

        # Draw points
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        
        # Display coordinates near the point
        self.canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", font=("Arial", 10), fill="black")

        if len(self.points) == 4:
            self.find_intersection_vector_method()

    def find_intersection_vector_method(self):
        # Create lines based on selected points
        p1, q1, p2, q2 = self.points
        self.lines = [(p1, q1), (p2, q2)]

        # Check for intersection using Vector Cross Product method
        intersect = do_intersect_vector_method(p1, q1, p2, q2)
        self.visualize_result(intersect)

    def run_ccw(self):
        self.reset_canvas()
        self.canvas.bind("<Button-1>", self.on_click_ccw)

    def on_click_ccw(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))

        # Draw points
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        
        # Display coordinates near the point
        self.canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", font=("Arial", 10), fill="black")

        if len(self.points) == 4:
            self.find_intersection_ccw()

    def find_intersection_ccw(self):
        # Create lines based on selected points
        p1, q1, p2, q2 = self.points
        self.lines = [(p1, q1), (p2, q2)]

        # Check for intersection using CCW method
        intersect = doIntersectCCW(p1, q1, p2, q2)
        self.visualize_result(intersect)

    def run_cramers(self):
        self.reset_canvas()
        self.canvas.bind("<Button-1>", self.on_click_cramers)

    def on_click_cramers(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))

        # Draw points
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        
        # Display coordinates near the point
        self.canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", font=("Arial", 10), fill="black")

        if len(self.points) == 4:
            self.find_intersection_cramers()
            
    def find_intersection_cramers(self):
        # Create lines based on selected points
        p1, q1, p2, q2 = self.points
        self.lines = [(p1, q1), (p2, q2)]

        # Check for intersection using Cramer's method
        intersect, intersection_point = doIntersectCramers(p1, q1, p2, q2)
        if intersect:
            # Round the coordinates to the nearest integers
            intersection_point.x = int(round(intersection_point.x))
            intersection_point.y = int(round(intersection_point.y))

            self.intersection_point = intersection_point
            self.visualize_intersection()
        else:
            self.visualize_lines()

    def visualize_lines(self):
        # Visualize lines
        self.canvas.create_line(self.lines[0][0].x, self.lines[0][0].y, self.lines[0][1].x, self.lines[0][1].y,
                                fill="blue", width=2)
        self.canvas.create_line(self.lines[1][0].x, self.lines[1][0].y, self.lines[1][1].x, self.lines[1][1].y,
                                fill="green", width=2)
        self.canvas.create_text(470, 415, text="Lines are not intersecting", font=("Verdana", 18, "bold italic"), fill="red")

        # Disable further clicks
        self.canvas.unbind("<Button-1>")

    def visualize_intersection(self):
        # Visualize lines
        self.canvas.create_line(self.lines[0][0].x, self.lines[0][0].y, self.lines[0][1].x, self.lines[0][1].y,
                                fill="blue", width=2)
        self.canvas.create_line(self.lines[1][0].x, self.lines[1][0].y, self.lines[1][1].x, self.lines[1][1].y,
                                fill="green", width=2)

        # Visualize intersection point
        self.canvas.create_oval(self.intersection_point.x - 5, self.intersection_point.y - 5,
                                self.intersection_point.x + 5, self.intersection_point.y + 5, fill="black")
        self.canvas.create_text(self.intersection_point.x + 20, self.intersection_point.y + 20,
                            text=f"({self.intersection_point.x}, {self.intersection_point.y})", font=("Arial bold", 10),
                            fill="black")
        self.canvas.create_text(480, 415, text="Lines are intersecting", font=("Verdana", 18, "bold italic"), fill="green")
        # Disable further clicks
        self.canvas.unbind("<Button-1>")

    def visualize_result(self, intersect):
        # Visualize lines
        self.canvas.create_line(self.lines[0][0].x, self.lines[0][0].y, self.lines[0][1].x, self.lines[0][1].y,
                                fill="blue", width=2)
        self.canvas.create_line(self.lines[1][0].x, self.lines[1][0].y, self.lines[1][1].x, self.lines[1][1].y,
                                fill="green", width=2)

        if intersect:
            # Visualize the area where the intersection point can be located
            self.canvas.create_rectangle(
                min(self.lines[0][0].x, self.lines[0][1].x, self.lines[1][0].x, self.lines[1][1].x),
                min(self.lines[0][0].y, self.lines[0][1].y, self.lines[1][0].y, self.lines[1][1].y),
                max(self.lines[0][0].x, self.lines[0][1].x, self.lines[1][0].x, self.lines[1][1].x),
                max(self.lines[0][0].y, self.lines[0][1].y, self.lines[1][0].y, self.lines[1][1].y),
                outline="yellow", width=2, stipple="gray25"
            )
            self.canvas.create_text(480, 415, text="Lines are intersecting in the yellow area",
                                    font=("Consolas", 20), fill="green")
        else:
            self.canvas.create_text(470, 415, text="Lines are not intersecting", font=("Verdana", 18, "bold italic"), fill="red")

        # Disable further clicks
        self.canvas.unbind("<Button-1>")

    def display_SUS(self):
        # Display SUS information
        self.reset_canvas()
        self.canvas.create_text(500, 200, text="Made by Samad Umer Sandesh\n\t(SUS)", font=("Verdana", 20, "bold underline"), fill="red")

    def reset_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.lines = []

    def run(self):
        self.root.mainloop()
    def load_points_from_file(self):
    # Open a file dialog to choose a .txt file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_path:
        # Read points from the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

        # Extract points from each line
        loaded_points = [tuple(map(int, line.strip().split())) for line in lines]

        # Draw points on canvas
        self.reset_canvas()
        for x, y in loaded_points:
            self.points.append(Point(x, y))
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
            self.canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", font=("Arial", 10), fill="black")

        # If the number of points is 4, proceed to check for intersection
        if len(self.points) == 4:
            self.find_intersection_vector_method()

# Driver program
visualizer = LineSegmentVisualizer()
visualizer.run()

