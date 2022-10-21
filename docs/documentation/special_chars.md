# Special Characters

This describes any special use of Unicode characters for layout control or other
functions. Unless described here, characters are passed through as text to be
shaped and rendered using the current font.

## Conventional Characters

These are characters that implement their normal meaning.

| Character | Details                           |
|-----------|-----------------------------------|
| U+0020    | Implemented as \\space with \\spacefactor derived glue |

## USFM Special Characters

These characters and character sequences have special meaning in USFM at an
encoding level.

| Character | Details                           |
|-----------|-----------------------------------|
| //        | Skip following space and insert \penalty-100 to encourage a line break |
| \|        | Tested to see if it delimits character style or milestone attributes |
| ~         | replaced by NBSP U+00A0 |
| [         | is output then skips following whitespace |
| (         | is output then skips following whitespace |

## Whitespace Characters

Unicode has a number of whitespace characters. Within TeX these are resolved to
a combination of a penalty (or no penalty) and an hskip of some glue.

| Character | Penalty | Skip                      | Defined             |
|-----------|---------|---------------------------|---------------------|
| U+00A0    | nobreak | \\space                   | NBSP                |
| U+2000    | bad     | \\space                   | NQUAD               |
| U+2001    | bad     | 1em plus .2em minus .2em  | MQUAD               |
| U+2002    |         | \\space                   | NSPACE              |
| U+2003    |         | 1em                       | MSPACE              |
| U+2004    |         | .333em                    | THEREEPEREMSPACE    |
| U+2005    |         | .25em                     | FOURPEREMSPACE      |
| U+2006    |         | .1666em                   | SIXPEREMSPACE       |
| U+2009    |         | .2em plus .1em minus .1em | THINSPACE           |
| U+200A    |         | 0.042em \\intercharspace  | HAIRSPACE           |
| U+200B    |         | \\intercharspace          | ZWSP                |
| U+2028    | break   |                           | LINESEP             |
| U+2060    | nobreak |                           | WJ                  |
| U+2063    | good    |                           | GOODBREAK           |
| U+2064    | bad     |                           | BADBREAK            |
| U+FEFF    | nobreak |                           | ZWNBSP              |

The various penalties are defined as:

| Penalty | Defined                 | Default Value |
|---------|-------------------------|---------------|
| nobreak |                         | 10000         |
| bad     | \\the\\badspacepenalty  | 100           |
| good    | -\\OptionalBreakPenalty | 300           |
| break   |                         | -10000        |

To output a space with a given linebreak penalty, output a penalty character
followed by a spacing character (with no penalty).

## Internal Characters

These characters are only used internally and should not to be used in any hand
written data files. They are included here for documentation purposes only and
may change at any time.

| Character | Description                                |
|-----------|--------------------------------------------|
| U+FDEE    | equivalent to { in TeX when { is redefined |
| U+FDEF    | equivalent to } in TeX when } is redefined |


