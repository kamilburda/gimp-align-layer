#! /usr/bin/env python

import gi

gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import GLib
from gi.repository import GObject

import procedure


def python_fu_align_layers(
      _procedure,
      _run_mode,
      image,
      drawables_to_align,
      config,
      _data,
):
  image_or_reference_layer = config.get_property('image-or-reference-layer')
  reference_layer = config.get_property('reference-layer')
  horizontal_align = config.get_property('horizontal-align')
  vertical_align = config.get_property('vertical-align')
  x_offset = config.get_property('x-offset')
  x_offset_unit = config.get_property('x-offset-unit')
  y_offset = config.get_property('y-offset')
  y_offset_unit = config.get_property('y-offset-unit')

  if reference_layer is None and image_or_reference_layer == 'reference_layer':
    return (
      Gimp.PDBStatusType.EXECUTION_ERROR,
      'You must specify a reference layer if image-or-reference-layer is set to "reference_layer"')

  image_width = image.get_width()
  image_height = image.get_height()

  if reference_layer is not None:
    ref_layer_x, ref_layer_y = reference_layer.get_offsets()[1:]
    ref_layer_width = reference_layer.get_width()
    ref_layer_height = reference_layer.get_height()
  else:
    ref_layer_x = 0
    ref_layer_y = 0
    ref_layer_width = 1
    ref_layer_height = 1

  for drawable in drawables_to_align:
    new_x, new_y = drawable.get_offsets()[1:]

    if horizontal_align == 'left':
      if image_or_reference_layer == 'image':
        new_x = 0
      elif image_or_reference_layer == 'reference_layer':
        new_x = ref_layer_x
    elif horizontal_align == 'center':
      if image_or_reference_layer == 'image':
        new_x = (image_width - drawable.get_width()) // 2
      elif image_or_reference_layer == 'reference_layer':
        new_x = ref_layer_x + (ref_layer_width - drawable.get_width()) // 2
    elif horizontal_align == 'right':
      if image_or_reference_layer == 'image':
        new_x = image_width - drawable.get_width()
      elif image_or_reference_layer == 'reference_layer':
        new_x = ref_layer_x + ref_layer_width - drawable.get_width()

    if vertical_align == 'top':
      if image_or_reference_layer == 'image':
        new_y = 0
      elif image_or_reference_layer == 'reference_layer':
        new_y = ref_layer_y
    elif vertical_align == 'center':
      if image_or_reference_layer == 'image':
        new_y = (image_height - drawable.get_height()) // 2
      elif image_or_reference_layer == 'reference_layer':
        new_y = ref_layer_y + (ref_layer_height - drawable.get_height()) // 2
    elif vertical_align == 'bottom':
      if image_or_reference_layer == 'image':
        new_y = image_height - drawable.get_height()
      elif image_or_reference_layer == 'reference_layer':
        new_y = ref_layer_y + ref_layer_height - drawable.get_height()

    if x_offset:
      if x_offset_unit == 'pixel':
        new_x += int(x_offset)
      elif x_offset_unit == 'percent_of_image_width':
        new_x += int(round((image_width * x_offset) / 100))
      elif x_offset_unit == 'percent_of_image_height':
        new_x += int(round((image_height * x_offset) / 100))
      elif x_offset_unit == 'percent_of_reference_layer_width':
        new_x += int(round((ref_layer_width * x_offset) / 100))
      elif x_offset_unit == 'percent_of_reference_layer_height':
        new_x += int(round((ref_layer_height * x_offset) / 100))

    if y_offset:
      if y_offset_unit == 'pixel':
        new_y += int(y_offset)
      elif y_offset_unit == 'percent_of_image_width':
        new_y += int(round((image_width * y_offset) / 100))
      elif y_offset_unit == 'percent_of_image_height':
        new_y += int(round((image_height * y_offset) / 100))
      elif y_offset_unit == 'percent_of_reference_layer_width':
        new_y += int(round((ref_layer_width * y_offset) / 100))
      elif y_offset_unit == 'percent_of_reference_layer_height':
        new_y += int(round((ref_layer_height * y_offset) / 100))

    drawable.set_offsets(new_x, new_y)


choice_image_or_reference_layer = Gimp.Choice.new()
choice_image_or_reference_layer.add('image', 0, 'Image', '')
choice_image_or_reference_layer.add('reference_layer', 1, 'Reference layer', '')

choice_horizontal_align = Gimp.Choice.new()
choice_horizontal_align.add('keep', 0, 'Keep', '')
choice_horizontal_align.add('left', 1, 'Left', '')
choice_horizontal_align.add('center', 2, 'Center', '')
choice_horizontal_align.add('right', 3, 'Right', '')

choice_vertical_align = Gimp.Choice.new()
choice_vertical_align.add('keep', 0, 'Keep', '')
choice_vertical_align.add('top', 1, 'Top', '')
choice_vertical_align.add('center', 2, 'Center', '')
choice_vertical_align.add('bottom', 3, 'Bottom', '')

offset_unit_choice_values = [
  ('pixel', 0, 'Pixels', ''),
  ('percent_of_image_width', 1, '% of image width', ''),
  ('percent_of_image_height', 2, '% of image height', ''),
  ('percent_of_reference_layer_width', 3, '% of reference layer width', ''),
  ('percent_of_reference_layer_height', 4, '% of reference layer height', ''),
]

choice_x_offset_unit = Gimp.Choice.new()
for choice_values in offset_unit_choice_values:
  choice_x_offset_unit.add(*choice_values)

choice_y_offset_unit = Gimp.Choice.new()
for choice_values in offset_unit_choice_values:
  choice_y_offset_unit.add(*choice_values)


procedure.register_procedure(
  python_fu_align_layers,
  arguments=[
    [
      'choice',
      'image-or-reference-layer',
      'Object to align the drawables to',
      'Object to align the drawables to',
      choice_image_or_reference_layer,
      'image',
      GObject.ParamFlags.READWRITE,
    ],
    [
      'layer',
      'reference-layer',
      'Reference layer',
      'Another layer to align the drawables to (ignored if aligning to the image)',
      True,
      GObject.ParamFlags.READWRITE,
    ],
    [
      'choice',
      'horizontal-align',
      'Horizontal alignment',
      'Horizontal alignment',
      choice_horizontal_align,
      'keep',
      GObject.ParamFlags.READWRITE,
    ],
    [
      'choice',
      'vertical-align',
      'Vertical alignment',
      'Vertical alignment',
      choice_vertical_align,
      'keep',
      GObject.ParamFlags.READWRITE,
    ],
    [
      'double',
      'x-offset',
      'X-offset',
      'X-offset',
      -GLib.MAXDOUBLE,
      GLib.MAXDOUBLE,
      0.0,
      GObject.ParamFlags.READWRITE,
    ],
    [
      'choice',
      'x-offset-unit',
      'Unit for the X-offset',
      'Unit for the X-offset',
      choice_x_offset_unit,
      'pixel',
      GObject.ParamFlags.READWRITE,
    ],
    [
      'double',
      'y-offset',
      'Y-offset',
      'Y-offset',
      -GLib.MAXDOUBLE,
      GLib.MAXDOUBLE,
      0.0,
      GObject.ParamFlags.READWRITE,
    ],
    [
      'choice',
      'y-offset-unit',
      'Unit for the Y-offset',
      'Unit for the Y-offset',
      choice_y_offset_unit,
      'pixel',
      GObject.ParamFlags.READWRITE,
    ],
  ],
  image_types='*',
  sensitivity_mask=(
    Gimp.ProcedureSensitivityMask.DRAWABLE
    | Gimp.ProcedureSensitivityMask.DRAWABLES),
  documentation=(
    'Aligns the specified layers against the image or another layer.',
    ('While aligning layers is already possible in GIMP,'
     ' this script can be used for automation purposes.'),
  ),
  attribution=(
    'Kamil Burda',
    'Kamil Burda',
    '2023',
  ),
)


procedure.main()
