#!/usr/bin/env python 

'''
Print matplotlib colors to standard output.
Some inspiration taken from Matplotlib documentation 
https://matplotlib.org/stable/gallery/color/named_colors.html
for getting color names and values.
'''

import argparse 
from collections import OrderedDict
from os import get_terminal_size
import difflib

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
from matplotlib import cm


def FormatRGB( rgb ):
    """
    Take output of mpl.colors.to_rgb and format for use in print.
    input is (r, g, b) in decimal form (e.g., values range from 0.0 to 1.0)
    Output is a string with ANSI escape sequences.
    """

    rgb = [ round(i*255) for i in rgb  ]

    # ANSI escape sequence mess
    return "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"


def PrintColor( rgb, name, endline ):
    """
    Print output for a single color (rbg, name).
    endline is a control to send a newline character
    """

    # Set the length of an entry as 25 spaces
    num_spaces = 31 - 5 - len(name)
    print( FormatRGB( mcolors.to_rgb(name) ) + "      " 
           + "\x1b[0;0m", name, num_spaces*" ", end=endline )

def getSortedHsvColors( colors ):
    return sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in colors.items())

def PrintColors( colors=mcolors.CSS4_COLORS ):
    """
    Print the standard matplotlib colors to screen.
    """
    
    by_hsv = getSortedHsvColors(colors)
    names = [name for hsv, name in by_hsv]

    n     = len( names  )

    # NOTE: You may edit the number of printed columns here
    ncols = 3
    nrows = n // ncols + int( n % ncols > 0 )

    for i, name in enumerate(names):
        col = i % ncols

        # print color.
        # If we're at the end of a row, send in a newline.
        if ( col == ncols - 1 ):
            PrintColor( mcolors.to_rgb(name), name, "\n"  )
        else:
            PrintColor( mcolors.to_rgb(name), name, " "  )


def getDecoString(s):
    s = " = " + s + " = "
    size = get_terminal_size().columns
    
    line = str((len(s)+1) * "=").center(size)
    
    return line + "\n" + s.center(size) + "\n" + line + "\n"

def getNearNameColors( target, colors, least_score = 0.5 ):
    """get near name colors based on difflib.SequenceMatcher.

    Args:
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

def searchColors( target, colors = mcolors.CSS4_COLORS ):
    match_colors = {
        name: color for name, color in colors.items() if target in name
    }
    
    message = f"RESULT (target = {target})"
    print( getDecoString( message ) )
    
    if not match_colors:
        message = "!! No color name hit. Try another color name. !!"
        print(getDecoString( message ))
        
        suggestions = getNearNameColors(target, colors)
        if suggestions:
            print("Maybe...")
            PrintColors( suggestions )

    else:
        PrintColors( match_colors )

def GetColormap( name ):
    """
    Load a colormap into a useable object.
    Easy to do with e.g., cm.Blues but we only have a string

    Create a scalarMap object that can return rgb values with 
    scalarMap.to_rgba(0...255)
    """

    norm = mpl.colors.Normalize(vmin=0.0, vmax=256)
    scalarMap = cm.ScalarMappable(norm=norm, cmap=name)

    return scalarMap


def GetStep( cols ):
    """
    Given the size of the terminal window, 
    set the striding for printing colors
    """

    step = 5
    if ( cols > 55 ):
        step = 5
    if ( cols > 69 ):
        step = 4
    if ( cols > 91 ):
        step = 3
    if ( cols > 136 ):
        step = 2 

    return step

def PrintColorbar( name ):
    """
    Print a single colorbar
    """

    scalarMap = GetColormap( name )

    n = 17 # length for text
    print( (n-len(name))*" " + name, end = " " )

    # get the length of the terminal window.
    # used for adjusting amount of colors printed
    cols   = get_terminal_size().columns

    step = GetStep( cols )

    # Print every 5th color. The colorbar is massive if we print all 256
    for i in range(0, 256, step):
        print( FormatRGB(scalarMap.to_rgba(i)[:-1]) + " " + "\033[0;0m",end=""  )
    print("\n")

    
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

def main( args ):
    
    if ( args.colorbars == False and args.search ):
        colors = mcolors.CSS4_COLORS
        if args.all:
            colors = mcolors.XKCD_COLORS
            # Remove "xkcd:blue with a hint of purple" because it is (almost) 
            # the same as "xkcd:blurple" and that name is too damn long.
            colors.pop("xkcd:blue with a hint of purple")

        searchColors( args.search, colors=colors)
    
    elif ( args.colorbars == False and args.all == False ):
        PrintColors()
    elif ( args.colorbars == False and args.all == True ):
        color_dict = mcolors.XKCD_COLORS
        # Remove "xkcd:blue with a hint of purple" because it is (almost) 
        # the same as "xkcd:blurple" and that name is too damn long.
        color_dict.pop("xkcd:blue with a hint of purple")
        PrintColors( colors=color_dict )
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
    
    # parse any args
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--colorbars", action="store_true",
                    help="display colorbars")
    parser.add_argument( "-a", "--all", action="store_true", help="Print all xkcd colors" )
    parser.add_argument("-s", "--search", help="The color name you want to look up.", default=None)

    args = parser.parse_args()

    main( args  )
