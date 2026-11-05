# Unique identification of paragraphs.
Piclist, adjustlist, triggers to expand/contract the font, and paragraph shaping around a drop-cap or cutout figure all need to **uniquely** identify a paragraph. There can be multiple ´third paragraph's after a given reference.

Historic methods of doing this are found in the piclist:
```
<Book> <chapter>.<verse> 
or
<Book> <chapter>.<verse>=<paragraph>
``` 
And the adjust list:
```
<Book> <chapter>.<verse> <adjust>[<paragraph>]
<Book> <chapter>.<verse> <adjust>[<paragraph> <T>.<n>.<p>]
       T is the note type
       N is is the note number within the chapter/verse/paragraph
       P (optional) is the paragraph within the note, defaults to 1
```

The piclist form (excluding the space between book and chapter) is also used in trigger files.

Sidebars and marginal notes, however,  are not included in either of these systems, leading to ambiguity.

## Proposed form:
```
ID     := REFBASE ('-preverse') 
       |   BASE('=' PARNUM)
       |   BASE (SUBID) ('[' N ']')
       |   BASE (SUBID) (PARNUMSEP N)

PARNUMSEP := The paragraph number separator. See below, by default '='. 

BASE      := REFBASE | NREFBASE
REFBASE   := the existing location string, when based on a reference
       <BOOK><glot?><C>.<V> 
NREFBASE  := Other location string: 
    | <BOOK>k.<kw> 
    | milestone ref
N  := paragraph index at body level within BASE (SUBID) (1-based; 0 = before the first \p)

SUBID  := '[' FRAME ']'
     | '[' FRAME '][' N ']' SUBID
FRAME  := TYPE '.' K 
TYPE   := marker of the element that opened the frame: 'f', 'x', 'fe', 'esb', 'fig', 'tc', …
K      := key of this frame within the enclosing paragraph (1-based, see below)
```
- **PARNUMSEP** This is user-settable to account for writing systems that use the character `=`, it can be any fixed string. It is particularly important for `k.<keyterm>` references. 
- **Frames** are listed from outermost to innermost. This is *strictly* the order in which they opened, and does not refer to their eventual position on the page.
- **N** counts paragraphs at the current level. Paragraphs inside a frame never advance the N of the paragraph that contains them.
- **A `\tr` row** is a body paragraph, so it has its own N.
- **K** is the ordinal of TYPE within the enclosing paragraph (1-based, counted in input order, separately for each TYPE), unless the type defines its own key:
  - `tc`: the cell's starting column (`\tablec@l`). A cell that spans columns takes the column it starts in. All cell markers (`tc`, `tcr`, `tcc`) use the type `tc`.
  - `fig` from a piclist: the piclist suffix (`\p@clistsuff`), so BASE + K identifies the piclist entry.
- **No spaces** are ever included in the format

Examples:

| ID | Meaning |
|---|---|
| `MAT1.5=2` | Body paragraph 2 of verse 5  (unchanged)|
| `MAT1.5[2]` | Body paragraph 2 of verse 5 (new format) |
| `MAT1.5[2][f.1][1]` | First paragraph of the first `\f` in that paragraph (similar to historic adjust-list syntax) |
| `MAT1.5[2][esb.2][3]` | Paragraph 3 of the second sidebar opened in paragraph 2 |
| `MAT1.5[2][esb.2]=3` | Paragraph 3 of the second sidebar opened in paragraph 2 (old format still acceptable for final paragraph number) |
| `MAT1.5[2][esb.1][2][f.1][1]` | A footnote in paragraph 2 of the first sidebar |
| `MAT1.5[4][tc.3]` | The cell in column 3 of the row that is paragraph 4. A table cell cannot have multiple paragraphs.
| `MAT1.8[1][fig.2][1]` | First caption paragraph of the 2nd piclist picture at MAT 1:8 |

**Triggers** use the same format after the existing separator: `MAT1.5[2][esb.1][3]`. Paragraphs with no frames keep their current trigger names.

## Inline vs triggered content
Piclist and trigger-file supplied content are processed as soon as `\v` (or other trigger location) is encountered. Therefore, there is no circumstance in which in-line content can be encountered before the triggered content. If a piclist contains 2 figures for `INT0.1`, then an inline image will receive 3 as its ordinal (`K`) .

## Implementation

* `\v` sets `\c@rref` to `<ID><CHAP>.<V>` and `\dc@rref` to `<ID><glot><CHAP>.<V>`
* `\esb`, `\f`, etc. generate `\c@rrefprefix` based on `\dc@rref` and the current paragraph number. They also increment relevant type-dependant counters. 
* `\k` and milestones generate `\c@rref` and `\dc@rref` as normal, but  prefixed with `\c@rrefprefix` if that is non-empty. **TBC**
* Triggers, piclist and adjlist compare with `\c@rref` and `\dc@rref` 

### Potential optimisation?
It would be possible to maintain a cache of `BASE` locations for which triggers/piclists/adjustments exist. If there is nothing for an `BASE`, then there is nothing for `BASE SUBID` either, in which case generating the SUBID could be skipped. Given there is a non-linear relationship between TeX's memory use and lookup-speed once extended storage is in use, this is probably not worth it.

# Unresolved

* Should the proposed change affect only the contents of piclists and trigger files (an extension of capabilities) or also adjust lists, where it would be a conflicting format.
* Should the space currently found in piclists and adjustlists between book and chapter be removed or preserved?
