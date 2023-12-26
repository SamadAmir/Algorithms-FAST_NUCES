import tkinter as tk
import random
import time
from functools import cmp_to_key

class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.angle = 0.0
        self.area = 0
        self.isFirstPointOnHull = False
        self.isOnHull = False
        self.flag = False

def ccw_test(p1, p2, p3):
    return (p3.y - p1.y) * (p2.x - p1.x) > (p2.y - p1.y) * (p3.x - p1.x)

def area(a, b, c):
    return ((b.x - a.x) * (c.y - a.y)) - ((b.y - a.y) * (c.x - a.x))

def find_max_y(points):
    return max(points, key=lambda p: p.y)

def find_min_y(points):
    return min(points, key=lambda p: p.y)

def find_max_x(points):
    return max(points, key=lambda p: p.x)

def find_min_x(points):
    return min(points, key=lambda p: p.x)

def draw_line(canvas, a, b):
    canvas.create_line(a.x, a.y, b.x, b.y, fill='green')

def find_convex_hull(points, canvas):
    hull = []
    hull.append(find_min_x(points))
    hull.append(find_min_y(points))
    hull.append(find_max_x(points))
    hull.append(find_max_y(points))

    draw_line(canvas, hull[0], hull[1])
    draw_line(canvas, hull[1], hull[2])
    draw_line(canvas, hull[2], hull[3])
    draw_line(canvas, hull[3], hull[0])

    for point in points:
        point.flag = False

    # Check if any point is in region 1, remove it from the hull
    for point in points:
        if point != hull[0] and point != hull[1] and area(hull[0], hull[1], point) < 0:
            point.flag = True

    # Check if any point is in region 2, remove it from the hull
    for point in points:
        if point != hull[1] and point != hull[2] and area(hull[1], hull[2], point) < 0:
            point.flag = True

    # Check if any point is in region 3, remove it from the hull
    for point in points:
        if point != hull[2] and point != hull[3] and area(hull[2], hull[3], point) < 0:
            point.flag = True

    # Check if any point is in region 4, remove it from the hull
    for point in points:
        if point != hull[3] and point != hull[0] and area(hull[3], hull[0], point) < 0:
            point.flag = True

    # Add points to region 1 array
    region1 = [hull[0], hull[1]]
    region1.extend([point for point in points if point != region1[0] and point != region1[1] and point.flag and area(region1[0], region1[1], point) < 0])
    region1.sort(key=lambda p: p.x)

    # Add points to region 2 array
    region2 = [hull[1], hull[2]]
    region2.extend([point for point in points if point != region1[0] and point != region2[1] and point.flag and area(region2[0], region2[1], point) < 0])
    region2.sort(key=lambda p: p.x)

    # Add points to region 3 array
    region3 = [hull[2], hull[3]]
    region3.extend([point for point in points if point != region3[0] and point != region3[1] and point.flag and area(region3[0], region3[1], point) < 0])
    region3.sort(key=lambda p: p.x, reverse=True)

    # Add points to region 4 array
    region4 = [hull[3], hull[0]]
    region4.extend([point for point in points if point != region4[0] and point != region4[1] and point.flag and area(region4[0], region4[1], point) < 0])
    region4.sort(key=lambda p: p.x, reverse=True)

    # Get hull of region 1
    if len(region1) > 3:
        j_itr = 2
        temp_itr = 0
        temp = region1[temp_itr]
        i = region1[1]
        j = region1[j_itr]
        while j != region1[-1]:
            if area(temp, i, j) >= 0:
                temp_itr += 1
                temp = region1[temp_itr]
                i = j
                j_itr += 1
                j = region1[j_itr]
            else:
                region1.remove(i)
                if temp_itr - 1 < 0:
                    temp_itr = 0
                    i = j
                    j = region1[j_itr]
                else:
                    j_itr -= 1
                    i = region1[temp_itr]
                    temp_itr -= 1
                    temp = region1[temp_itr]
        if area(temp, i, j) < 0:
            region1.remove(i)

    # Get hull of region 2
    if len(region2) > 3:
        j_itr = 2
        temp_itr = 0
        temp = region2[temp_itr]
        i = region2[1]
        j = region2[j_itr]
        while j != region2[-1]:
            if area(temp, i, j) >= 0:
                temp_itr += 1
                temp = region2[temp_itr]
                i = j
                j_itr += 1
                j = region2[j_itr]
            else:
                region2.remove(i)
                if temp_itr - 1 < 0:
                    temp_itr = 0
                    i = j
                    j = region2[j_itr]
                else:
                    j_itr -= 1
                    i = region2[temp_itr]
                    temp_itr -= 1
                    temp = region2[temp_itr]
        if area(temp, i, j) < 0:
            region2.remove(i)

    # Get hull of region 3
    if len(region3) > 3:
        j_itr = 2
        temp_itr = 0
        temp = region3[temp_itr]
        i = region3[1]
        j = region3[j_itr]
        while j != region3[-1]:
            if area(temp, i, j) >= 0:
                temp_itr += 1
                temp = region3[temp_itr]
                i = j
                j_itr += 1
                j = region3[j_itr]
            else:
                region3.remove(i)
                if temp_itr - 1 < 0:
                    temp_itr = 0
                    i = j
                    j = region3[j_itr]
                else:
                    j_itr -= 1
                    i = region3[temp_itr]
                    temp_itr -= 1
                    temp = region3[temp_itr]
        if area(temp, i, j) < 0:
            region3.remove(i)

    # Get hull of region 4
    if len(region4) > 3:
        j_itr = 2
        temp_itr = 0
        temp = region4[temp_itr]
        i = region4[1]
        j = region4[j_itr]
        while j != region4[-1]:
            if area(temp, i, j) >= 0:
                temp_itr += 1
                temp = region4[temp_itr]
                i = j
                j_itr += 1
                j = region4[j_itr]
            else:
                region4.remove(i)
                if temp_itr - 1 < 0:
                    temp_itr = 0
                    i = j
                    j = region4[j_itr]
                else:
                    j_itr -= 1
                    i = region4[temp_itr]
                    temp_itr -= 1
                    temp = region4[temp_itr]
        if area(temp, i, j) < 0:
            region4.remove(i)

    for point in region1:
        print(point.name, end=" ")
    for point in region2:
        print(point.name, end=" ")
    for point in region3:
        print(point.name, end=" ")
    for point in region4:
        print(point.name, end=" ")

def generate_random_points(num_points):
    return [Point(str(i), random.randint(100, 800), random.randint(15, 400)) for i in range(num_points)]

def animate(canvas, points):
    find_convex_hull(points, canvas)

def main():
    root = tk.Tk()
    root.title("Quick Elimination Convex Hull Animation")

    canvas = tk.Canvas(root, width=1000, height=430)
    canvas.pack()

    random_points = generate_random_points(30)

    # Draw random points on the canvas
    for point in random_points:
        canvas.create_oval(point.x - 2, point.y - 2, point.x + 2, point.y + 2, fill='blue')

    # Button to start the animation
    start_button = tk.Button(root, text="Start Animation", command=lambda: animate(canvas, random_points))
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
