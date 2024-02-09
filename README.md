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

### Installing Pre-Requisites

First make sure you have an updated operating system
by running:

```bash
sudo apt update
sudo apt upgrade
```

Next install the required packages:

```bash
sudo apt install python3-pyqt5
pip install pyqtconfig
```

You should be all set for installations!

### Clone Repository

Next up,
clone the repository from GitHub
or download and
unpack it.
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
python3 controls.py
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

### Resolution and framerate

You can set the resolution as `width x height` in pixels, and the framerate in frames per second. For maximum supported resolutions and framerates, see [Sensor Modes](https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes) in the picamera documentation. The new resolution will be applied as soon as you either start the preview, start a recording or capture an image. The new framerate will be applied as soon as you either start the preview or record a video.

### Recording to files

The recording path can be typed directly under
`File path`, or set by clicking on `Browse`.
This will specify which folder new files get saved to.
Putting something into the `File name` input box
will furthermore choose this filename.
A full timestamp can be attached to the beginning of
each file name by checking `Date prefix`.

By default,
the path that you will record to is your Desktop,
e.g., `/home/pi/Desktop`.

### Preview

The raspberry pi camera preview can be started or stopped
with the `Start Preview` / `Stop Preview` button.
This preview directly streams to the GPU and bypasses your window manager,
meaning that you can't move or resize it with the mouse.
See the [Settings](#settings) sections for preview positioning.

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

### <a name="settings"></a> Settings
The settings allow you to configure your RPyScope app and are saved in `~/.config/rpyscope-config.json`.
`open_preview_startup` lets you choose if the preview should be startet when you open the app.
Checking `open_cmd_startup` opens the command window when you open the app.
`preview_x`, `preview_y` and `preview_h` set the `x` and `y` position of the previews top left corner and its height respectively.
The preview width is chosen to preserve the aspect ratio determined by the resolution.
`image_format` and `video_format` allow you to specify output format for image and video files.
Finally `rotation`, `vflip` and `hflip` can rotate and mirror the image vertically and horizontally.

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

### Shortcuts
Shortcuts for each action are indicated in square brackets in the app(for example `[F]` to set the file name).
Shortcuts are inactivated when you input a text or a number. Press enter to end input and activate shortcuts again.
You can manipulate the sliders for brighness and contrast by pressing their shortcut and then adjusting the position with arrows keys.
Press `Ctrl+W` to exit the command window and `Ctrl+Q` to close the app.

## Simple camera
If you only need to take pictures and don't want to install PyQt, you can just run the script `simple_capture.py` in the folder `simple_capture`. In the dialog window type the file name, press save and a picture gets captured and saved as you specified. If your filename ends with a digit, the next filename is set to be the previeus filename with the digit incremented by one.

## Issues, Problems, Questions...

For issues, problems, questions,
contributions, feature requests,
please raise an Issue on GitHub.


## Development

**This section is work in progress, needs:**

- Code of Conduct
- Some details on dev guidelines
- Test requirements

### pre-commit

We use pre-commit to enfore formatting guidelines automatically.
Make sure you have `pre-commit` installed,
e.g., via `pip install pre-commit`.
From the folder where this repo is,
run `pre-commit install` to create the hook.
Now, automatic formatting changes will be done on code-commits.
