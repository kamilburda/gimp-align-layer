Align Layer
===========

This is a simple [GIMP](https://www.gimp.org/) script that aligns a layer against another layer.

Alignment is performed both horizontally (none, left, center, right) and vertically (none, top, center, bottom).

X- and Y-offsets can be specified as pixels, as percentages of image width/height or as percentages of the second layer width/height.

This script introduces a procedure named `python-fu-align-layer`.
While aligning layers is already possible in GIMP, this script is intended to be used for automation purposes. Hence, there is no GUI associated with this procedure.


Usage
-----

Example of centering the first layer against the second layer, both horizontally and vertically:

```
image = gimp.image_list()[0]
layer_to_align = image.layers[0]
reference_layer = image.layers[1]

pdb.python_fu_align_layer(image, layer_to_align, reference_layer, 2, 2, 0, 0, 0, 0)
```

The parameters are explained in the GIMP procedural database browser. The procedure name is `python-fu-align-layer`.


Installation
------------

GIMP 2.10 is required.

1. In GIMP, locate the folder containing GIMP plug-ins - open GIMP and go to Edit → Preferences → Folders → Plug-Ins.
2. Copy the `align_layer` folder inside one of the folders identified in step 1.

For Windows, make sure you have GIMP installed with support for Python scripting.

For Linux, make sure you use a GIMP installation bundled as Flatpak (which can be downloaded from the [official GIMP page](https://www.gimp.org/downloads/)) or AppImage.

For macOS, make sure you have Python 2.7 installed.
