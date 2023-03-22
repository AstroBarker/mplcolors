# mplcolors

<p align="center">A command-line information tool written in Python 3.x</p>

<p align="center">
<a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-GPL-blue.svg"></a>
</p>

Tired of searching "[matplotlib colors](https://duckduckgo.com/?q=matplotlib+colors&atb=v275-4&ia=web)" every week/day/hour?
`mplcolors` is a command-line information tool written in Python 3.x which can display `matplotlib` colors, colorbars, and has a few other useful functions.
This uses [matplotlib.colors](https://matplotlib.org/stable/api/colors_api.html) to get color names and RGB values and prints with [ANSI escape sequences](https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences). 
Finally, given a `matplotlib` color or hex value, `mplcolors` can return the RGB color complement.

It can also print all of the built-in colorbars.

<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmatplotlib.org%2F2.1.1%2F_images%2Fsphx_glr_named_colors_001.png&f=1&nofb=1" alt="matplotlib colors" align="right" height="240px">

# Compatibility
This requires a [terminal with true color support](https://gist.github.com/XVilka/8346728).
Notably, Mac's Terminal.app does not have this and so the colors cannot be properly displayed.
I'm not sure that that is a workaround for this. 
On Mac I suggest switching to a different terminal emulator with more modern support such as [kitty](https://sw.kovidgoyal.net/kitty/), [alacritty](https://alacritty.org/), or [iTerm](https://iterm2.com/).

# Requirements
You just need a Python distribution (3.x) with matplotlib and a true color compatible terminal emulator.

# Installation
## Direct Installation
1. Clone this repository `git clone https://github.com/AstroBarker/mplcolors.git`.
2. Run `make install` inside the script directory.
  * __MacOS__ `make PREFIX=/usr/local install`

## OS Packages
`mplcolors` is hosted on the Arch User Repository.
On an Arch-based system, you can do, e.g., 
```shell
yay -S mplcolors
```

Alternatively, you may create an alias in your shell's rc file (e.g., `~/.bashrc`) such as 
```shell
alias mplcolors='python /path/to/dir/mplcolors.py'
```
although this will not install the `man` file.

# Usage

After installation, you may run
```shell
mplcolors
```

to print the default `matplotlib` colors.

You may display all of the available [xkcd colors](https://xkcd.com/color/rgb/) by passing the option `-a` or flag `--all`.

To search for the RGB complement to a given color, use the `-c` or `--complement` flags followed by either a `matplotlib` color or hex.
If using a hex value, the "#" can be given or withheld.

```shell
mplcolors -c "12ab84"
```

To search for colors containing a given string (e.g., "red"), then you can run: 
```shell
mplcolors -s "red"
```

To display all of the built-in colormaps, use the `-b` flag ("b" for "bars") or the `--colorbars` option

```shell
mplcolors -b
```

# TODO
Some functionality to determine how many columns to print based on temrinal size, namely for the color bars, needs logic updates.
