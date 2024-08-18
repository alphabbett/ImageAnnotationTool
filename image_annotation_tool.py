import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# Initialize tkinter
root = tk.Tk()
root.title("Wayne Metcalf - CV Image Annotation Tool")

# Set dark theme colors
bg_color = "#2E2E2E"
fg_color = "#FFFFFF"
btn_bg_color = "#444444"
btn_fg_color = "#FFFFFF"
highlight_color = "#FFD700"

root.configure(bg=bg_color)
root.state('zoomed')  # Maximize the window

# Style configurations
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background=btn_bg_color, foreground=btn_fg_color, font=("Helvetica", 10), padding=5)
style.map("TButton", background=[("active", highlight_color)])
style.configure("SelectedButton.TButton", background=highlight_color, foreground=fg_color)

# Default directories
default_images_dir = r"C:\Users\CurrentUser\Pictures"
default_labels_dir = r"C:\Users\CurrentUser\Pictures"
default_approved_images_dir = r"C:\Users\CurrentUser\Pictures"
default_approved_labels_dir = r"C:\Users\CurrentUser\Pictures"
default_rejected_images_dir = r"C:\Users\CurrentUser\Pictures"
default_rejected_labels_dir = r"C:\Users\CurrentUser\Pictures"

# Initialize directories with default values
images_dir = default_images_dir
labels_dir = default_labels_dir
approved_images_dir = default_approved_images_dir
approved_labels_dir = default_approved_labels_dir
rejected_images_dir = default_rejected_images_dir
rejected_labels_dir = default_rejected_labels_dir

# Global variables for image handling
image_files = []
current_image_index = 0
annotations = []
current_annotation = None
drawing = False
start_x = start_y = 0
current_rect = None
class_buttons = {}  # Dictionary to keep track of class buttons

# Class ID to name mapping
class_names = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6"
}

# Reverse class names for easy lookup
class_name_to_id = {v: k for k, v in class_names.items()}

# Function to select directories
def select_images_directory():
    global images_dir, image_files, current_image_index
    images_dir = filedialog.askdirectory(title="Select Images Directory")
    if images_dir:
        image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('jpg', 'jpeg', 'png'))])
        current_image_index = 0  # Reset index when a new directory is selected
    update_directories()

def select_labels_directory():
    global labels_dir
    labels_dir = filedialog.askdirectory(title="Select Labels Directory")
    update_directories()

def select_approved_images_directory():
    global approved_images_dir
    approved_images_dir = filedialog.askdirectory(title="Select Approved Images Directory")
    update_directories()

def select_approved_labels_directory():
    global approved_labels_dir
    approved_labels_dir = filedialog.askdirectory(title="Select Approved Labels Directory")
    update_directories()

def select_rejected_images_directory():
    global rejected_images_dir
    rejected_images_dir = filedialog.askdirectory(title="Select Rejected Images Directory")
    update_directories()

def select_rejected_labels_directory():
    global rejected_labels_dir
    rejected_labels_dir = filedialog.askdirectory(title="Select Rejected Labels Directory")
    update_directories()

def update_directories():
    global images_dir, labels_dir, approved_images_dir, approved_labels_dir, rejected_images_dir, rejected_labels_dir
    
    print(f"Images dir: {images_dir}")
    print(f"Labels dir: {labels_dir}")
    print(f"Approved images dir: {approved_images_dir}")
    print(f"Approved labels dir: {approved_labels_dir}")
    print(f"Rejected images dir: {rejected_images_dir}")
    print(f"Rejected labels dir: {rejected_labels_dir}")
    
    if all([images_dir, labels_dir, approved_images_dir, approved_labels_dir, rejected_images_dir, rejected_labels_dir]):
        print("All directories selected. Enabling start button.")
        # Ensure directories exist
        for directory in [approved_images_dir, approved_labels_dir, rejected_images_dir, rejected_labels_dir]:
            os.makedirs(directory, exist_ok=True)
        start_button.config(state=tk.NORMAL)  # Enable the start button
    else:
        print("Not all directories selected. Start button remains disabled.")
        start_button.config(state=tk.DISABLED)

def start_annotation_tool():
    global image_files

    # Automatically use the default directories if they are set
    update_directories()

    if images_dir:
        image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('jpg', 'jpeg', 'png'))])
        if image_files:
            load_image(0)
        else:
            messagebox.showinfo("Info", "No images found in the selected directory.")
    else:
        messagebox.showinfo("Info", "Please select an images directory first.")

def read_annotations(label_path):
    annotations = []
    if os.path.exists(label_path):
        print(f"Reading annotations from {label_path}")
        with open(label_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id = int(parts[0])
                    x_center, y_center, width, height = map(float, parts[1:])
                    annotations.append((class_id, x_center, y_center, width, height))
                    print(f"Read annotation: class={class_id}, coords=({x_center},{y_center},{width},{height})")
                else:
                    print(f"Skipped invalid line: {line.strip()}")
    else:
        print(f"Label file not found: {label_path}")
    return annotations

def save_annotations(label_path, annotations):
    with open(label_path, 'w') as file:
        for annotation in annotations:
            line = f"{annotation[0]} {annotation[1]:.6f} {annotation[2]:.6f} {annotation[3]:.6f} {annotation[4]:.6f}\n"
            file.write(line)

def draw_annotations_on_image(image, annotations):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    height, width = img.shape[:2]
    print(f"Number of annotations: {len(annotations)}")
    for annotation in annotations:
        class_id, x_center, y_center, box_width, box_height = annotation
        x1 = int((x_center - box_width/2) * width)
        y1 = int((y_center - box_height/2) * height)
        x2 = int((x_center + box_width/2) * width)
        y2 = int((y_center + box_height/2) * height)
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)  # Reduced line width to 1
        class_name = class_names.get(class_id, "Unknown")
        cv2.putText(img, class_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)  # Reduced font scale and thickness
        print(f"Drew annotation: class={class_name}, coords=({x1},{y1},{x2},{y2})")
    
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def resize_and_display_image():
    global photo, annotated_image
    
    if 'annotated_image' not in globals() or annotated_image is None:
        if 'image' in globals() and image is not None:
            annotated_image = image.copy()
        else:
            return  # Do nothing if neither annotated_image nor image is defined
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if canvas_width <= 1 or canvas_height <= 1:
        return

    # Calculate scaling factor
    img_width, img_height = annotated_image.size
    scale = min(canvas_width / img_width, canvas_height / img_height)
    
    # Calculate new dimensions
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    
    # Resize the image
    resized_image = annotated_image.resize((new_width, new_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    
    # Clear canvas and display the image
    canvas.delete("all")
    canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=photo)

def load_image(index):
    global current_image_index, annotations, image, annotated_image
    if not image_files or index >= len(image_files):
        messagebox.showinfo("Info", "No more images.")
        return

    current_image_index = index
    img_path = os.path.join(images_dir, image_files[index])
    label_path = os.path.join(labels_dir, image_files[index].rsplit('.', 1)[0] + ".txt")

    print(f"Loading image: {img_path}")
    print(f"Looking for label file: {label_path}")

    image = Image.open(img_path)
    annotations = read_annotations(label_path)
    
    print(f"Loaded {len(annotations)} annotations")
    
    # Draw annotations directly on the image
    annotated_image = draw_annotations_on_image(image, annotations)

    resize_and_display_image()
    root.title(f"Wayne - Simple Annotation Tool - {index + 1}/{len(image_files)}")

def approve_image():
    global current_image_index
    if current_image_index >= len(image_files):
        return  # No more images to approve

    img_name = image_files[current_image_index]
    label_name = img_name.rsplit('.', 1)[0] + ".txt"
    
    # Source paths
    img_src = os.path.join(images_dir, img_name)
    label_src = os.path.join(labels_dir, label_name)
    
    # Destination paths
    img_dest = os.path.join(approved_images_dir, img_name)
    label_dest = os.path.join(approved_labels_dir, label_name)
    
    # Save current annotations
    if not os.path.exists(label_src):
        save_annotations(label_dest, annotations)
    else:
        save_annotations(label_src, annotations)
    
    try:
        # Move image and label file
        shutil.move(img_src, img_dest)
        if os.path.exists(label_src):
            shutil.move(label_src, label_dest)
    except Exception as e:
        print(f"Failed to move files: {str(e)}")  # Print error message to console
    
    current_image_index += 1
    load_image(current_image_index)

def reject_image():
    global current_image_index
    if current_image_index >= len(image_files):
        return  # No more images to reject

    img_name = image_files[current_image_index]
    label_name = img_name.rsplit('.', 1)[0] + ".txt"
    
    # Source paths
    img_src = os.path.join(images_dir, img_name)
    label_src = os.path.join(labels_dir, label_name)
    
    # Destination paths
    img_dest = os.path.join(rejected_images_dir, img_name)
    label_dest = os.path.join(rejected_labels_dir, label_name)
    
    # Save current annotations
    if not os.path.exists(label_src):
        save_annotations(label_dest, annotations)
    else:
        save_annotations(label_src, annotations)
    
    try:
        # Move image and label file
        shutil.move(img_src, img_dest)
        if os.path.exists(label_src):
            shutil.move(label_src, label_dest)
    except Exception as e:
        print(f"Failed to move files: {str(e)}")  # Print error message to console
    
    current_image_index += 1
    load_image(current_image_index)

def move_image_and_label(target_image_dir, target_label_dir):
    img_name = image_files[current_image_index]
    label_name = img_name.rsplit('.', 1)[0] + ".txt"
    
    img_src = os.path.join(images_dir, img_name)
    label_src = os.path.join(labels_dir, label_name)
    
    img_dest = os.path.join(target_image_dir, img_name)
    label_dest = os.path.join(target_label_dir, label_name)
    
    if not os.path.exists(label_src):
        save_annotations(label_dest, annotations)
    shutil.move(img_src, img_dest)
    if os.path.exists(label_src):
        shutil.move(label_src, label_dest)

def previous_image():
    if current_image_index > 0:
        load_image(current_image_index - 1)

def next_image():
    if current_image_index < len(image_files) - 1:
        load_image(current_image_index + 1)

def start_annotation(event):
    global start_x, start_y, drawing, current_rect
    if current_class_id is not None:
        start_x, start_y = event.x, event.y
        drawing = True
        current_rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="yellow", width=2)

def draw_annotation(event):
    global current_rect
    if drawing and current_rect:
        canvas.coords(current_rect, start_x, start_y, event.x, event.y)

def finish_annotation(event):
    global drawing, current_rect, annotated_image, annotations
    if drawing and current_class_id is not None:
        end_x, end_y = event.x, event.y
        drawing = False
        if start_x != end_x and start_y != end_y:
            class_id = current_class_id
            
            # Convert canvas coordinates to image coordinates
            img_width, img_height = image.size
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            scale = min(canvas_width / img_width, canvas_height / img_height)
            
            # Calculate coordinates relative to the image
            adj_start_x = (start_x - (canvas_width - img_width * scale) / 2) / scale
            adj_start_y = (start_y - (canvas_height - img_height * scale) / 2) / scale
            adj_end_x = (end_x - (canvas_width - img_width * scale) / 2) / scale
            adj_end_y = (end_y - (canvas_height - img_height * scale) / 2) / scale

            # Calculate annotation in normalized coordinates
            x_center = (adj_start_x + adj_end_x) / 2 / img_width
            y_center = (adj_start_y + adj_end_y) / 2 / img_height
            width = abs(adj_end_x - adj_start_x) / img_width
            height = abs(adj_end_y - adj_start_y) / img_height
            
            annotations.append((class_id, x_center, y_center, width, height))
            print(f"Added annotation: class={class_id}, coords=({x_center},{y_center},{width},{height})")
            
            # Redraw annotations on the image
            annotated_image = draw_annotations_on_image(image, annotations)
            resize_and_display_image()
        
        if current_rect:
            canvas.delete(current_rect)
        current_rect = None


def remove_annotations():
    global annotations, annotated_image
    annotations = []
    annotated_image = draw_annotations_on_image(image, annotations)
    resize_and_display_image()

def create_class_button(class_id, class_name):
    button = ttk.Button(class_frame, text=class_name, 
                        command=lambda: set_current_class(class_id, button))
    class_buttons[class_id] = button  # Store button reference
    return button

def set_current_class(class_id, button):
    global current_class_id
    
    # Reset all buttons to default color
    for btn in class_buttons.values():
        btn.config(style="TButton")
    
    # Set selected button to yellow
    button.config(style="SelectedButton.TButton")
    current_class_id = class_id

# Setup GUI components
canvas = tk.Canvas(root, bg=bg_color)
canvas.pack(side="top", fill="both", expand="yes")

# Frame for directory selection buttons
dir_frame = tk.Frame(root, bg=bg_color)
dir_frame.pack(side="bottom", fill="x", expand="no")

# Frame for class buttons
class_frame = tk.Frame(root, bg=bg_color)
class_frame.pack(side="bottom", fill="x", expand="no")

# Button frame for image annotation actions
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(side="bottom", fill="x", expand="no")

# Place all directory selection buttons in a single row inside dir_frame
ttk.Button(dir_frame, text="Select Images Directory", command=select_images_directory).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(dir_frame, text="Select Labels Directory", command=select_labels_directory).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(dir_frame, text="Select Approved Images Directory", command=select_approved_images_directory).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(dir_frame, text="Select Approved Labels Directory", command=select_approved_labels_directory).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(dir_frame, text="Select Rejected Images Directory", command=select_rejected_images_directory).grid(row=0, column=4, padx=5, pady=5)
ttk.Button(dir_frame, text="Select Rejected Labels Directory", command=select_rejected_labels_directory).grid(row=0, column=5, padx=5, pady=5)

# Add Start button after the directory buttons in dir_frame
start_button = ttk.Button(dir_frame, text="Start", command=start_annotation_tool, state=tk.DISABLED)
start_button.grid(row=0, column=6, padx=5, pady=5)

# Create buttons for each class in class_frame
for i, (class_id, class_name) in enumerate(class_names.items()):
    btn = create_class_button(class_id, class_name)
    btn.grid(row=0, column=i, sticky="ew", in_=class_frame)

# Action buttons in btn_frame
approve_btn = ttk.Button(btn_frame, text="Approve", command=approve_image)
approve_btn.grid(row=0, column=0, sticky="ew")

reject_btn = ttk.Button(btn_frame, text="Reject", command=reject_image)
reject_btn.grid(row=0, column=1, sticky="ew")

prev_btn = ttk.Button(btn_frame, text="Previous", command=previous_image)
prev_btn.grid(row=0, column=2, sticky="ew")

next_btn = ttk.Button(btn_frame, text="Next", command=next_image)
next_btn.grid(row=0, column=3, sticky="ew")

remove_ann_btn = ttk.Button(btn_frame, text="Remove Annotations", command=remove_annotations)
remove_ann_btn.grid(row=0, column=4, sticky="ew")

# Initialize current class variables
current_class_id = None

# Bind the configure event to resize the image when the window is resized
canvas.bind("<Configure>", lambda event: resize_and_display_image())
canvas.bind("<Button-1>", start_annotation)
canvas.bind("<B1-Motion>", draw_annotation)
canvas.bind("<ButtonRelease-1>", finish_annotation)

# Call update_directories() once after the button is defined
update_directories()

# Start the GUI loop
root.mainloop()
