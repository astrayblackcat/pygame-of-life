## PyGame of Life  
#### Video Demo: https://www.youtube.com/watch?v=CkmMOINZUfE


## Description
This is a small and simple recreation of John Conway's Game of Life made in Pygame, largely created as a just-for-fun project. Despite how simple it is in concept, I've been pretty fascinated by it for a long time — even before I got into software development myself.

John Conway's passing in 2020 during the COVID-19 pandemic was a tragic loss, and ever since then I'd wanted to make something like what you see before you, as a small tribute. Rest in peace, John.

## Running the game

There are only a couple of requirements to run this, listed below as well as within `requirements.txt`.

```
pygame > 2.5.2
numpy > 1.26.4
```

It's recommended but not required that you create virtual environment.

Once the requirements are installed, you may simply run it like any other Python program.

Step by step instructions:

1. (Optional) Create a virtual environment. The simplest way is to run `python -m venv <venv-name>`.  
2. Run `pip install -r requirements.txt` from within the directory.
3. Run `python gameoflife.py`.
4. All done!

## Controls

Left Click + Drag: Camera Movement

Right Click: Add/Remove Cell

Space: Pause/Unpause

For convenience, the controls are additionally displayed at the bottom of the screen within the game itself.

## Implementation details

There are a few limitations of this version, notably the lack of an infinite grid. You can achieve a similar effect (although with a significant performance impact) by increasing the size of `GAME_WIDTH` and `GAME_HEIGHT` respectively. It's recommended that you keep these values as multiples of 20.

By default, the grid should fill the screen of a 1440p display, though the game window is completely resizable and is intended to work on smaller displays than this.

If you're having trouble with performance, try turning down the value passed to CLOCK.tick().

Cells are created as instances of the Cell class within a matrix, which is primarily used for visuals. Logic is handled by another matrix of 0's and 1's, to avoid having to generate many more objects than necessary.

## Possible improvements

As noted above, the grid is not infinite. I had considered creating a wrapping grid at some stage of development, but decided against it for simplicity.
If you wish to more accurately create the game, this would likely be a first step.

Adding speed settings, rebinding controls, and alternate color schemes would also be nice improvements and would be fairly easy to accomplish.

## Credits
Built with [Pygame](www.pygame.org).

Thank you to [Catppuccin](https://github.com/catppuccin/catppuccin) for the lovely color scheme.