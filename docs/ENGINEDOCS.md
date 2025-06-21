# Engine Documentation

(no i dont know what im calling this engine quite yet)
also this documentation is currently for my own reference so i dont have to dig through code about each object lmao

## Basic Flow:

1. Grid Manager: - Graphics stuff
 * Controls font, program window size, other 'global' program settings
 * Handles cursor movement and inputs
 * Talks to pygame's renderer
 * Controls the actual grid of characters which will be drawn to the screen
 * Contents are set via functions, to be called by other objects
 * Individual tiles have their own objects, with character, colour, function, default arguments

2. State Manager: - Logic stuff
 * Handles actual program logic on every frame
 * Contains windows, menus and info bar as children
 * Base class is (going to be) fairly barebones, to be customized/ subclassed by actual program logic

3. Windows:
 * Container for controls
 * Talk to grid manager to place their contents
 * 



# Rendering Objects:

## GridTile
Represents a single tile on the display grid. Contains a character, and colour information, and can optionally contain a function that can be activated.

### change_char(char, fg, bg, hi, hi_bg):
Changes the displayed character and colours. All arguments are optional.
* char: the character to display.
* fg: Foreground colour name (see COLOURS enum)
* bg: Background colour name
* hi: Highlighted foreground colour name
* hi_bg: Highlighted background colour name

### toggle_higlight():
Toggles highlighted status.
Returns new highlight status.

### set_function(new_func = None, new_args = None):
Changes the function and/or default arguments assigned to the tile. All arguments are optional.
* new_func: The new function to assign to the tile
* new_args: The new arguments to assign to the default function
    * if multiple arguments are needed, use a list
    * I'm still learning how to pass multiple arguments properly so forgive me if it's messy or breaks your shit.

### clear_function(just_args = False):
Removes the tile's assigned function and/or arguments. 
* just_args: If True, leaves self.function alone, and only removes the arguments.


### activate(args = None):
Activates the tile's function, replacing default args if desired.
* args: List of arguments to use instead of defaults. 


## GridManager
Object that manages the grid of characters, and outputs display information to the renderer. 
Contains the default font, and a grid of individual grid tiles.
