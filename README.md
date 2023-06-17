# Inner-Boundary-Tracing-Algorithm

The Inner Boundary Tracing Algorithm is a widely used computer vision technique that is used to extract the boundary of an object in an image. This GitHub repository contains code and data for implementing the Inner Boundary Tracing Algorithm in Python.

## Project Description

The project aims to extract the boundary of an object in an image using the Inner Boundary Tracing Algorithm. The algorithm detects the edges of an object by tracing the boundary of its interior. The repository includes a PyQt application that allows the user to apply the algorithm on an image of their choice.

## Implementation

The Inner Boundary Tracing Algorithm is implemented in this project using Python and the OpenCV library. The algorithm works by first converting the image to grayscale, and then applying a binary threshold to create a binary image. The algorithm then selects a starting point on the boundary of the object and follows the inner boundary by traversing the pixels on the boundary. The algorithm stops when it reaches the starting point. The algorithm is implemented for 4-connectivity and 8 connectivity tracing.

## Screenshots

### The GUI

<img src="./screens/GUI.png">

### Applying the algorithm on a simple image

<img src="./screens/first_img.png">

<br>
<br>

<img src="./screens/second_img.png">

<br>
<br>

<img src="./screens/third_img.png">
