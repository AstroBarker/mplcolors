# mplcolors
Tired of searching "[matplotlib colors](https://duckduckgo.com/?q=matplotlib+colors&atb=v275-4&ia=web)" every week/day/hour?
This simple script displays them all conveniently right in your terminal emulator!
This uses [matplotlib.colors](https://matplotlib.org/stable/api/colors_api.html) to get color names and RGB values and prints 
with [ANSI escape sequences](https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences).

It can also print all of the built-in colorbars.
**Note**: The printed colors are slightly dimmer/duller than the proper colors due to how they're displayed.
I'll look into how to fix this, but this should only be used as a quick reminder.
# Compatability
This requires a [terminal with true color support](https://gist.github.com/XVilka/8346728).
Notably, Mac's Terminal.app does not have this and so the colors cannot be properly displayed.
I'm not sure that that is a workaround for this. 
On Mac I suggest switching to a different terminal emulator with more modern support such as [kitty](https://sw.kovidgoyal.net/kitty/) or [iTerm](https://iterm2.com/).

# Requirements
You just need a Python distribution with matplotlib.

# Useage
It's probably easiest to create an alias in your shell's rc file (e.g., `~/.bashrc`) such as 
```shell
alias mplcolors='python /path/to/dir/mplcolors.py'
```

then you can just run 
```shell
mplcolors
```

to print the colors.

![Screenshot showing the script in use](screenshot.png)

To display all of the built-in colormaps, use the `-b` flag ("b" for "bars") or the `--colorbars` option

```shell
mplcolors -b
```

![Screenshot showing colorbars.](screenshot_colorbars.png)

# To Do
Color lookup, color grouping.
Print subset of colormaps
