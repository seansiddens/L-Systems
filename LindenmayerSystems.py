import colorsys
import numpy as np
import math
import turtle
import colorsys
import pyglet
from pyglet import shapes


def rotate(point, angle):
    px, py = point

    qx = (px * math.cos(angle)) - (py * math.sin(angle))
    qy = (px * math.sin(angle)) + (py * math.cos(angle))
    return qx, qy


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


class SierpinskiSquare:
    def __init__(self, order=0):
        self.name = "Sierpinski Square Curve"
        self.angle = math.pi / 2                       # must be in radians
        self.axiom = "F+XF+F+XF"                       # initial string to begin construction
        self.rules = [["X", "XF-F+F-XF+F+XF-F+F-X"]]   # production rules
        self.sentence = ""                             # resulting string from generating from axiom using rules
        self.order = order

    def generate(self, order=None):
        if order is None:
            order = self.order

        if order == 0:
            self.sentence = self.axiom
        else:
            sentence = self.generate(order-1)
            next_sentence = ""
            for char in self.sentence:
                found = False
                for rule in self.rules:
                    if char == rule[0]:
                        found = True
                        next_sentence += rule[1]
                        break
                if not found:
                    next_sentence += char

            sentence = next_sentence
            self.sentence = sentence

    def draw(self, scr_dim=800):
        draw_area = scr_dim * 0.9

        # screen setup
        screen = turtle.getscreen()
        screen.setup(scr_dim, scr_dim)
        screen.bgcolor('black')
        screen.setworldcoordinates(-1, -1, scr_dim, scr_dim)

        length = draw_area / (1 + 4 * pow(2, self.order))

        t = turtle.Turtle()
        t.color('white')
        color_step = 1 / len(self.sentence)
        t.hideturtle()
        t.speed('fastest')

        t.penup()
        t.setpos(((scr_dim - draw_area) / 2) + ((draw_area / 2) - (length / 2)), (scr_dim - draw_area) / 2)
        t.setheading(0)
        t.pendown()

        color_count = 1
        for char in self.sentence:
            t.color(colorsys.hsv_to_rgb(color_step*color_count, 1.0, 1.0))

            if char == 'F':
                t.forward(length)
            elif char == '-':
                t.right(math.degrees(self.angle))
            elif char == '+':
                t.left(math.degrees(self.angle))
            else:
                pass

            color_count += 1

        turtle.Screen().exitonclick()

    def render(self, scr_dim=800):
        window = pyglet.window.Window(scr_dim, scr_dim)
        draw_area = scr_dim * 0.9
        length = draw_area / (1 + 4 * pow(2, self.order))
        batch = pyglet.graphics.Batch()

        start_point = (((scr_dim - draw_area) / 2) + ((draw_area / 2) - (length / 2)), (scr_dim - draw_area) / 2)
        lines = []
        unit_vec = (1, 0)
        vec = start_point
        color_count = 1
        color_step = 1 / len(self.sentence)
        for char in self.sentence:
            if char == 'F':
                # draw forward - multiply unit vector by length
                prev_vec = vec
                vec = np.multiply(length, unit_vec) + vec
                color = hsv2rgb(color_step*color_count, 1.0, 1.0)
                color_count += 1
                new_line = shapes.Line(prev_vec[0], prev_vec[1], vec[0], vec[1], batch=batch, color=color)
                lines.append(new_line)
            elif char == '-':
                # turn right - rotate unit vector clockwise
                unit_vec = rotate(unit_vec, (2 * math.pi) - (math.pi / 2))
            elif char == '+':
                # turn left - rotate unit vector counter-clockwise
                unit_vec = rotate(unit_vec, math.pi / 2)
            else:
                pass

        @window.event()
        def on_draw():
            window.clear()
            batch.draw()

        pyglet.app.run()

    # getters
    def set_order(self, order): self.order = order

    # setters
    def get_sentence(self): return self.sentence
    def get_order(self): return self.order
    def get_name(self): return self.name


class BinaryTree:
    def __init__(self, order=0):
        self.name = "Binary Tree"
        self.angle = math.pi / 4                     # must be in radians
        self.axiom = "0"                             # initial string to begin construction
        self.rules = [["1", "11"], ["0", "1[0]0"]]   # production rules
        self.sentence = ""                           # resulting string from generating from axiom using rules
        self.order = order

    def generate(self, order=None):
        if order is None:
            order = self.order

        if order == 0:
            self.sentence = self.axiom
        else:
            sentence = self.generate(order-1)
            next_sentence = ""
            for char in self.sentence:
                found = False
                for rule in self.rules:
                    if char == rule[0]:
                        found = True
                        next_sentence += rule[1]
                        break
                if not found:
                    next_sentence += char

            sentence = next_sentence
            self.sentence = sentence

    def draw(self, scr_dim=800):
        draw_area = scr_dim * 0.9

        # screen setup
        screen = turtle.getscreen()
        screen.setup(scr_dim, scr_dim)
        screen.bgcolor('black')
        screen.setworldcoordinates(-1, -1, scr_dim, scr_dim)

        count = 1
        for char in self.sentence:
            if char != '1':
                break

            count += 1

        length = scr_dim / count / 2

        t = turtle.Turtle()
        t.color('white')
        color_step = 1 / len(self.sentence)
        t.hideturtle()
        t.speed('fastest')

        t.penup()
        t.setpos(scr_dim / 2, 0)
        t.setheading(90)
        t.pendown()

        color_count = 1
        stack = []
        t.color(colorsys.hsv_to_rgb(color_step * color_count, 1.0, 1.0))
        for char in self.sentence:

            if char == '0' or char == '1':
                # draw line segment
                color_count += 1
                t.forward(length)
            elif char == '[':
                # push position and angle, turn counter clockwise
                pos = [t.pos(), t.heading(), color_count]
                stack.append(pos)
                t.left(math.degrees(self.angle))
            elif char == ']':
                # pop position and angle, turn clockwise
                pos = stack.pop()
                color_count = pos[2]
                t.penup()
                t.setpos(pos[0])
                t.setheading(pos[1])
                t.pendown()
                t.right(math.degrees(self.angle))
            else:
                pass

            t.color(colorsys.hsv_to_rgb(color_step*color_count, 1.0, 1.0))

        turtle.Screen().exitonclick()

    def render(self, scr_dim=800):
        window = pyglet.window.Window(scr_dim, scr_dim)
        draw_area = scr_dim * 0.9

        count = 1
        for char in self.sentence:
            if char != '1':
                break

            count += 1

        length = scr_dim / count / 2

        batch = pyglet.graphics.Batch()

        start_point = (scr_dim / 2, 0)
        lines = []
        unit_vec = (0, 1)
        vec = start_point
        color_count = 1
        color_step = 1 / len(self.sentence)
        stack = []
        for char in self.sentence:
            if char == '0' or char == '1':
                # draw forward - multiply unit vector by length
                prev_vec = vec
                vec = np.multiply(length, unit_vec) + vec
                color = hsv2rgb(color_step*color_count, 1.0, 1.0)
                color_count += 1
                new_line = shapes.Line(prev_vec[0], prev_vec[1], vec[0], vec[1], batch=batch, color=color)
                lines.append(new_line)
            elif char == '[':
                # push position and angle, turn counter clockwise
                pos = [vec, unit_vec]
                stack.append(pos)
                unit_vec = rotate(unit_vec, self.angle)
            elif char == ']':
                # pop position and angle, turn clockwise
                pos = stack.pop()
                vec = pos[0]
                unit_vec = pos[1]
                unit_vec = rotate(unit_vec, (2 * math.pi) - self.angle)
            else:
                pass

        @window.event()
        def on_draw():
            window.clear()
            batch.draw()

        pyglet.app.run()

    # getters
    def set_order(self, order): self.order = order

    # setters
    def get_sentence(self): return self.sentence
    def get_order(self): return self.order
    def get_name(self): return self.name


class KochCurve:
    def __init__(self, order=0):
        self.name = "Koch Curve"
        self.angle = math.pi / 3
        self.axiom = "F"
        self.rules = [["F", "F+F--F+F"]]
        self.sentence = ""
        self.order = order

    def generate(self, order=None):
        if order is None:
            order = self.order

        if order == 0:
            self.sentence = self.axiom
        else:
            sentence = self.generate(order-1)
            next_sentence = ""
            for char in self.sentence:
                found = False
                for rule in self.rules:
                    if char == rule[0]:
                        found = True
                        next_sentence += rule[1]
                        break
                if not found:
                    next_sentence += char

            sentence = next_sentence
            self.sentence = sentence

    def draw(self, scr_dim=800):
        draw_area = scr_dim * 0.9

        # screen setup
        screen = turtle.getscreen()
        screen.setup(scr_dim, scr_dim)
        screen.bgcolor('black')
        screen.setworldcoordinates(-1, -1, scr_dim, scr_dim)

        length = draw_area / pow(3, self.order)

        t = turtle.Turtle()
        t.color('white')
        color_step = 1 / len(self.sentence)
        t.hideturtle()
        t.speed('fastest')

        t.penup()
        t.setpos(5, scr_dim - draw_area)
        t.setheading(0)
        t.pendown()

        color_count = 1
        for char in self.sentence:
            t.color(colorsys.hsv_to_rgb(color_step*color_count, 1.0, 1.0))

            if char == 'F':
                t.forward(length)
            elif char == '-':
                t.right(math.degrees(self.angle))
            elif char == '+':
                t.left(math.degrees(self.angle))
            else:
                pass

            color_count += 1

        turtle.Screen().exitonclick()

    def render(self, scr_dim=800):
        window = pyglet.window.Window(scr_dim, 800)
        draw_area = scr_dim * 0.9
        length = draw_area / pow(3, self.order)
        batch = pyglet.graphics.Batch()

        start_point = (5, scr_dim - draw_area)
        lines = []
        unit_vec = (1, 0)
        vec = start_point
        color_count = 1
        color_step = 1 / len(self.sentence)
        for char in self.sentence:
            if char == 'F':
                # draw forward - multiply unit vector by length
                prev_vec = vec
                vec = np.multiply(length, unit_vec) + vec
                color = hsv2rgb(color_step*color_count, 1.0, 1.0)
                color_count += 1
                new_line = shapes.Line(prev_vec[0], prev_vec[1], vec[0], vec[1], batch=batch, color=color)
                lines.append(new_line)
            elif char == '-':
                # turn right - rotate unit vector clockwise
                unit_vec = rotate(unit_vec, (2 * math.pi) - self.angle)
            elif char == '+':
                # turn left - rotate unit vector counter-clockwise
                unit_vec = rotate(unit_vec, self.angle)
            else:
                pass

        @window.event()
        def on_draw():
            window.clear()
            batch.draw()

        pyglet.app.run()

    # getters
    def set_order(self, order): self.order = order

    # setters
    def get_sentence(self): return self.sentence
    def get_order(self): return self.order
    def get_name(self): return self.name


class SierpinskiTriangle:
    def __init__(self, order=0):
        self.name = "Sierpinski Triangle"
        self.angle = np.deg2rad(120)
        self.axiom = "F-G-G"
        self.rules = [["F", "F-G+F+G-F"], ["G", "GG"]]
        self.sentence = ""
        self.order = order

    def generate(self, order=None):
        if order is None:
            order = self.order

        if order == 0:
            self.sentence = self.axiom
        else:
            sentence = self.generate(order-1)
            next_sentence = ""
            for char in self.sentence:
                found = False
                for rule in self.rules:
                    if char == rule[0]:
                        found = True
                        next_sentence += rule[1]
                        break
                if not found:
                    next_sentence += char

            sentence = next_sentence
            self.sentence = sentence

    def draw(self, scr_dim=800):
        draw_area = scr_dim * 0.9

        # screen setup
        screen = turtle.getscreen()
        screen.setup(scr_dim, scr_dim)
        screen.bgcolor('black')
        screen.setworldcoordinates(-1, -1, scr_dim, scr_dim)

        if self.order == 0:
            length = scr_dim
        else:
            length = scr_dim / pow(2, self.order)

        t = turtle.Turtle()
        t.color('white')
        color_step = 1 / len(self.sentence)
        t.hideturtle()
        t.speed('fastest')

        t.penup()
        t.setpos(0, 0)
        t.setheading(90)
        t.pendown()

        color_count = 1
        for char in self.sentence:
            t.color(colorsys.hsv_to_rgb(color_step*color_count, 1.0, 1.0))

            if char == 'F' or char == 'G':
                t.forward(length)
            elif char == '-':
                t.right(math.degrees(self.angle))
            elif char == '+':
                t.left(math.degrees(self.angle))
            else:
                pass

            color_count += 1

        turtle.Screen().exitonclick()

    def render(self, scr_dim=800):
        window = pyglet.window.Window(scr_dim, 800)
        draw_area = scr_dim * 0.9
        if self.order == 0:
            length = scr_dim
        else:
            length = scr_dim / pow(2, self.order)
        batch = pyglet.graphics.Batch()

        start_point = (1, 1)
        lines = []
        unit_vec = (0, 1)
        vec = start_point
        color_count = 1
        color_step = 1 / len(self.sentence)
        for char in self.sentence:
            if char == 'F' or char == 'G':
                # draw forward - multiply unit vector by length
                prev_vec = vec
                vec = np.multiply(length, unit_vec) + vec
                color = hsv2rgb(color_step*color_count, 1.0, 1.0)
                color_count += 1
                new_line = shapes.Line(prev_vec[0], prev_vec[1], vec[0], vec[1], batch=batch, color=color)
                lines.append(new_line)
            elif char == '-':
                # turn right - rotate unit vector clockwise
                unit_vec = rotate(unit_vec, (2 * math.pi) - self.angle)
            elif char == '+':
                # turn left - rotate unit vector counter-clockwise
                unit_vec = rotate(unit_vec, self.angle)
            else:
                pass

        @window.event()
        def on_draw():
            window.clear()
            batch.draw()

        pyglet.app.run()

    # getters
    def set_order(self, order): self.order = order

    # setters
    def get_sentence(self): return self.sentence
    def get_order(self): return self.order
    def get_name(self): return self.name


class HilbertCurve:
    def __init__(self, order=0):
        self.name = "Hilbert Curve"
        self.angle = math.pi / 2
        self.axiom = "A"
        self.rules = [["A", "-BF+AFA+FB-"], ["B", "+AF-BFB-FA+"]]
        self.sentence = ""
        self.order = order

    def generate(self, order=None):
        if order is None:
            order = self.order

        if order == 0:
            self.sentence = self.axiom
        else:
            sentence = self.generate(order-1)
            next_sentence = ""
            for char in self.sentence:
                found = False
                for rule in self.rules:
                    if char == rule[0]:
                        found = True
                        next_sentence += rule[1]
                        break
                if not found:
                    next_sentence += char

            sentence = next_sentence
            self.sentence = sentence

    def draw(self, scr_dim=800):
        draw_area = scr_dim * 0.9

        # screen setup
        screen = turtle.getscreen()
        screen.setup(scr_dim, scr_dim)
        screen.bgcolor('black')
        screen.setworldcoordinates(-1, -1, scr_dim, scr_dim)

        length = scr_dim / pow(2, self.order)

        t = turtle.Turtle()
        t.color('white')
        color_step = 1 / len(self.sentence)
        t.hideturtle()
        t.speed('fastest')

        t.penup()
        t.setpos(5, 5)
        t.setheading(0)
        t.pendown()

        color_count = 1
        for char in self.sentence:
            t.color(colorsys.hsv_to_rgb(color_step*color_count, 1.0, 1.0))

            if char == 'F':
                t.forward(length)
            elif char == '-':
                t.left(math.degrees(self.angle))
            elif char == '+':
                t.right(math.degrees(self.angle))
            else:
                pass

            color_count += 1

        turtle.Screen().exitonclick()

    def render(self, scr_dim=800):
        window = pyglet.window.Window(scr_dim, 800)
        draw_area = scr_dim * 0.9
        length = scr_dim / pow(2, self.order)
        batch = pyglet.graphics.Batch()

        start_point = (length / 2, length / 2)
        lines = []
        unit_vec = (1, 0)
        vec = start_point
        color_count = 1
        color_step = 1 / len(self.sentence)
        for char in self.sentence:
            if char == 'F':
                # draw forward - multiply unit vector by length
                prev_vec = vec
                vec = np.multiply(length, unit_vec) + vec
                color = hsv2rgb(color_step*color_count, 1.0, 1.0)
                color_count += 1
                new_line = shapes.Line(prev_vec[0], prev_vec[1], vec[0], vec[1], batch=batch, color=color)
                lines.append(new_line)
            elif char == '-':
                # turn left - rotate unit vector counter-clockwise
                unit_vec = rotate(unit_vec, self.angle)
            elif char == '+':
                # turn right - rotate unit vector clockwise
                unit_vec = rotate(unit_vec, (2 * math.pi) - self.angle)
            else:
                pass

        @window.event()
        def on_draw():
            window.clear()
            batch.draw()

        pyglet.app.run()

    # getters
    def set_order(self, order): self.order = order

    # setters
    def get_sentence(self): return self.sentence
    def get_order(self): return self.order
    def get_name(self): return self.name
