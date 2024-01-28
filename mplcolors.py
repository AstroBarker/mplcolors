#!/usr/bin/env python

'''
             .        .
             |        |
.--.--. .,-. | .-..-. | .-. .--..--.
|  |  | |   )|(  (   )|(   )|   `--.
'  '  `-|`-' `-`-'`-' `-`-' '   `--'
        |
        '
Author: Brandon Barker

Print matplotlib colors to standard output.
Some inspiration taken from Matplotlib documentation
https://matplotlib.org/stable/gallery/color/named_colors.html
for getting color names and values.
'''

import math
import argparse
from collections import OrderedDict
from os import get_terminal_size
import difflib

# import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
from matplotlib import cm

__version__ = "1.0.2"

_COL_LENGTH_ = 31 # max column length for printing colors.

# === Color Print Routines ===

def FormatRGB( rgb ):
  """
  Take output of mpl.colors.to_rgb and format for use in print.
  input is (r, g, b) in decimal form (e.g., values range from 0.0 to 1.0)
  Output is a string with ANSI escape sequences.
  """

  rgb = [ round(i*255) for i in rgb  ]

  # ANSI escape sequence mess
  outstr = "\x1b[48;2;" + str(rgb[0]) + ";" \
                 + str(rgb[1]) + ";" + str(rgb[2]) + "m"
  return outstr

def NameToRGB( name ):
  """
  General purpose conversion to RGB
  Parameters:
    name - string. Either mpl color or hex
  Returns:
    rgb: tuple
  """
  if ( name[0].isnumeric() ): # no # in string
    name = "#" + name
    rgb = HexToRGB( name )
  elif ( name[0] == "#" ):    # yes # in string
    rgb = HexToRGB( name )
  else:                       # input is mpl color name
    rgb   = mcolors.to_rgb(name)
  return rgb

def PrintColor( rgb, name, endline ):
  """
  Print output for a single color (rbg, name).
  endline is a control to send a newline character
  """

  # Set the length of an entry as 25 spaces
  num_spaces = _COL_LENGTH_ - 5 - len(name)
  print( FormatRGB( rgb ) + "      "
    + "\x1b[0;0m", name, num_spaces*" ", end=endline )

def GetComplement( name ):
  """
  Compute color complement to "name"
  Parameters:
    name - string. Either mpl color or hex string
  """
  rgb = NameToRGB( name )
  rgb_c = Complement( *rgb )
  hex_c = RGBToHex(rgb_c)
  return hex_c

def PrintComplement( name ):
  """
  Compute and print complement colors to "name"
  Parameters:
      name - string. Either mpl color or hex string.
  """
  rgb = NameToRGB( name )

  message = "Finding RGB Complement of " + name
  print(GetDecoString( message ))

  hex_c = GetComplement( name )
  rgb_c = HexToRGB( hex_c )

  PrintColor( rgb, name, "\n" )
  name = "Complement: " + str( hex_c ) 
  PrintColor( rgb_c, name, "\n" )


def GetSortedHsvColors( colors ):
  """return sorted colors by hsv. check mpl documentation for more."""
  return sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                name) for name, color in colors.items())


def PrintColors( colors=mcolors.CSS4_COLORS ):
  """
  Print the standard matplotlib colors to screen.
  """

  by_hsv = GetSortedHsvColors(colors)
  names  = [name for hsv, name in by_hsv]

  # NOTE: You may edit the number of printed columns here
  
  # do some "smart" setting of number of printed columns.
  # below _COL_LENGTH_ is a magic number I determined to be the max length of a col
  cols = get_terminal_size().columns
  rows = get_terminal_size().lines
  ncols = math.floor( cols / _COL_LENGTH_ )

  for i, name in enumerate(names):
    col = i % ncols

    # print color.
    # If we're at the end of a row, send in a newline.
    if ( col == ncols - 1 ):
      PrintColor( mcolors.to_rgb(name), name, "\n"  )
    else:
      PrintColor( mcolors.to_rgb(name), name, " "  )

# === Colorbar Routines ===

def GetColormap( name ):
  """
  Load a colormap into a useable object.
  Easy to do with e.g., cm.Blues but we only have a string

  Create a scalar_map object that can return rgb values with
  scalar_map.to_rgba(0...255)
  """

  norm = mpl.colors.Normalize(vmin=0.0, vmax=256)
  scalar_map = cm.ScalarMappable(norm=norm, cmap=name)

  return scalar_map


def GetStep( cols ):
  """
  Given the size of the terminal window,
  set the striding for printing colorbar colors.
  Hacky.
  """

  step = 8
  if ( cols > 55 ): step = 5
  if ( cols > 69 ): step = 4 
  if ( cols > 91 ): step = 3
  if ( cols > 136 ): step = 2

  return step


def PrintColorbar( name ):
  """
  Print a single colorbar
  """

  scalar_map = GetColormap( name )

  n = 17 # length for text
  print( (n-len(name))*" " + name, end = " " )

  # get the length of the terminal window.
  # used for adjusting amount of colors printed
  cols = get_terminal_size().columns

  step = GetStep( cols )

  # Print every nth color. The colorbar is massive if we print all 256
  for i in range(0, 256, step):
    print( FormatRGB(scalar_map.to_rgba(i)[:-1]) + " " + "\033[0;0m",end=""  )
  print( "\n" )


def PrintColorbars( cmaps ):
  """
  Print a set of colorbars from dictionary cmap
  """

  for cmap_category, cmap_list in cmaps.items():

    cols = get_terminal_size().columns
    size = int( (256 + 17) / GetStep( cols ) - 1 )

    title = " = " + cmap_category + " = "
    print( str( (len(title)+1)*"=" ).center(size ) )
    print(title.center(size))
    print( str( (len(title)+1)*"=" ).center(size ) )
    print("\n")
    for cmap in cmap_list:
      PrintColorbar( cmap )

# === Complement Color Functions ===

# Based on stackoverflow.com/
#questions/40233986/python-is-there-a-function-or-formula-to-find-the-complementary-colour-of-a-rgb
def hilo(a, b, c):
  """
  min + max of (a, b, c)
  """

  minval = min( min(a, b), c )
  maxval = max( max(a, b), c )
  return minval + maxval


def Complement(r, g, b):
  """
  Given (r, g, b) compute the complement color.
  Note: this is based on RGB color theory. For example,
  Red and green are not complements in this theory.
  Maybe good, maybe bad, but color theory is hard
  (and having colorblind-unfriendly complements is bad in my opinion).

  returns: tuple(r,g,b)
  """
  k = hilo(r, g, b)
  return tuple(k - u for u in (r, g, b))

# === Search Routines ===

def GetDecoString(message):
  """
  Decorative string, mainly for search functions.
  """
  message = " = " + message + " = "
  size = get_terminal_size().columns

  line = str((len(message)+1) * "=").center(size)

  return line + "\n" + message.center(size) + "\n" + line + "\n"


def GetNearNameColors( target, colors, least_score = 0.5 ):
  """
  Get near name colors based on difflib.SequenceMatcher.

  Parameters:
    target (str): the color name to search
    colors (dict[str, str]): search space to search

  Returns:
    dict[str, str]: the result
  """

  near_name_colors = {}
  for name, color in colors.items():
    diff = difflib.SequenceMatcher(None, target, name).ratio()
    if diff > least_score:
      near_name_colors[name] = color

  return near_name_colors


def SearchColors( target, colors = mcolors.CSS4_COLORS ):
  """
  Search mpl colors for target.
  """
  match_colors = {
    name: color for name, color in colors.items() if target in name
  }

  message = f"RESULT (target = {target})"
  print( GetDecoString( message ) )

  if not match_colors:
    message = "!! No color name hit. Try another color name. !!"
    print(GetDecoString( message ))

    suggestions = GetNearNameColors(target, colors)
    if suggestions:
      print("Maybe...")
      PrintColors( suggestions )

  else:
    PrintColors( match_colors )


# === Conversion Routines ===

def HexToRGB( hexval ): # Unused Currently.
  """
  Convert Hex to RGB.
  Parameters: hexval : string -- includes the #, or not.
  returns: tuple(r,g,b)
  """
  if ( hexval[0] != "#" ):
    hexval = "#" + hexval
  return mpl.colors.to_rgb(hexval)


def RGBToHex(rgb):
  """
  Convert RGB to Hex
  Parameter: rgb : tuple
  returns hex: string, inclding "#"
  """
  return mpl.colors.to_hex(rgb)

def HSVToRGB(hsv):
  """
  Convert HSV to RGB
  Parameter: hsv : tuple
  returns rgb: tuple(r,g,b)
  """
  return mpl.colors.hsv_to_rgb(hsv)

def RGBToHSV(rgb):
  """
  Convert RGB to HSV
  Parameter: rgb : tuple
  returns hsv: tuple(h,s,v)
  """
  return mpl.colors.rgb_to_hsv(rgb)

def HexToHSV(hexval):
  """
  Convert hex to hsv
  Parameter: hex : tuple
  returns hsv: tuple(h,s,v)
  """
  rgb = HexToRGB(hexval)
  return RGBToHSV(rgb)

def HSVToHEX(hsv):
  """
  Convert hsv to hex
  Parameter: hsv : tuple
  returns hex: string
  """
  rgb = HSVToRGB(hsv)
  return RGBToHex(rgb)

def main( args ):
  """main function. parse args and call appropriate functions"""

  if ( args.version ):
    print( f"mplcolors {__version__}\n" )
    return 0

  if ( args.colorbars is False and args.search ):
    colors = mcolors.CSS4_COLORS
    if args.all:
      colors = mcolors.XKCD_COLORS
      # Remove "xkcd:blue with a hint of purple" because it is (almost)
      # the same as "xkcd:blurple" and that name is too damn long.
      colors.pop("xkcd:blue with a hint of purple")

    SearchColors( args.search, colors=colors)

  elif ( args.colorbars is False and args.all is False and args.complement is None ):
    PrintColors()
  elif ( args.colorbars is False and args.all is True ):
    color_dict = mcolors.XKCD_COLORS
    # Remove "xkcd:blue with a hint of purple" because it is (almost)
    # the same as "xkcd:blurple" and that name is too damn long.
    color_dict.pop("xkcd:blue with a hint of purple")
    PrintColors( colors=color_dict )
  elif ( args.complement is not None ):
    name = args.complement
    PrintComplement( name )
  else:
    cmaps = OrderedDict()

    # Help us organize the colormaps

    cmaps['Perceptually Uniform Sequential'] = [
      'viridis', 'plasma', 'inferno', 'magma', 'cividis']

    cmaps['Sequential'] = [
      'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

    cmaps['Sequential2'] = [
      'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
      'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
      'hot', 'afmhot', 'gist_heat', 'copper']

    cmaps['Diverging'] = [
      'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
      'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

    cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

    cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
      'Dark2', 'Set1', 'Set2', 'Set3',
      'tab10', 'tab20', 'tab20b', 'tab20c']

    cmaps['Miscellaneous'] = [
      'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
      'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
      'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
      'gist_ncar']

    PrintColorbars(cmaps)
  return 0


if __name__ == "__main__":

  # parse any arg
  DESC = "mplcolors - CLI tool for displaying matplotlib colors"
  parser = argparse.ArgumentParser( description = DESC )
  parser.add_argument("-b", "--colorbars", action="store_true",
    help="display colorbars")
  parser.add_argument( "-a", "--all", action="store_true",
    help="Print all xkcd colors" )
  parser.add_argument("-s", "--search", help="The color name you want to look up.",
    default=None)
  parser.add_argument( "-c", "--complement",
    help="Return the RGB color complement. \
    Input either matplotlib color name or Hex as string, e.g., violet.",
    default=None)

  parser.add_argument( "-v", "--version", help="Print version number.",
    action="store_true" )

  myargs = parser.parse_args()

  main( myargs  )
