# Old-school display engine

This engine is designed to create displays similar to those in old DOS programs, while keeping the basic python functionality.

TKinter? QT? I don't know them!!!

This is still very, very early and far from feature complete. I'm aiming for the main controls used in most applications, like text entry, buttons, progress bars, etc.

I've also included a test/experimental application - a basic idle game, partially as an example, but also as a way for me to figure out what needs to be done!!



## Changes:
### V0.3:
* Content objects can now beg for death
* Windows see which children need to die before drawing themselves
* Updated fonts to versions with more characters
* Added second font option, just because
* StateManagers can now update the screen outside of the normal frame cycle
    * Useful if a single function will take more than the normal frame rate, such as a loading screen
* Fixed functions acting weird if something drew on top of them
* Added text prompt window prefab

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
    (proper always-on-top support will be coming, but is not implemented yet)
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
- dividers for windows - also having windows be able to share a border
- menu bar submenus
- window resize
- window movement


## Credits:
* Font by VileR, part of a larger pack that is very, very good: https://int10h.org/oldschool-pc-fonts/fontlist/
