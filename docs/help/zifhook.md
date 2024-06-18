# zifhook
## Summary
Test if there are any hooks set on a marker and set conditional markers (ztruetext,zfalsetext) appropriately.

## Examples
```
\zifhooks|add\* \zfalsetext [\zfalsetext* Some extra text \zfalsetext ]\zfalsetext*
```

## Description
`\add` (translator's addition) might impose some kind of subtle brackets, via hooks.
Or it might just mark the text in italics, or even not mark the text at all.
The above will put `[` and `]` around `Some extra text`, but only if there are
no hooks normally triggered by that
markup.

## Attributes
* `marker="add"` - the marker to be tested.

## See also
* Documentation on [Contitional text](conditional.md)
* [ztruetext](ztruetext.md)
* [zfalsetext](zfalsetext.md)
