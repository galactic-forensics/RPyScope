# RPyScope

This project is the start for a microscope interface
using a Raspberry Pi Camera.
The software interface is written in Python,
thus the name `RPyScope`.

## Privacy notice

Since this is very much work in progress,
we are currently using [Sentry](https://sentry.io/)
to track the behavior of the software.
This is by default activated in the `__init__.py` file
in `src/rpyconfig` and there is currently no automatic way of changing it.
If you do not want to send crashes to us,
please delete the `import sentry_sdk` line
and delete the statement `sentry_sdk.init(...)`.

In a future, more stable version,
this will be made a user opt-in version,
such that you have to explicitly opt-in to submit data.

Of course, leaving this activated helps us a lot
in finding errors and issues!

## Installation

We assume that you have the following components available:

- A raspberry pi with an HQ camera connected
- A stock installation of Raspberry Pi OS

### Update your Pi

First make sure you have an updated operating system
by running:

```bash
sudo apt update
sudo apt upgrade
```


You should be all set for the next steps!

### Clone Repository

Clone the repository from GitHub.
To do so,
start a terminal and type:

```bash
git clone https://github.com/galactic-forensics/RPyScope.git
```

Now you should have a new folder named `RPyScope`
wherever you cloned the repository into.

### RPyScope installation

Go into the `RPyScope` folder by typing `cd RPyScope`.
Now create a virtual python environment:

```bash
python -m venv --system-site-packages venv
```

This will create a new folder called `venv`
that has the system packages available.

Activate the virtual environment by typing:

```bash
source venv/bin/activate
```

Now you can install the `RPyScope` via:

```bash
pip install -e .
```

This will install the source in editable mode,
which is important for updating!



### Running the RPyScope Software

TBD

### Updates

If there are updates,
go into the `RPyScope` folder on the terminal
and type:

```bash
git pull
```

This will update to the latest commit on git


## Usage

Many tool tips have been implemented.
Hover over something you want to adjust and read the tool tip.
Here, only the functions that are not completely self-explanatory
are discussed.


### Recording to files

The recording path can be typed directly under
`File path`, or set by clicking on `Set Path`.
This will specify which folder new files get saved to.
Putting something into the `File name` input box
will furthermore choose this filename.
A full timestamp can be attached to the beginning of
each file name by checking `Date prefix`.

Filenames are autoincremented with a three-digit number.
The first filename will be `-000`.

You can also set up a timelapse.
Activate the checkbox and select the interval and total duration
of the timelapse recording.

By default,
the path that you will record to is your Desktop,
e.g., `~/Desktop`.


### Recording Video

You can record videos by clicking the `Start Recording` button.
The video recorded will be around as long as you set in the
recording time input field.
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


## Configuration

Program settings are stored in `json` format
in the folder `~/.config/rpyscope.json`.


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
