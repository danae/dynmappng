# dynmap-png

**dynmap-png** is a Python script for creating .png exports from Minecraft Dynmap maps. It currently supports creating .png exports from a Dynmap tiles directory, exported per chunk.

## Installation

For the script to work you need a recent version op Python 3 installed on your machine. Afterwards, the script is best installed from the Python Package Index using PIP:

```bash
python3 -m pip install dynmap_png
```

The installation script creates a global executable `dynmap_png` that can be used to generate the images.

## Usage

Use the following command in a terminal to execute the script:

```bash
dynmap_png [-h] [-o OUTPUT] [-z ZOOM] /path/to/tiles
```

Optional arguments:

Name | Description
--- | ---
`-h`, `--help` | Show this help message and exit
`-o OUTPUT`, `--output OUTPUT` | The output directory of the image(s); defaults to the working directory
`-z ZOOM`, `--zoom ZOOM` | The zoom level to use when generating the image; between 0 and 5; defaults to 0
