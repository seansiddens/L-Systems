import colorsys
import math
import numpy as np
import LindenmayerSystems as ls

if __name__ == '__main__':
    curves = []
    sierpinski_square = ls.SierpinskiSquare()
    curves.append(sierpinski_square)
    binary_tree = ls.BinaryTree()
    curves.append(binary_tree)
    koch_curve = ls.KochCurve()
    curves.append(koch_curve)
    sierpinski_triangle = ls.SierpinskiTriangle()
    curves.append(sierpinski_triangle)

    while True:
        choice = False
        while not choice:
            count = 0
            for curve in curves:
                count += 1
                name = curve.get_name()
                print("[{}]".format(count), name)

            choice = input()

            try:
                val = int(choice)
                if (val - 1) not in range(len(curves)):
                    print("Please input a valid number: ")
                    choice = False
            except ValueError:
                print("Please input a valid number:")
                choice = False

        curve = curves[int(choice)-1]

        choice = False
        while not choice:
            print("Please input order to render up to: ")

            choice = input()

            try:
                val = int(choice)
                if val < 0:
                    print("Please input a positive number: ")
                    choice = False
            except ValueError:
                print("Please input a valid number:")
                choice = False

        order = int(choice)
        curve.set_order(order)
        curve.generate()

        choice = False
        while not choice:
            print("Please input a drawing mode: ")
            print("[1] Draw curve")
            print("[2] Render curve")

            choice = input()

            try:
                val = int(choice)
                if val < 0:
                    print("Please input a positive number: ")
                    choice = False
            except ValueError:
                print("Please input a valid number:")
                choice = False

        if int(choice) == 1:
            curve.draw()
        elif int(choice) == 2:
            curve.render()

