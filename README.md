# mplcolors
Tired of searching "[matplotlib colors](https://duckduckgo.com/?q=matplotlib+colors&atb=v275-4&ia=web)" every week/day/hour?
This simple script displays them all conveniently right in your terminal emulator!
This uses [matplotlib.colors](https://matplotlib.org/stable/api/colors_api.html) to get color names and RGB values and prints 
with [ANSI escape sequences](https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences).

# Useage
It's probably easiest to create an alias in your shell's rc file (e.g., `~/.bashrc`) such as 
```shell
alias mplcolors='python /path/to/dir/mplcolors.py'
```

![Screenshot showing the script in use](screenshot.png)
