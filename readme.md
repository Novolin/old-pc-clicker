# Old-school display engine

This engine is designed to create displays similar to those in old DOS programs, while keeping the basic python functionality.

TKinter? QT? I don't know them!!!

This is still very, very early and far from feature complete. I'm aiming for the main controls used in most applications, like text entry, buttons, progress bars, etc.

## Changes:
### V0.2:
* Rework to make parenting more logical
* Support for scrolling, close buttons on windows
* Actually tied to github.
* Added per-frame logic stuff! 
* Designed program state to be more sub-classable!

### V0.1:
* Display prototype: 16 colour support with DOS-style display feel
* Barebones menu system
* 80 x 35 characters of ASCII (unicode, really) goodness
* Number go up!


## Funky Engine Notes:
Objects are 
If our window list contains [a, b, c, d], object d will be rendered on top, and override collision detection for anything below it
    (proper always-on-top support will be coming, but is not implemented)
The title bar and its menus will always render on top of, and have collision priority over, anything else.

The Infobar (bottom text line) will always be rendered on top, and will not allow collision


## Known Issues (as of V0.2):
- Default font only supports " ", "▌", and "█", making progress bars less smooth
    - As a result, if you use the "font_supports_eighths" flag, it just does nothing

- text input does not support selection
- Text input cursor is real fucked up on multi-line options, but I need to rewrite a bunch to make it work.
- dropdown menu options don't highlight on hover
- still figuring out how I want to handle entering/exiting text entry mode, so that's a bit busted.
- no sounds yet.

## Controls To Be Implemented:
- Working multi-line text
- check boxes
- radio buttons
- drop dowm menus
- sliders
- dividers for windows
- menu bar submenus
- window resize
- window movement


## Credits:
* Font by VileR, part of a larger pack that is very, very good: https://int10h.org/oldschool-pc-fonts/fontlist/
