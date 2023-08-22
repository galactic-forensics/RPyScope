from picamera import PiCamera
import tkinter as tk
from tkinter import filedialog as fd

camera = PiCamera()
camera.resolution = (1280, 720)

camera.start_preview(fullscreen=False, window=(550, 0, 1350, 1100))
initial_directory = "~/Desktop"
initial_file = "A1"

while True:
    root = tk.Tk()
    root.geometry("10x10+300+400")
    root.update()

    fname = tk.filedialog.asksaveasfilename(
        title="Where do you want to save the next Picture?",
        filetypes=[("Portable Network Graphics", "*.png")],
        initialdir=initial_directory,
        initialfile=initial_file,
    )
    root.destroy()

    if len(fname) == 0:
        break
    else:
        camera.capture(fname)
        print("picture taken!")
        initial_directory = fname.rsplit("/", 1)[0]

        # Increase last digit in the filename if it is a number, ie A3.png -> A4.png
        initial_file = fname.rsplit("/", 1)[1].split(".")[0]
        try:
            n = int(initial_file[-1])
            initial_file = initial_file[0:-1] + str(n + 1)
        except:
            pass


camera.stop_preview()
