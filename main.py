import numpy as np
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import cv2
import copy
from matplotlib.figure import Figure
from sympy import EX, false
from maingui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.browse_button.clicked.connect(self.browse)
        self.ui.apply_button.clicked.connect(
            self.check_algorithm_selected)

        # variables
        self.original_image_figure = Figure()
        self.original_canvas_figure = FigureCanvas(self.original_image_figure)
        self.ui.verticalLayout.addWidget(self.original_canvas_figure)

        self.final_image_figure = Figure()
        self.final_canvas_figure = FigureCanvas(self.final_image_figure)
        self.ui.verticalLayout_2.addWidget(self.final_canvas_figure)

        self.left_most_value = [0, 0]
        self.next_point = [0, 0]
        self.boundary_points = []

    def browse(self):
        try:
            imported_image = QFileDialog.getOpenFileName(
                filter="image (*.png *.jpg *.jpeg)")[0]
            self.image = cv2.imread(imported_image, 0)
            # change the image to grayscale by passing the flag 0 to cv2.imread()
            ret, self.image = cv2.threshold(
                self.image, 127, 255, cv2.THRESH_BINARY)
            # then if the image is not binary change it to binary
            self.rows, self.cols = self.image.shape
            self.show_image(self.original_image_figure,
                            self.original_canvas_figure, self.image)
            self.final_image_figure.clear()
            self.final_canvas_figure.draw()
            self.final_canvas_figure.flush_events()
        except Exception as e:
            print(e)

    def apply_algorithm_4_connectivity(self):
        try:
            self.boundary_points = []
            self.new_image = np.zeros(self.image.shape)
            self.find_left_most_point()
            self.dir = 3
            while(True):
                row_left_most = self.left_most_value[0]
                column_left_most = self.left_most_value[1]
                self.dir = (self.dir + 3) % 4
                self.flag_4 = True
                while(self.flag_4):
                    if self.dir == 0:

                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most + 1

                        self.check_valid_image_bounadries(4)

                    elif self.dir == 1:
                        # go up
                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most

                        self.check_valid_image_bounadries(4)

                    elif self.dir == 2:
                        # go left
                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most - 1

                        self.check_valid_image_bounadries(4)

                    elif self.dir == 3:
                        # go down

                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most

                        self.check_valid_image_bounadries(4)

                if len(self.boundary_points) >= 4:
                    if self.boundary_points[-1] == self.boundary_points[1]:
                        if self.boundary_points[-2] == self.boundary_points[0]:
                            break

            for boundary in self.boundary_points:
                self.new_image[boundary[0]][boundary[1]] = 255
            self.show_image(self.final_image_figure,
                            self.final_canvas_figure, self.new_image)
        except Exception as e:
            print(e)

    def apply_algorithm_8_connectivity(self):
        try:

            self.boundary_points = []
            self.new_image = np.zeros(self.image.shape)
            self.find_left_most_point()
            self.dir = 7

            while(True):
                row_left_most = self.left_most_value[0]
                column_left_most = self.left_most_value[1]
                # even
                if self.dir % 2 == 0:
                    self.dir = (self.dir + 7) % 8
                # odd
                else:
                    self.dir = (self.dir + 6) % 8

                self.flag_8 = True
                while(self.flag_8):

                    if self.dir == 0:
                        # go right
                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most + 1

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 1:

                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most + 1

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 2:
                        # go up
                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 3:
                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most - 1

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 4:
                        # go left
                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most - 1

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 5:
                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most - 1

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 6:
                        # go down

                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most

                        self.check_valid_image_bounadries(8)

                    elif self.dir == 7:
                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most + 1

                        self.check_valid_image_bounadries(8)

                if len(self.boundary_points) >= 4:
                    if self.boundary_points[-1] == self.boundary_points[1]:
                        if self.boundary_points[-2] == self.boundary_points[0]:
                            break

            for boundary in self.boundary_points:
                self.new_image[boundary[0]][boundary[1]] = 255
            self.show_image(self.final_image_figure,
                            self.final_canvas_figure, self.new_image)

        except Exception as e:
            print(e)

    def check_algorithm_selected(self):
        # check the current index of the combo box
        algo_index = self.ui.comboBox.currentIndex()
        if algo_index == 0:
            self.apply_algorithm_4_connectivity()
        elif algo_index == 1:
            self.apply_algorithm_8_connectivity()

    def find_left_most_point(self):
        for col in range(self.cols+1):
            for row in range(col+1):
                if self.image[row][col-row] == 255:
                    # found the first boundary point
                    self.left_most_value = [row, col - row]
                    self.boundary_points.append(self.left_most_value)
                    return

    def show_image(self, figure, canvas, image):
        figure.clear()
        figure_axes = figure.gca()
        figure_axes.imshow(image, cmap='gray')
        figure_axes.set_xticks([])
        figure_axes.set_yticks([])
        figure.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
        canvas.draw()
        canvas.flush_events()

    def check_valid_image_bounadries(self, connectivity):
        # check if the next point is in the image frame
        if (self.next_point[1] > self.cols - 1) or (self.next_point[0] < 0) or (self.next_point[1] < 0) or (self.next_point[0] > self.rows - 1):
            self.dir = (self.dir + 1) % connectivity
        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
            self.left_most_value = copy.deepcopy(
                self.next_point)
            self.boundary_points.append(self.left_most_value)
            self.flag_8 = false
            self.flag_4 = false
        else:
            self.dir = (self.dir + 1) % connectivity


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
