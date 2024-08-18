# ImageAnnotationTool
Image Annotation Tool - For Large Data Sets. (Computer Vision)
Wayne Metcalf - CV Image Annotation Tool
Overview
For Large datasets. This script does not cachethe whole catalogue of images into memory, it loads one at a time from a specified directory, so you can annotate many thousands of images without memory issues.
The CV Image Annotation Tool is a graphical user interface (GUI) application for annotating images with bounding boxes. This tool is particularly useful for preparing datasets for computer vision tasks. It allows users to view images, draw bounding boxes around objects, and classify these objects into predefined classes. The application also supports moving images to approved or rejected directories based on their annotation quality.  

Features
Image Display: View images with their annotations.
Annotation Drawing: Draw bounding boxes on images to label objects.
Class Management: Annotate objects with predefined class labels.
Directory Management: Select directories for images, labels, and sorting them into approved or rejected categories.
File Operations: Move images and labels to different directories based on their annotation status.
Prerequisites
Before running the application, ensure you have the following Python packages installed:

Pillow for image handling
opencv-python for image processing
numpy for numerical operations
tkinter for the GUI
You can install these dependencies using pip:

```bash
pip install Pillow opencv-python numpy
```
Note: tkinter is included with Python's standard library, but if it's missing, you can install it via your package manager.

Setup
Clone the Repository:

```bash
git clone https://github.com/alphabbett/ImageAnnotationTool.git
cd ImageAnnotationTool
```
Install Dependencies:
Ensure you have Python installed, then install the necessary packages:

```bash
pip install Pillow opencv-python numpy
```
Usage
Run the Application:

Execute the Python script to launch the GUI:

```bash
python annotation_tool.py
```
Select Directories:

Use the buttons in the GUI to select directories for images, labels, and directories for approved/rejected images and labels.

Start Annotation:

Click the "Start" button to begin annotating images. The tool will load images from the selected directory and display them.

Annotate Images:

Select a class by clicking on one of the class buttons.
Draw bounding boxes around objects by clicking and dragging on the image.
Finish drawing by releasing the mouse button.
Approve/Reject Images:

Use the "Approve" or "Reject" buttons to move the current image and its associated label to the approved or rejected directories, respectively.

Navigate Images:

Use the "Previous" and "Next" buttons to navigate through the images.
Click "Remove Annotations" to clear all annotations from the current image.
Directory Structure
Images Directory: Directory containing the images to annotate.
Labels Directory: Directory containing label files corresponding to the images.
Approved Images Directory: Directory where approved images will be moved.
Approved Labels Directory: Directory where approved label files will be moved.
Rejected Images Directory: Directory where rejected images will be moved.
Rejected Labels Directory: Directory where rejected label files will be moved.
Code Explanation
select_images_directory(): Opens a dialog to select the directory containing images.
select_labels_directory(): Opens a dialog to select the directory containing labels.
start_annotation_tool(): Initializes the annotation process and loads the first image.
draw_annotations_on_image(): Draws annotations on the image using OpenCV.
resize_and_display_image(): Adjusts the image size to fit the canvas and displays it.
approve_image(): Moves the current image and label to the approved directories.
reject_image(): Moves the current image and label to the rejected directories.
Contributing
Contributions to improve the tool are welcome. Please fork the repository and submit pull requests with your changes.

