# ptx macros notes

## New things here

- \include ptxplus-marginalverses.tex to have marginal verses
- \ifendbooknoeject Ability to start a new book without starting a new page
- \PaperWidth, \PaperHeight
- \ifhangingverse
- \BaseLine in sty
- handling of headings notes correctly wrapping
- Insert strut at the start of each paragraphed note so that the caller doesn't clash with the line above. Previously this was fixed to 1.2 x font size
- allow notes to split to the next page
- \ExtraRMargin set in .tex
- \AboveNoteSpace and \InterNoteSpace set in .tex
- \columnshift (or is this calculated)?
- \internotepenalty (currently -10). \internotespace
- \ColumnGutterRuleSkip gap between header horizontal line and vertical gutter line
- \ifrotate (for things like mongolian) along with \XeTeXupwardsmode
- \CallerRaise in sty to raise the caller in the main text
- \NoteCallerRaise in sty to raise the caller in the note
- \NoteCallerStyle in sty to set style of caller in note
- \Notecallerstyle for a note marker type
- \ifOmitBookRef for headers
- can override \defineheaders to define \oddhead, \evenhead, \titlehead (why?)
- do we need to bring in \calch@ngverseoffset and \HangVerseAlignMarker from PT?
