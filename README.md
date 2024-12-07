Align Layers
============

This is a [GIMP](https://www.gimp.org/) script that aligns the specified layer(s) against the specified image or another layer.

Alignment is performed horizontally (none, left, center, right) and/or vertically (none, top, center, bottom).

X- and Y-offsets can be specified as pixels, as percentages of image width/height or as percentages of the second layer width/height.

This script introduces a procedure named `python-fu-align-layers`.
While aligning layers is already possible in GIMP, this script is intended to be used for automation purposes. Hence, there is no GUI associated with this procedure.


Usage
-----

Example of centering the first layer against the image, both horizontally and vertically:

```
image = Gimp.get_images()[0]
layer_to_align = image.get_layers()[0]

procedure = Gimp.get_pdb().lookup_procedure('python-fu-align-layers')
config = procedure.create_config()
config.set_property('image', image)
config.set_core_object_array('drawables', [layer_to_align])
config.set_property('horizontal-align', 'center')
config.set_property('vertical-align', 'center')
procedure.run(config)
```

The parameters are explained in the GIMP procedure browser. The procedure name is `python-fu-align-layers`.


Installation
------------

GIMP 3.0.0-RC1 or later is required.

For Linux, make sure you have at least Python 3.7 installed.

1. In GIMP, locate the folder containing GIMP plug-ins - open GIMP and go to Edit → Preferences → Folders → Plug-Ins.
2. Copy the `align_layers` folder inside one of the folders identified in step 1.
