#!/usr/bin/env python 

'''
Print matplotlib colors to standard output.
Some inspiration taken from Matplotlib documentation 
https://matplotlib.org/stable/gallery/color/named_colors.html
for getting color names and values.
'''

import matplotlib.colors as mcolors

def FormatRGB( rgb ):
    """
    Take output of mpl.colors.to_rgb and format for use in print.
    input is (r, g, b) in decimal form (e.g., values range from 0.0 to 1.0)
    """

    rgb = [ round(i*100) for i in rgb  ]

    return "\033[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"


def PrintColor( rgb, name, endline ):
    """
    Print output for a single color
    """

    num_spaces = 25 - 5 - len(name)
    print( FormatRGB( mcolors.to_rgb(name) ) + "      " 
           + "\033[0;0m", name, num_spaces*" ", end=endline )



def main():

    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in mcolors.CSS4_COLORS.items())
    names = [name for hsv, name in by_hsv]

    n     = len( names  )

    ncols = 3
    nrows = n // ncols + int( n % ncols > 0 )

    for i, name in enumerate(names):
        row = i % nrows
        col = i % ncols
        if ( col == ncols - 1 ):
            PrintColor( mcolors.to_rgb(name), name, "\n"  )
        else:
            PrintColor( mcolors.to_rgb(name), name, " "  )


if __name__ == "__main__":

    main()
