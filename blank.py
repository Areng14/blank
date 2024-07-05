import os

import shutil

import sys

from PIL import Image

from tkinter import Tk, simpledialog, Toplevel, Label, BooleanVar

import tkinter.ttk as ttk  # Import standard ttk

from tqdm import tqdm

import tempfile



def resize_image(image, size):

    return image.resize(size)



def image_to_blank(image_path, blank_path, new_size=None, progress_callback=None):

    try:

        img = Image.open(image_path)

        if new_size:

            img = resize_image(img, new_size)

        width, height = img.size

        pixels = img.convert('RGB').getdata()



        with open(blank_path, 'w') as f:

            total_pixels = width * height

            for index, (r, g, b) in enumerate(tqdm(pixels, desc="Encrypting", unit="pixel")):

                f.write(' ' * r + '\t' + ' ' * g + '\t' + ' ' * b + '\t')

                if (index + 1) % width == 0:

                    f.write('\n')

                if progress_callback:

                    progress_callback(index + 1, total_pixels)

            f.write('\n')  # Ensure the file ends with a newline

    except Exception as e:

        print(f"Failed to convert image to .blank: {e}")



def blank_to_image(blank_path, output_path, progress_callback=None):

    try:

        with open(blank_path, 'r') as f:

            data = f.readlines()

        

        width = len(data[0].split('\t')) // 3

        height = len(data)

        

        pixels = []

        total_pixels = width * height

        pixel_count = 0

        for line in tqdm(data, desc="Decrypting", unit="line"):

            pixel_values = line.split('\t')

            for i in range(0, len(pixel_values) - 2, 3):

                r = len(pixel_values[i])

                g = len(pixel_values[i + 1])

                b = len(pixel_values[i + 2])

                pixels.append((r, g, b))

                pixel_count += 1

                if progress_callback:

                    progress_callback(pixel_count, total_pixels)

        

        img = Image.new('RGB', (width, height))

        img.putdata(pixels)

        img.save(output_path)

        print("Blank file decrypted and saved as image")

    except Exception as e:

        print(f"Failed to convert .blank to image: {e}")



def show_progress(title, task, ftitle):

    global progress_window

    progress_window = Toplevel()

    progress_window.title(title)

    progress_window.geometry('400x100')



    style = ttk.Style()

    style.configure("TProgressbar", thickness=30, troughcolor='#d9d9d9', background='#4caf50')



    progress_label = Label(progress_window, text=title, font=('Helvetica', 14))

    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=300, mode='determinate')

    progress_bar.pack(pady=10)

    

    def progress_callback(current, total):

        progress_bar['value'] = (current / total) * 100

        progress_window.update_idletasks()



    def run_task(callback):

        task(callback)

        progress_label.config(text=ftitle)

        progress_window.update_idletasks()



    def update_progress(callback, delay=100):

        progress_window.after(delay, run_task, callback)



    # Add 5-second delay before starting the progress bar

    progress_window.after(100, update_progress, progress_callback)

    progress_window.mainloop()



def main():

    root = Tk()

    root.withdraw()



    if len(sys.argv) != 2:

        print("Usage: blank_converter.py <path_to_file>")

        return

    

    input_path = sys.argv[1]

    file_ext = os.path.splitext(input_path)[1].lower()



    if not os.path.exists(input_path):

        print(f"File not found: {input_path}")

        return



    if file_ext in ['.png', '.jpg', '.jpeg']:

        blank_path = os.path.splitext(input_path)[0] + '.blank'

        resize_option = simpledialog.askstring("Resize Image", "Do you want to resize the image? (yes/no)", initialvalue="no")

        new_size = None

        if resize_option.lower() == 'yes':

            size_option = simpledialog.askstring("New Size", "Choose new size: 128x128 or 64x64", initialvalue="128x128")

            if size_option in ["128x128", "64x64"]:

                new_size = tuple(map(int, size_option.split('x')))

        

        def convert_image_to_blank(callback):

            image_to_blank(input_path, blank_path, new_size, callback)

            print(f"Image converted and saved as {blank_path}")

            root.quit()



        show_progress("Converting Image to .blank", convert_image_to_blank, "Conversion Complete")

    

    elif file_ext == '.blank':

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:

            output_path = tmp_file.name

        

            def convert_blank_to_image(callback):

                blank_to_image(input_path, output_path, callback)

                new_path = os.path.splitext(input_path)[0] + ".png"

                try:

                    os.remove(os.path.splitext(input_path)[0] + ".png")

                except:

                    print("Already has file... replacing")

                shutil.copy(output_path, new_path)

                os.remove(output_path)

                print(f"Image saved as {os.path.splitext(input_path)[0] + '.png'}")

                root.quit()

        show_progress("Converting .blank to Image", convert_blank_to_image, "Opening image...")

    

    else:

        print("Unsupported file type. Please provide an image file or a .blank file.")



if __name__ == "__main__":

    main()
