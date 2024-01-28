#!/usr/bin/env python

"""
             .        .
             |        |
.--.--. .,-. | .-..-. | .-. .--..--.
|  |  | |   )|(  (   )|(   )|   `--.
'  '  `-|`-' `-`-'`-' `-`-' '   `--'
        |
        '
Author: Brandon L. Barker
https://astrobarker.github.io
https://github.com/AstroBarker

Print matplotlib colors to standard output.
Some inspiration taken from Matplotlib documentation
https://matplotlib.org/stable/gallery/color/named_colors.html
for getting color names and values.

Also usable as a package.
"""

import math
import argparse
from collections import OrderedDict
from os import get_terminal_size
import difflib

# import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
from matplotlib import cm

__version__ = "1.1.0"

_COL_LENGTH_ = 31  # max column length for printing colors.

# === Helper Functions ===


def ColorAbs(val):
  """
  an "absolute value" on the color wheel for H values.
  e.g., for negative numbers, return 360 - H
  """

  return val if (val >= 0.0) else 1.0 + val


# End ColorAbs


def NameToRGB(name):
  """
  General purpose conversion to RGB
  Parameters:
    name - string. Either mpl color or hex
  Returns:
    rgb: tuple
  """
  if name[0].isnumeric():  # no # in string
    name = "#" + name
    rgb = HexToRGB(name)
  elif name[0] == "#":  # yes # in string
    rgb = HexToRGB(name)
  else:  # input is mpl color name
    rgb = mcolors.to_rgb(name)
  return rgb


# End NameToRGB

# === Calcuation Functions ===


def GetComplement(name):
  """
  Compute color complement to "name"
  Parameters:
    name - string. Either mpl color or hex string
  """
  rgb = NameToRGB(name)
  rgb_c = Complement(*rgb)
  hex_c = RGBToHex(rgb_c)
  return hex_c


# End GetComplement


# Based on stackoverflow.com/
# questions/40233986/python-is-there-a-function-or-formula-to-find-the-complementary-colour-of-a-rgb
def hilo(a, b, c):
  """
  min + max of (a, b, c). used for complement.
  """

  minval = min(min(a, b), c)
  maxval = max(max(a, b), c)
  return minval + maxval


# End hili


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


# End Complement


def GetTriad(name):
  """
  Compute color triad. Convert to HSV and manipulate "H" (the zero component)
  Parameters:
    name - string. Either mpl color or hex.
  Returns:
    triad: list(tuples(hexvalues))
  """
  rgb_in = NameToRGB(name)

  out = []

  # convert to hsv
  hsv_in = RGBToHSV(rgb_in)
  hsv_2 = hsv_in.copy()  # will modify later
  hsv_3 = hsv_in.copy()

  # manipulate to get triad
  h_2 = ColorAbs(hsv_in[0] + (120.0 / 360.0) - 1.0)
  h_3 = ColorAbs(hsv_in[0] + (240.0 / 360.0) - 1.0)

  hsv_2[0] = h_2
  hsv_3[0] = h_3

  # convert all to hex
  out.append(RGBToHex(rgb_in))
  out.append(HSVToHex(hsv_2))
  out.append(HSVToHex(hsv_3))

  return out


# End GetTriad


def GetSplitComplement(name):
  """
  Compute color split complements. Convert to HSV and manipulate "H" (the zero component)
  Parameters:
    name - string. Either mpl color or hex.
  Returns:
    triad: list(tuples(hexvalues))
  """
  rgb_in = NameToRGB(name)

  out = []

  # convert to hsv
  hsv_in = RGBToHSV(rgb_in)
  hsv_2 = hsv_in.copy()  # will modify later
  hsv_3 = hsv_in.copy()

  # manipulate to get triad
  h_2 = ColorAbs(hsv_in[0] + (150.0 / 360.0) - 1.0)
  h_3 = ColorAbs(hsv_in[0] + (210.0 / 360.0) - 1.0)

  hsv_2[0] = h_2
  hsv_3[0] = h_3

  # convert all to hex
  out.append(RGBToHex(rgb_in))
  out.append(HSVToHex(hsv_2))
  out.append(HSVToHex(hsv_3))

  return out


# End GetSplitComplement


def GetTetrad(name):
  """
  Compute color tetrad. Convert to HSV and manipulate "H" (the zero component)
  Parameters:
    name - string. Either mpl color or hex.
  Returns:
    triad: list(tuples(hexvalues))
  """
  rgb_in = NameToRGB(name)

  out = []

  # convert to hsv
  hsv_in = RGBToHSV(rgb_in)
  hsv_2 = hsv_in.copy()  # will modify later
  hsv_3 = hsv_in.copy()
  hsv_4 = hsv_in.copy()

  # manipulate to get tetrad
  h_2 = ColorAbs(hsv_in[0] + (90.0 / 360) - 1.0)
  h_3 = ColorAbs(hsv_in[0] + (180.0 / 360) - 1.0)
  h_4 = ColorAbs(hsv_in[0] + (270.0 / 360) - 1.0)

  hsv_2[0] = h_2
  hsv_3[0] = h_3
  hsv_4[0] = h_4

  # convert all to hex
  out.append(RGBToHex(rgb_in))
  out.append(HSVToHex(hsv_2))
  out.append(HSVToHex(hsv_3))
  out.append(HSVToHex(hsv_4))

  return out


# End GetTetrad

# === Color Print Routines ===


def FormatRGB(rgb):
  """
  Take output of mpl.colors.to_rgb and format for use in print.
  input is (r, g, b) in decimal form (e.g., values range from 0.0 to 1.0)
  Output is a string with ANSI escape sequences.
  """

  rgb = [round(i * 255) for i in rgb]

  # ANSI escape sequence mess
  outstr = (
    "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
  )
  return outstr


# End FormatRGB


def PrintColor(rgb, name, endline):
  """
  Print output for a single color (rbg, name).
  endline is a control to send a newline character
  """

  # Set the length of an entry as 25 spaces
  num_spaces = _COL_LENGTH_ - 5 - len(name)
  print(
    FormatRGB(rgb) + "      " + "\x1b[0;0m", name, num_spaces * " ", end=endline
  )


# End PrintColor


def PrintComplement(name):
  """
  Compute and print complement colors to "name"
  Parameters:
      name - string. Either mpl color or hex string.
  """
  rgb = NameToRGB(name)

  message = "Finding RGB Complement of " + name
  print(GetDecoString(message))

  hex_c = GetComplement(name)
  rgb_c = HexToRGB(hex_c)

  PrintColor(rgb, name, "\n")
  name = "Complement: " + str(hex_c)
  PrintColor(rgb_c, name, "\n")


# End PrintComplement


def PrintTriad(name):
  """
  Print color triad
  Parameters:
    name - string. Either mpl color or hex.
  """
  message = "Finding RGB Triad of " + name
  print(GetDecoString(message))

  triad = GetTriad(name)
  rgb_triad = []
  for i in range(3):
    rgb_triad.append(HexToRGB(triad[i]))

  PrintColor(rgb_triad[0], name, "\n")
  for i in range(1, 3):
    name = str(triad[i])
    PrintColor(rgb_triad[i], name, "\n")


# End PrintTriad


def PrintSplitComplement(name):
  """
  Print color split complements
  Parameters:
    name - string. Either mpl color or hex.
  """
  message = "Finding RGB Split Complements of " + name
  print(GetDecoString(message))

  split_c = GetSplitComplement(name)
  rgb_sc = []
  for i in range(3):
    rgb_sc.append(HexToRGB(split_c[i]))

  PrintColor(rgb_sc[0], name, "\n")
  for i in range(1, 3):
    name = str(split_c[i])
    PrintColor(rgb_sc[i], name, "\n")


# End PrintSplitComplement


def PrintTetrad(name):
  """
  Print color tetrad
  Parameters:
    name - string. Either mpl color or hex.
  """
  message = "Finding RGB Tetrad of " + name
  print(GetDecoString(message))

  tetrad = GetTetrad(name)
  rgb_tetrad = []
  for i in range(4):
    rgb_tetrad.append(HexToRGB(tetrad[i]))

  PrintColor(rgb_tetrad[0], name, "\n")
  for i in range(1, 4):
    name = str(tetrad[i])
    PrintColor(rgb_tetrad[i], name, "\n")


# End PrintTetrad


def GetSortedHsvColors(colors):
  """return sorted colors by hsv. check mpl documentation for more."""
  return sorted(
    (tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))), name)
    for name, color in colors.items()
  )


# End GetSortedHsvColors


def PrintColors(colors=mcolors.CSS4_COLORS):
  """
  Print the standard matplotlib colors to screen.
  """

  by_hsv = GetSortedHsvColors(colors)
  names = [name for hsv, name in by_hsv]

  # NOTE: You may edit the number of printed columns here

  # do some "smart" setting of number of printed columns.
  # below _COL_LENGTH_ is a magic number I determined to be the max length of a col
  cols = get_terminal_size().columns
  # rows = get_terminal_size().lines
  ncols = math.floor(cols / _COL_LENGTH_)

  for i, name in enumerate(names):
    col = i % ncols

    # print color.
    # If we're at the end of a row, send in a newline.
    if col == ncols - 1:
      PrintColor(mcolors.to_rgb(name), name, "\n")
    else:
      PrintColor(mcolors.to_rgb(name), name, " ")


# End PrintColors

# === Colorbar Routines ===


def GetColormap(name):
  """
  Load a colormap into a useable object.
  Easy to do with e.g., cm.Blues but we only have a string

  Create a scalar_map object that can return rgb values with
  scalar_map.to_rgba(0...255)
  """

  norm = mpl.colors.Normalize(vmin=0.0, vmax=256)
  scalar_map = cm.ScalarMappable(norm=norm, cmap=name)

  return scalar_map


# End GetColormap


def GetStep(cols):
  """
  Given the size of the terminal window,
  set the striding for printing colorbar colors.
  Hacky.
  """

  step = 8
  if cols > 55:
    step = 5
  if cols > 69:
    step = 4
  if cols > 91:
    step = 3
  if cols > 136:
    step = 2

  return step


# End GetStep


def PrintColorbar(name):
  """
  Print a single colorbar
  """

  scalar_map = GetColormap(name)

  n = 17  # length for text
  print((n - len(name)) * " " + name, end=" ")

  # get the length of the terminal window.
  # used for adjusting amount of colors printed
  cols = get_terminal_size().columns

  step = GetStep(cols)

  # Print every nth color. The colorbar is massive if we print all 256
  for i in range(0, 256, step):
    print(FormatRGB(scalar_map.to_rgba(i)[:-1]) + " " + "\033[0;0m", end="")
  print("\n")


# End PrintColorbar


def PrintColorbars(cmaps):
  """
  Print a set of colorbars from dictionary cmap
  """

  for cmap_category, cmap_list in cmaps.items():
    cols = get_terminal_size().columns
    size = int((256 + 17) / GetStep(cols) - 1)

    title = " = " + cmap_category + " = "
    print(str((len(title) + 1) * "=").center(size))
    print(title.center(size))
    print(str((len(title) + 1) * "=").center(size))
    print("\n")
    for cmap in cmap_list:
      PrintColorbar(cmap)


# End PrintColorbars

# === Search Routines ===


def GetDecoString(message):
  """
  Decorative string, mainly for search functions.
  """
  message = " = " + message + " = "
  size = get_terminal_size().columns

  line = str((len(message) + 1) * "=").center(size)

  return line + "\n" + message.center(size) + "\n" + line + "\n"


# End GetDecoString


def GetNearNameColors(target, colors, least_score=0.5):
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


# End GetNearNameColors


def SearchColors(target, colors=mcolors.CSS4_COLORS):
  """
  Search mpl colors for target.
  """
  match_colors = {
    name: color for name, color in colors.items() if target in name
  }

  message = f"RESULT (target = {target})"
  print(GetDecoString(message))

  if not match_colors:
    message = "!! No color name hit. Try another color name. !!"
    print(GetDecoString(message))

    suggestions = GetNearNameColors(target, colors)
    if suggestions:
      print("Maybe...")
      PrintColors(suggestions)

  else:
    PrintColors(match_colors)


# End SearchColors

# === Conversion Routines ===


def HexToRGB(hexval):  # Unused Currently.
  """
  Convert Hex to RGB.
  Parameters: hexval : string -- includes the #, or not.
  returns: tuple(r,g,b)
  """
  if hexval[0] != "#":
    hexval = "#" + hexval
  return mpl.colors.to_rgb(hexval)


# End HexToRGB


def RGBToHex(rgb):
  """
  Convert RGB to Hex
  Parameter: rgb : tuple
  returns hex: string, inclding "#"
  """
  return mpl.colors.to_hex(rgb)


# End RGBToHex


def HSVToRGB(hsv):
  """
  Convert HSV to RGB
  Parameter: hsv : tuple
  returns rgb: tuple(r,g,b)
  """
  return mpl.colors.hsv_to_rgb(hsv)


# End HSVToRGB


def RGBToHSV(rgb):
  """
  Convert RGB to HSV
  Parameter: rgb : tuple
  returns hsv: tuple(h,s,v)
  """
  return mpl.colors.rgb_to_hsv(rgb)


# End TGBToHSV


def HexToHSV(hexval):
  """
  Convert hex to hsv
  Parameter: hex : tuple
  returns hsv: tuple(h,s,v)
  """
  rgb = HexToRGB(hexval)
  return RGBToHSV(rgb)


# End HexToHSV


def HSVToHex(hsv):
  """
  Convert hsv to hex
  Parameter: hsv : tuple
  returns hex: string
  """
  rgb = HSVToRGB(hsv)
  return RGBToHex(rgb)


# End HSVToHex


def main(args):
  """main function. parse args and call appropriate functions"""

  if args.version:
    print(f"mplcolors {__version__}\n")
    return 0

  if args.colorbars is False and args.search:
    colors = mcolors.CSS4_COLORS
    if args.all:
      colors = mcolors.XKCD_COLORS
      # Remove "xkcd:blue with a hint of purple" because it is (almost)
      # the same as "xkcd:blurple" and that name is too damn long.
      colors.pop("xkcd:blue with a hint of purple")

    SearchColors(args.search, colors=colors)

  elif (
    args.colorbars is False
    and args.all is False
    and args.complement is None
    and args.triad is None
    and args.tetrad is None
    and args.split is None
  ):
    PrintColors()
  elif args.colorbars is False and args.all is True:
    color_dict = mcolors.XKCD_COLORS
    # Remove "xkcd:blue with a hint of purple" because it is (almost)
    # the same as "xkcd:blurple" and that name is too damn long.
    color_dict.pop("xkcd:blue with a hint of purple")
    PrintColors(colors=color_dict)
  elif args.complement is not None:
    name = args.complement
    PrintComplement(name)
  elif args.triad is not None:
    name = args.triad
    PrintTriad(name)
  elif args.tetrad is not None:
    name = args.tetrad
    PrintTetrad(name)
  elif args.split is not None:
    name = args.split
    PrintSplitComplement(name)
  else:
    cmaps = OrderedDict()

    # Help us organize the colormaps

    cmaps["Perceptually Uniform Sequential"] = [
      "viridis",
      "plasma",
      "inferno",
      "magma",
      "cividis",
    ]

    cmaps["Sequential"] = [
      "Greys",
      "Purples",
      "Blues",
      "Greens",
      "Oranges",
      "Reds",
      "YlOrBr",
      "YlOrRd",
      "OrRd",
      "PuRd",
      "RdPu",
      "BuPu",
      "GnBu",
      "PuBu",
      "YlGnBu",
      "PuBuGn",
      "BuGn",
      "YlGn",
    ]

    cmaps["Sequential2"] = [
      "binary",
      "gist_yarg",
      "gist_gray",
      "gray",
      "bone",
      "pink",
      "spring",
      "summer",
      "autumn",
      "winter",
      "cool",
      "Wistia",
      "hot",
      "afmhot",
      "gist_heat",
      "copper",
    ]

    cmaps["Diverging"] = [
      "PiYG",
      "PRGn",
      "BrBG",
      "PuOr",
      "RdGy",
      "RdBu",
      "RdYlBu",
      "RdYlGn",
      "Spectral",
      "coolwarm",
      "bwr",
      "seismic",
    ]

    cmaps["Cyclic"] = ["twilight", "twilight_shifted", "hsv"]

    cmaps["Qualitative"] = [
      "Pastel1",
      "Pastel2",
      "Paired",
      "Accent",
      "Dark2",
      "Set1",
      "Set2",
      "Set3",
      "tab10",
      "tab20",
      "tab20b",
      "tab20c",
    ]

    cmaps["Miscellaneous"] = [
      "flag",
      "prism",
      "ocean",
      "gist_earth",
      "terrain",
      "gist_stern",
      "gnuplot",
      "gnuplot2",
      "CMRmap",
      "cubehelix",
      "brg",
      "gist_rainbow",
      "rainbow",
      "jet",
      "turbo",
      "nipy_spectral",
      "gist_ncar",
    ]

    PrintColorbars(cmaps)
  return 0


# End main

if __name__ == "__main__":
  # parse any arg
  DESC = "mplcolors - CLI tool for displaying matplotlib colors"
  parser = argparse.ArgumentParser(description=DESC)
  parser.add_argument(
    "-b", "--colorbars", action="store_true", help="display colorbars"
  )
  parser.add_argument(
    "-a", "--all", action="store_true", help="Print all xkcd colors"
  )
  parser.add_argument(
    "-s", "--search", help="The color name you want to look up.", default=None
  )
  parser.add_argument(
    "-c",
    "--complement",
    help="Return the RGB color complement. \
    Input either matplotlib color name or Hex as string, e.g., violet.",
    default=None,
  )
  parser.add_argument(
    "-t",
    "--triad",
    help="Return the RGB color triad. \
    Input either matplotlib color name or Hex as string, e.g., violet.",
    default=None,
  )
  parser.add_argument(
    "-r",
    "--tetrad",
    help="Return the RGB color tetrad. \
    Input either matplotlib color name or Hex as string, e.g., violet.",
    default=None,
  )
  parser.add_argument(
    "-sc",
    "--split",
    help="Return the RGB split color complement. \
    Input either matplotlib color name or Hex as string, e.g., violet.",
    default=None,
  )

  parser.add_argument(
    "-v", "--version", help="Print version number.", action="store_true"
  )

  myargs = parser.parse_args()

  main(myargs)
