from rembg import remove
from PIL import Image, ImageChops
import tkinter as tk
from tkinter import filedialog

def choose_front_image():
    front_path = filedialog.askopenfilename(title="Select front image file")
    front_entry.delete(0, tk.END)
    front_entry.insert(0, front_path)

def choose_back_image():
    back_path = filedialog.askopenfilename(title="Select back image file")
    back_entry.delete(0, tk.END)
    back_entry.insert(0, back_path)

def crop_to_content(image):
    bbox = image.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

def combine_images():
    front_path = front_entry.get()
    back_path = back_entry.get()

    front_image = Image.open(front_path)
    front_transparent = remove(front_image)

    back_image = Image.open(back_path)
    back_transparent = remove(back_image)

    front_cropped = crop_to_content(front_transparent)
    back_cropped = crop_to_content(back_transparent)

    max_height = max(front_cropped.height, back_cropped.height)

    background_width = front_cropped.width + back_cropped.width
    background_height = max_height
    background = Image.new("RGB", (background_width, background_height), "white")

    paste_position_front = (0, (background_height - front_cropped.height) // 2)
    background.paste(front_cropped, paste_position_front, front_cropped)

    paste_position_back = (front_cropped.width, (background_height - back_cropped.height) // 2)
    background.paste(back_cropped, paste_position_back, back_cropped)

    background.save("combined_images.png")

    combined_image = Image.open("combined_images.png")
    combined_image.show()

    front_entry.delete(0, tk.END)
    back_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Background Remover")

window_width = 500
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

front_button = tk.Button(root, text="Front Of Coin", command=choose_front_image)
front_button.place(x=50, y=100)

back_button = tk.Button(root, text="Back Of Coin", command=choose_back_image)
back_button.place(x=50, y=150)

preview_button = tk.Button(root, text="Show Preview", command=combine_images)
preview_button.place(x=50, y=200)

front_entry = tk.Entry(root, width=50)
front_entry.place(x=140, y=105)

back_entry = tk.Entry(root, width=50)
back_entry.place(x=140, y=155)

root.mainloop()