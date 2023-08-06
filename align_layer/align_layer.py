#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from gimp import pdb
import gimpfu


def align_layer(
      image,
      layer_to_align,
      reference_layer,
      horizontal_alignment,
      vertical_alignment,
      x_offset,
      x_offset_unit,
      y_offset,
      y_offset_unit,
):
  new_x, new_y = layer_to_align.offsets
  
  if horizontal_alignment == 1:
    new_x = reference_layer.offsets[0]
  elif horizontal_alignment == 2:
    new_x = reference_layer.offsets[0] + (reference_layer.width - layer_to_align.width) // 2
  elif horizontal_alignment == 3:
    new_x = reference_layer.offsets[0] + reference_layer.width - layer_to_align.width
  
  if vertical_alignment == 1:
    new_y = reference_layer.offsets[1]
  elif vertical_alignment == 2:
    new_y = reference_layer.offsets[1] + (reference_layer.height - layer_to_align.height) // 2
  elif vertical_alignment == 3:
    new_y = reference_layer.offsets[1] + reference_layer.height - layer_to_align.height
  
  if x_offset:
    if x_offset_unit == 0:
      new_x += x_offset
    elif x_offset_unit == 1:
      new_x += (image.width * x_offset) / 100
    elif x_offset_unit == 2:
      new_x += (reference_layer.width * x_offset) / 100
  
  if y_offset:
    if y_offset_unit == 0:
      new_y += y_offset
    elif y_offset_unit == 1:
      new_y += (image.height * y_offset) / 100
    elif y_offset_unit == 2:
      new_y += (reference_layer.height * y_offset) / 100
  
  pdb.gimp_layer_set_offsets(layer_to_align, new_x, new_y)


gimpfu.register(
  proc_name='align_layer',
  blurb='Aligns a layer against another layer.',
  help=(
    'While aligning layers is already possible in GIMP,'
    ' this script can be used for automation purposes.'),
  author='Kamil Burda',
  copyright='Kamil Burda',
  date='2023',
  label='',
  imagetypes='*',
  params=[
    (gimpfu.PF_IMAGE, 'image', 'Image', None),
    (gimpfu.PF_LAYER, 'layer_to_align', 'Layer to align', None),
    (gimpfu.PF_LAYER, 'reference_layer', 'Reference layer', None),
    (gimpfu.PF_SLIDER,
     'horizontal_alignment',
     'Horizontal alignment (0 = none, 1 = left, 2 = center, 3 = right)',
     0,
     (0, 3, 1)),
    (gimpfu.PF_SLIDER,
     'vertical_alignment',
     'vertical_alignment (0 = none, 1 = top, 2 = center, 3 = bottom)',
     0,
     (0, 3, 1)),
    (gimpfu.PF_FLOAT, 'x_offset', 'X-offset', 0.0),
    (gimpfu.PF_SLIDER,
     'x_offset_unit',
     ('Unit of X-offset (0 = pixel, 1 = percentage of image width,'
      ' 2 = percentage of reference layer width)'),
     0,
     (0, 1, 1)),
    (gimpfu.PF_FLOAT, 'y_offset', 'Y-offset', 0.0),
    (gimpfu.PF_SLIDER,
     'y_offset_unit',
     ('Unit of Y-offset (0 = pixel, 1 = percentage of image height,'
      ' 2 = percentage of reference layer height)'),
     0,
     (0, 1, 1)),
  ],
  results=[],
  function=align_layer)


if __name__ == '__main__':
  gimpfu.main()
