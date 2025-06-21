# Idle Incremental Arcade (title tbd)

## Changes:
### V0.2:
* Rework to make parenting more logical
* Support for scrolling, close buttons on windows
* Better gameplay shit i guess.
* Actually tied to github.

### V0.1:
* Display prototype: 16 colour support with DOS-style display feel
* Barebones menu system
* 80 x 35 characters of ASCII (unicode, really) goodness
* Number go up!


## Funky Engine Notes:
Objects are (or will be lmao) rendered with the highest-indexed child as highest-priority. example:
If our window list contains [a, b, c, d], object d will be rendered on top, and override collision detection for anything below it
The title bar and its menus will always render on top of, and have collision priority over, anything else.

The Infobar (bottom text line) will always be rendered on top, and will not allow collision



## Credits:
* Font by VileR, part of a larger pack that is very, very good: https://int10h.org/oldschool-pc-fonts/fontlist/
