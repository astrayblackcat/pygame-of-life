## PyGame of Life  

## Description
This is a small and simple recreation of John Conway's Game of Life made in Pygame, largely created as a just-for-fun project. Despite how simple it is in concept, I've been pretty fascinated by it for a long time — even before I got into software development myself.

John Conway's passing in 2020 during the COVID-19 pandemic was a tragic loss, and ever since then I'd wanted to make something like what you see before you, as a small tribute.

## Running the game

1. Run `pip install -r requirements.txt` from within the directory.
2. Run `python gameoflife.py`.

## Controls

Left Click + Drag: Camera Movement

Right Click: Add/Remove Cell

Space: Pause/Unpause

For convenience, the controls are additionally displayed at the bottom of the screen within the game itself.

## Implementation details

There are a few limitations of this version, notably the lack of an infinite grid. You can achieve a similar effect (although with a significant performance impact) by increasing the size of `GAME_WIDTH` and `GAME_HEIGHT` respectively. It's recommended that you keep these values as multiples of 20.

By default, the grid should fill the screen of a 1440p display, though the game window is completely resizable and is intended to work on smaller displays than this.


## Credits
Built with [Pygame](www.pygame.org).

Thank you to [Catppuccin](https://github.com/catppuccin/catppuccin) for the lovely color scheme.
