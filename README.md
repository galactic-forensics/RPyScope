# RPyScope

This project is the start for a microscope interface
using a Raspberry Pi Camera.
The software interface is written in Python,
thus the name `RPyScope`.

## Installation

We assume that you have the following components available:
 - A raspberry pi with a camera that is enabled
 - A stock installation of Raspberry Pi OS

If you are not sure if your camera is enabled, 
try and take an image according to the getting started guide
[here](https://static.raspberrypi.org/files/product-guides/Raspberry_Pi_High_Quality_Camera_Getting_Started.pdf).

### Installing Linux Pre-Requisites

First make sure you have an updated operating system
by running:

```bash
sudo apt update
sudo apt upgrade
```

Next install the required packages
to run PyQt5 as following:

```bash
sudo apt install python3-pyqt5
```

You should be all set for installations!

### Clone Repository

Next up,
clone the repository from GitHub
or download an

d unpack it.  
**Note**: The repository is
currently private,
therefore you have to authenticate
when cloning the repository.

Cloning can be done in the folder of your interest
by typing:
```bash
git clone https://github.com/galactic-forensics/RPyScope.git
```
for access via `https`, or 
```bash
git clone git@github.com:galactic-forensics/RPyScope.git
```
for access via `ssh` authentication.

Now you should have a new folder named `RPyScope`
wherever you cloned the repository into.

### Installing the rpyscope python package

Inside the folder `RPyScope`, install the python package by typing
```bash
pip3 install .
```
If you plan on playing with the source code, type
```bash
pip3 install -e .
```
instead.

### Running the RPyScope Software

To run the software,
go into the folder `RPyScope/rpyscope`
and run the command:
```bash
python3 gui_qt.py
```
You should see the software start up. Give it a try!

### Updates

If you cloned the GitHub repository,
you can simply go into the folder and pull from the repo
in order to update your branch to the latest one.


## Usage

Many tool tips have been implemented. 
Hover over something you want to adjust and read the tool tip.
Here, only the functions that are not completely self-explanatory
are discussed.

### Exposure control

Using the sliders,
you can live-adjust brightness and contrast of the camera.
Generally,
the camera is set up such that 
automatic expsosure is turned on (checked).
For details, see
[here](https://picamera.readthedocs.io/en/release-1.13/fov.html)
on what that entails.

When you turn automatic exposure off, 
the camera will not regulate the shutter speed, 
or digital and analog gain anymore.
This is intended for taking images under stable conditions
and follows the description in
[Section 3.5](https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-consistent-images)
in the PiCamera Manual.
You can still adjust brightness and contrast.

### Recording to files

The recording path can be set by 
clicking the button 
`Set Recording Path`.
This will specify which folder new files get saved to.
Putting something into the file name input box
will furthermore choose this filename.
*Note* that currently,
a full timestamp will be attached to the beginning of 
each file name.

By default,
the path that you will record to is the home path,
e.g., `/home/pi`.

### Preview

The raspberry pi camera preview can be started or stopped
with the `Start Preview` / `Stop Preview` button.
This preview directly streams to the GPU,
therefore you are advised to keep the program on the very left
or very right of the screen.
If you don't move your mouse away from the button,
you can always click it in case you cannot see it anymore
after the preview starts.

### Recording Video

You can record videos by clicking the `Start Recording` button.
The video recorded will be around as long as you set in the
recording time input field. 
Increments of 0.1 milliseconds are currently considered.
You can always stop the recording early by pressing
the `Stop Recording` button.

If you leave the recording time at 0,
video will be recorded until 
you press the `Stop Recording` button.

The video format that is outputted is currently fixed
to `.h264`.

**Limitation:** While images can be captured 
during recordings,
this functionality is currently not implemented.


### Capturing Images

If you want to take a photo,
press the `Capture Image` button
and the software will save an image in the 
`.jpeg` format in the location of your choice. 
Other formats are currently not supported,
but will be in the future. 
You can also easily change the default 
by hacking around in the code :)

### Command line interface (CLI)

The second window is the command line interface.
Many features are not currently implemented, 
however, 
if you can work with the `picamera` class,
you can execute commands here directly from the software.
The camera itself is stored into an instance called `cam`.
So if you, e.g.,
want to set the `iso` of the camera to fixed,
you can type:

```python
camera.iso = 100
```

You can also use regular python commands here,
they will all be interpreted.
For example, typing:

```python
print(camera.iso)
```

Should print the current `iso` setting out to the terminal.
If python raises an error,
a messagebox will be displayed.

**Important:**
You can run any python command you want.
However, 
you can also interfere with the software itself.
The idea of the CLI is to give the user an easy way
of modifying stuff with commands and to play / explore the settings.
If you need stuff over and over again, 
it might be easier to implement it into the software.
Also: you might be able to do real damage with the CLI to all your data,
because you have the full power of python at your fingertips.
Enjoy!

## Issues, Problems, Questions...

For issues, problems, questions,
contributions, feature requests,
please raise an Issue on GitHub.
