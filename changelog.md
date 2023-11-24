# Changelog
This file is updated nearly every commit and copied to GH release changelog.

# 0.16.0-beta
## Syntax
* Add `var ... ++` and `var ... --`

## Loops
* Loops now append `None` to their result even if the node is `None`, not printable, or if the loop is broke or continued.

## Modules
### Import and export
* Add `import ... as ...`
* You can now import nougaro files from current folder and sub-folders.
* Add `export (node) as ...`
* `export` now returns the value to export
### Builtin libs
* Add `noug_version` lib
* Fixed an old bug in the `debug` lib:
  * When you activate the debug mode from the shell, you no longer need to restart it for errors to print their origin file.

## Builtin functions
* Add `__python__` builtin func
* Update `reverse` builtin function (fix error message + can now take strings as argument)
* Improve `__gpl__` builtin func on BSD:
  * now can take any command as text editor

## Misc
* Better error messages
* Switch to semantic versioning
* Add `__args__` to have access to CLI args (except in Nebraska)
* Better retrocompatibility with python 3.10 in tests
* Add a reference to this changelog file in the intro text
* Add backlines to the intro text to be more pleasant to read
* Add python version to intro text in debug mode