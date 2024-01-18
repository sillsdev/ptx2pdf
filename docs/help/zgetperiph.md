# zgetperiph
## Summary
Milestone to use a stored periphery
## Examples
```
\zgetperiph|side="L" id="intnt"\*
```
## Description
The USFM line `\periph|id="measurements"` will store what follows (until the next `\periph` or `\zendperiph`) for later usage, witth an id of 'measurements'.
 
`\zgetperiph` puts such stored content at the current point (even if that makes little sense). Used peripheries are normally single-use, i.e. they are discarded to save space. See documentation on KeepPeriph if that's undersired.

## Styling of periphery contents
Periphery-specific styling is possible, e.g. a style entry for `periph:intbible|p` could be used to select a different font for all `p` paragraphs in periphery section `intbible`.

## Attributes
* `id="measurements"` Specify the previously stored periphery section's id.
* `side="L"` In a diglot or polyglot, which side's periph should be loaded? Note that this does *not* perform font, etc. setup. That should be done with `\zglot`.

## See also
* [KeepPeriph](keepperiph.md)
* [zglot](zglot.md)

