[+d_setup]::

The first file to be loaded is `paratext2.tex` and it has some initial
definitions and set up that it does. The macros make extensive use of
bidirectional controls and for this we need ETeX and its extensions. This is a
prerequisite and therefore all other ETeX extensions are also available to us.
We also follow the LaTeX convension of using the `@` in internal tokens since
outside of the macros we turn off `@` as a letter, making such tokens
inaccessible. `\expandafter` is a long name for this token and can often occur
very frequently in a short space. It is easier to have a short name for the same
thing. Having a local temporary `if` is useful.

`MSG` is for writing messages to the user. `TRACE` was used in the earliest
debugging, but has been largely replaced by `trace` and `tracing`. But some uses
still persist.

The following two `if`s need to be declared early because they are used during
the declaration of other macros.

[=c_pt_intro]::

Files are timestamped in the cropmarks, if enabled.

The timestamp is not recalculated each call. It is calculated once at the start
of the run.

[=c_timestamp]::

All the other files in the PTX macros system are pulled in early into
`paratext2.tex` before the rest of macros are defined. This allows them to
include their own initialisation early. In some cases, the order in which files
are included is important.

[=c_imports]::

A final setup is to have some fall back fonts defined. It is fully expected that
jobs will override these definitions later:

[=c_fonts-basic]::

### Hooks

The PTX macros have an extensive set of hooks which are token lists that are
executed at appropriate points in the processing.

[=c_define-hooks]::

A CV hook is executed when the verse milestone occurs. The identifier takes the
form of BK1.2 and is based on exactly what the verse milestone value is. The
book is whatever is the book id.

[=csty_define-hooks]::

There are also diglot hooks:

[=cdig_define-hooks]::

Within the style system there a style specific hooks that run at different
points in style processing: before, start, end, after.

[=csty_sethook]::

## Declarations

Various useful declarations. The parargraph types and positions:

[=cpar_strings]::



[-d_setup]::
