# Open Issue Triage — sizing for upcoming work

Snapshot: 2026-10-22. Source: <https://github.com/sillsdev/ptx2pdf/issues>, filter
`is:issue state:open -label:Fixed? -label:Documentation -label:"No action" -label:delayed -label:duplicate -label:enhancement -label:wontfix` (62 issues).

Struck-through rows (~~like this~~) are done; skip them.

Sizes are rough estimates made from each issue's title and text, without reading the code.

- **S**: under half a day, with a clear fix.
- **M**: a day or two, or needs real investigation.
- **L**: multi-day, needs design work, or is open-ended.
- 🔺 **Senior**: a senior developer should definitely be involved (core TeX/algorithm work, design decisions, or cross-cutting changes).

## Quick-win groupings

- [#997](https://github.com/sillsdev/ptx2pdf/issues/997) + [#1049](https://github.com/sillsdev/ptx2pdf/issues/1049): picture settings not persisted across sessions (likely one cause).
- [#1038](https://github.com/sillsdev/ptx2pdf/issues/1038) + [#1246](https://github.com/sillsdev/ptx2pdf/issues/1246): footnote spacing with "Start each footnote on a new line" (likely one cause).
- [#1202](https://github.com/sillsdev/ptx2pdf/issues/1202) and [#1204](https://github.com/sillsdev/ptx2pdf/issues/1204) are duplicates, so close one.
- [#1171](https://github.com/sillsdev/ptx2pdf/issues/1171) (3.0.6 report) and [#1207](https://github.com/sillsdev/ptx2pdf/issues/1207) are marked "info needed". Retest before spending time.

## Small (22)

| Issue | Title | Notes | Senior |
|---|---|---|---|
| [#601](https://github.com/sillsdev/ptx2pdf/issues/601) | Crash if hyphenation patterns include characters from fallback-font | Cause identified: patterns load while chars are still active. Catcode fix in `\liter@lspecials`. | |
| [#785](https://github.com/sillsdev/ptx2pdf/issues/785) | Column cross references affects GLO book layout | Non-scripture books should revert to full width; XXS already does. | |
| ~~[#789](https://github.com/sillsdev/ptx2pdf/issues/789)~~ | ~~Copying setting from an old style (Borders)~~ | ~~Borders not copied when adding a style based on `cat:box\|esb`.~~ **DONE** 2026-10-23: new `copyMarkerValues` copies all keys (base + user sheets); test in `test/test_styleditor.py`. | |
| [#991](https://github.com/sillsdev/ptx2pdf/issues/991) | Problem removing footnote from module | Notes checkbox should also strip the `\f` content. | |
| ~~[#997](https://github.com/sillsdev/ptx2pdf/issues/997)~~ | ~~Picture Details tab doesn't remember Media settings~~ | ~~Persistence bug; see grouping above.~~ **DONE** 2026-10-23: unchecking all of Print/App/Web saved `media="x"`, but reloading filtered the `x` away and fell back to the default (all active). `_loadrow` now keeps `x`. Not yet checked whether this also explains #1049. | |
| ~~[#1049](https://github.com/sillsdev/ptx2pdf/issues/1049)~~ | ~~Disappearing image copyrights~~ | ~~Probably same cause as #997.~~ **DONE Fixed?** 2026-10-23: not the same cause as #997. Mostly already fixed by `ad816fdfb` (17 Oct 2026: `PicChecks.init` read the wrong folder, so credits were never read back and the next save discarded them). Also fixed: the first credit in a project was lost if you exited without clicking another picture (`writeCfg` bailed before `savepic`). Awaiting Alastair's confirmation. | |
| [#1114](https://github.com/sillsdev/ptx2pdf/issues/1114) | diglot: text blocks ending with an end-title should be set as text | Fix described in the issue (vtop vs vbox). | |
| [#1038](https://github.com/sillsdev/ptx2pdf/issues/1038) | Start each Footnote on a new line moves the footnote bottom down | Known workaround (±0.25 space) to bake in. | |
| [#1246](https://github.com/sillsdev/ptx2pdf/issues/1246) | Slight change in footnote spacing – observation | Likely same cause as #1038. | |
| [#1058](https://github.com/sillsdev/ptx2pdf/issues/1058) | Final page footnote misalignment | `\FinalNotesDowntrue` works around it; needs default or auto-detect. | |
| [#1170](https://github.com/sillsdev/ptx2pdf/issues/1170) | Wishlist: automatically check usfmtc version | Small startup check. | |
| ~~[#1180](https://github.com/sillsdev/ptx2pdf/issues/1180)~~ | ~~Save a Named Custom Page Size~~ | **DONE** 2026-10-23: typed sizes are saved (whole string) to `customPageSizes` in the user config and added to the dropdown; right-click the entry to remove one. | |
| ~~[#1193](https://github.com/sillsdev/ptx2pdf/issues/1193)~~ | ~~Push Config — Option to Skip Language-Specific Variables~~ | **DONE** 2026-10-23: new checkbox (on by default) in the copy-to-other-projects dialog keeps each target's `[vars]` and `[strongsvars]`; a new config there starts without them. | |
| ~~[#1207](https://github.com/sillsdev/ptx2pdf/issues/1207)~~ | ~~First _diff is hard to produce~~ | ~~Automatic diff filename.~~ **DONE Fixed?** 2026-10-23: the automatic filename already worked (print, change, print again). Improved: Compare now keeps the previous PDF even if "keep versions" is 0; the first print says "Nothing to compare with yet" instead of "No differences found"; `--diffoutfile` was ignored (wrong keyword) and now works. Awaiting a failing procedure from the reporter. | |
| [#1217](https://github.com/sillsdev/ptx2pdf/issues/1217) | Flaky behaviour on right-click for polyglot style settings | **PARKED 2026-10-23, needs more testing; not fixed.** Not reproduced yet. At the model level the real `switchToDiglot`, project/config reload and "Return to Primary" were repeated on `Triglot2JN` (R = other project, A = same project other config) and always switched correctly, with `diglotViews` rebuilt each time. Not tested: the real GTK window (polyglot tree view, dropdown signals), or leaving the secondary project by another route than "Return to Primary". The one path that gives the reported symptom: `switchToDiglot` returns False when `otherDiglot` is None and `diglotViews` has no entry for the column. | |
| ~~[#1238](https://github.com/sillsdev/ptx2pdf/issues/1238)~~ | ~~Need non-breaking glue between Strong's number and following word~~ | **DONE Fixed?** 2026-10-23: not a bug with the default `\HAIRSPACE` (non-breaking): 0 line-end numbers. It only happened when a config's `ptxprint-mods.tex` replaced it with plain glue (the WSG/Strongs test project has `\def\HAIRSPACE{\hskip 0.1em}`: 33 numbers ended a line, 0 after the fix). `\dostr@ngs` now adds `\nobreak` after the number box, so the join holds whatever `\HAIRSPACE` is. The WSG/Strongs standard PDF will change; refresh it with `-u`. | |
| [#1239](https://github.com/sillsdev/ptx2pdf/issues/1239) | Missing ending verse in a cross-ref range | | |
| [#1271](https://github.com/sillsdev/ptx2pdf/issues/1271) | v3.1.3 Picture captions can't be moved away from the picture | Needs a quick look; may be a missing hook. | |
| [#1119](https://github.com/sillsdev/ptx2pdf/issues/1119) | Table alignment broken in RTL books | | |
| ~~[#1028](https://github.com/sillsdev/ptx2pdf/issues/1028)~~ | ~~Issue Page and Displayed page mismatched if Front Matter included~~ | ~~Previous Issue button is easy; page numbering mismatch is more.~~ **DONE Fixed?** 2026-10-23: could not reproduce with a front PDF (page offset, paragraph lookup and arrows all correct); fixed a related arrow bug when the start page number isn't 1 (`updatePageNavigation` compared a folio with the PDF page count). Awaiting David's confirmation. | |
| [#1137](https://github.com/sillsdev/ptx2pdf/issues/1137) | Foreground/background figures in stylesheet not included in archive | Archive code; use relative paths. | |
| [#1260](https://github.com/sillsdev/ptx2pdf/issues/1260) | Old Coverpage configs break with newer versions of the TeX macros | A `\global` def masks the error; David suspects a deeper definition-order problem. | 🔺 |

## Medium (24)

| Issue | Title | Notes | Senior |
|---|---|---|---|
| [#764](https://github.com/sillsdev/ptx2pdf/issues/764) | Possibly unexpected behaviour from ranged milestones with paragraph styles | May end as a docs fix or a design decision. | 🔺 |
| [#917](https://github.com/sillsdev/ptx2pdf/issues/917) | Import Settings from ZIP archive - with custom .py script | Path remapping and script copy. | |
| [#992](https://github.com/sillsdev/ptx2pdf/issues/992) | Copyright overlay should be recorded per piclist-entry | Data-model change; `picInfo.txt` becomes defaults only. | |
| [#994](https://github.com/sillsdev/ptx2pdf/issues/994) | Make it possible to compare PDFs where some have cropmarks | Also needs a page-offset option. | |
| [#998](https://github.com/sillsdev/ptx2pdf/issues/998) | Covers and diglots (work-around) | Side-less periphs for covers. | |
| [#999](https://github.com/sillsdev/ptx2pdf/issues/999) | Random(?) changes in strongs numbering | Non-deterministic output; hard to find, probably small once found. | 🔺 |
| [#1024](https://github.com/sillsdev/ptx2pdf/issues/1024) | Multiple poetry verse number misalignment | | |
| [#1044](https://github.com/sillsdev/ptx2pdf/issues/1044) | Misalignment of page numbers on introduction pages | Happens when a page ends with the outline summary. | |
| [#1048](https://github.com/sillsdev/ptx2pdf/issues/1048) | Using DoulosSILCipher font for music notation | Font/shaping investigation. | |
| [#1051](https://github.com/sillsdev/ptx2pdf/issues/1051) | `\w` to footnote processing makes illegal nested footnotes | Needs USFM-legal flattening. | |
| [#1108](https://github.com/sillsdev/ptx2pdf/issues/1108) | Line spacing is corrupted on one page only | Archive-driven investigation. | |
| [#1171](https://github.com/sillsdev/ptx2pdf/issues/1171) | Unable to create a pdf file | 3.0.6 report, "info needed". Retest on current first. | |
| [#1183](https://github.com/sillsdev/ptx2pdf/issues/1183) | Add Twistie for Headers/Footers with Override Comment in TeX | UI work. | |
| [#1184](https://github.com/sillsdev/ptx2pdf/issues/1184) | Colour-Code AdjList Rows by Diglot Background Shading | UI work. | |
| [#1192](https://github.com/sillsdev/ptx2pdf/issues/1192) | Diglot: Shared vs Unique Footnote Caller Sequence Per Column | | |
| [#1194](https://github.com/sillsdev/ptx2pdf/issues/1194) | Diglot/Polyglot: Option to Request Only Unmerged L-side Books | | |
| [#1229](https://github.com/sillsdev/ptx2pdf/issues/1229) | Archive woe list | Tracker; bug 1 (pdfassets paths) can be fixed on its own. | |
| [#1232](https://github.com/sillsdev/ptx2pdf/issues/1232) | New and old sidebar configuration options not in the user interface | Many new widgets. | |
| [#1234](https://github.com/sillsdev/ptx2pdf/issues/1234) | Numeric Note Callers | Defined proposal. | |
| [#1235](https://github.com/sillsdev/ptx2pdf/issues/1235) | Psalm Book Section Formatting | `\c` and `\ms` order reversed; TeX or Python? | |
| [#1236](https://github.com/sillsdev/ptx2pdf/issues/1236) | Can we detect clashing headers? | Warning heuristic. | |
| [#1241](https://github.com/sillsdev/ptx2pdf/issues/1241) | Page Full Factor isn't behaving as expected | Needs reproducing. | |
| [#1242](https://github.com/sillsdev/ptx2pdf/issues/1242) | un-styling of nested text | Stylesheet semantics change. | 🔺 |
| [#1248](https://github.com/sillsdev/ptx2pdf/issues/1248) | Figure not printing in module XXA | `\fig` ref/placement in the module path. | |

## Large (16)

| Issue | Title | Notes | Senior |
|---|---|---|---|
| [#854](https://github.com/sillsdev/ptx2pdf/issues/854) | Deficiencies in paragraphed footnotes (collect via a vbox instead?) | Core algorithm rework. | 🔺 |
| [#977](https://github.com/sillsdev/ptx2pdf/issues/977) | Drop Chapters and poetry | Parshape and indent interaction. | 🔺 |
| [#1094](https://github.com/sillsdev/ptx2pdf/issues/1094) | PtxP settings not stable after restart or version upgrade | Vague, intermittent; may be several bugs. | 🔺 |
| [#1101](https://github.com/sillsdev/ptx2pdf/issues/1101) | Page-length estimation and breakable footnotes / page-shrinking | Design problem in the balancer. | 🔺 |
| [#1110](https://github.com/sillsdev/ptx2pdf/issues/1110) | Underlined / background-colour text cannot contain special items | Needs box-unwrapper rewrite. | 🔺 |
| [#1181](https://github.com/sillsdev/ptx2pdf/issues/1181) | Config Diff Viewer — Highlight Widgets and Show Tooltip | | |
| [#1185](https://github.com/sillsdev/ptx2pdf/issues/1185) | Lock/Rename a Known-Good PDF in the Preview Pane | | |
| [#1186](https://github.com/sillsdev/ptx2pdf/issues/1186) | Configurable Lock Granularity for Locked Configs | | |
| [#1202](https://github.com/sillsdev/ptx2pdf/issues/1202) | Polyglot Picture Handling — Merged Captions and Correct Piclists | Duplicate of #1204. | 🔺 |
| [#1204](https://github.com/sillsdev/ptx2pdf/issues/1204) | Handle Diglot/Polyglot PicLists better | Duplicate of #1202. | 🔺 |
| [#1210](https://github.com/sillsdev/ptx2pdf/issues/1210) | Multi-project PUSH needs fine-grained control | `ptxprint_nopush.cfg` design. | 🔺 |
| [#1233](https://github.com/sillsdev/ptx2pdf/issues/1233) | Developing a testing framework | Mostly done; remaining items are packaging and recording. | |
| [#1237](https://github.com/sillsdev/ptx2pdf/issues/1237) | Rare column miscalculation? | None of the usual fixes work; deep balancing investigation. | 🔺 |
| [#1243](https://github.com/sillsdev/ptx2pdf/issues/1243) | `\polyglotpages{RL}` is not the same as `\diglotSwaptrue` | Merge, processing, layout and header orders to untangle. | 🔺 |
| [#1247](https://github.com/sillsdev/ptx2pdf/issues/1247) | Publications Tab | New feature with parallel printing. | 🔺 |
| [#1267](https://github.com/sillsdev/ptx2pdf/issues/1267) | Add font fallback for symbols | XeTeX `\iffontchar` fallback mechanism. | 🔺 |

## Senior-developer list (🔺, 16)

[#764](https://github.com/sillsdev/ptx2pdf/issues/764), [#854](https://github.com/sillsdev/ptx2pdf/issues/854), [#977](https://github.com/sillsdev/ptx2pdf/issues/977), [#999](https://github.com/sillsdev/ptx2pdf/issues/999), [#1094](https://github.com/sillsdev/ptx2pdf/issues/1094), [#1101](https://github.com/sillsdev/ptx2pdf/issues/1101), [#1110](https://github.com/sillsdev/ptx2pdf/issues/1110), [#1202](https://github.com/sillsdev/ptx2pdf/issues/1202), [#1204](https://github.com/sillsdev/ptx2pdf/issues/1204), [#1210](https://github.com/sillsdev/ptx2pdf/issues/1210), [#1237](https://github.com/sillsdev/ptx2pdf/issues/1237), [#1242](https://github.com/sillsdev/ptx2pdf/issues/1242), [#1243](https://github.com/sillsdev/ptx2pdf/issues/1243), [#1247](https://github.com/sillsdev/ptx2pdf/issues/1247), [#1260](https://github.com/sillsdev/ptx2pdf/issues/1260), [#1267](https://github.com/sillsdev/ptx2pdf/issues/1267).

---

# View by implementation layer: TeX vs Python

The same 62 issues, split by where the work is likely to be. The split comes from each issue's text and its `Python`/`XeTeX` labels, not from reading the code.

- **TeX only**: the fix should live entirely in the macros (`ptx2pdf.tex` and friends). No Python or UI change is expected.
- **Python involved**: any change to the Python side (GUI, config, archive, text processing, page filler). `+TeX` means the TeX macros will probably need touching as well.
- ❓ means the layer is uncertain until someone reproduces it. The issue could turn out to be Python-side.
- 🔺 means a senior developer should be involved (same marker as above).

## Pure TeX (21)

| Issue | Title | Size | Senior | Confidence |
|---|---|---|---|---|
| [#601](https://github.com/sillsdev/ptx2pdf/issues/601) | Crash if hyphenation patterns include fallback-font characters | S | | Cause identified in `\liter@lspecials` |
| [#764](https://github.com/sillsdev/ptx2pdf/issues/764) | Ranged milestones with paragraph styles | M | 🔺 | |
| [#854](https://github.com/sillsdev/ptx2pdf/issues/854) | Deficiencies in paragraphed footnotes | L | 🔺 | |
| [#977](https://github.com/sillsdev/ptx2pdf/issues/977) | Drop Chapters and poetry | L | 🔺 | |
| [#1024](https://github.com/sillsdev/ptx2pdf/issues/1024) | Multiple poetry verse number misalignment | M | | |
| [#1038](https://github.com/sillsdev/ptx2pdf/issues/1038) | Start each footnote on a new line moves footnote bottom | S | | Same cause as #1246 |
| [#1044](https://github.com/sillsdev/ptx2pdf/issues/1044) | Page numbers off-centre on introduction pages | M | | |
| [#1048](https://github.com/sillsdev/ptx2pdf/issues/1048) | DoulosSILCipher music notation mangled | M | | ❓ font/shaping |
| [#1058](https://github.com/sillsdev/ptx2pdf/issues/1058) | Final page footnote misalignment | S | | |
| [#1108](https://github.com/sillsdev/ptx2pdf/issues/1108) | Line spacing corrupted on one page | M | | ❓ |
| [#1110](https://github.com/sillsdev/ptx2pdf/issues/1110) | Underlined / background text can't contain special items | L | 🔺 | |
| [#1114](https://github.com/sillsdev/ptx2pdf/issues/1114) | Diglot: block ending in end-title should be a vtop | S | | |
| [#1119](https://github.com/sillsdev/ptx2pdf/issues/1119) | Table alignment broken in RTL books | S | | |
| [#1171](https://github.com/sillsdev/ptx2pdf/issues/1171) | Unable to create a PDF (`\@v@` extra `}`) | M | | ❓ old 3.0.6 report; retest |
| [#1234](https://github.com/sillsdev/ptx2pdf/issues/1234) | Numeric note callers | M | | |
| [#1235](https://github.com/sillsdev/ptx2pdf/issues/1235) | Psalms: `\c` and `\ms` order reversed | M | | ❓ |
| [#1237](https://github.com/sillsdev/ptx2pdf/issues/1237) | Rare column miscalculation | L | 🔺 | ❓ may involve the page filler |
| [#1241](https://github.com/sillsdev/ptx2pdf/issues/1241) | Page Full Factor ignored | M | | ❓ |
| [#1246](https://github.com/sillsdev/ptx2pdf/issues/1246) | Footnote spacing changes with option | S | | Same cause as #1038 |
| [#1260](https://github.com/sillsdev/ptx2pdf/issues/1260) | Old coverpage configs break with newer macros | S | 🔺 | ❓ |
| [#1271](https://github.com/sillsdev/ptx2pdf/issues/1271) | Picture captions can't be moved away from picture | S | | ❓ |

## Python involved (41)

### Python only (33)

| Issue | Title | Size | Senior |
|---|---|---|---|
| ~~[#789](https://github.com/sillsdev/ptx2pdf/issues/789)~~ | ~~Copying setting from an old style (Borders)~~ | ~~S~~ **DONE** | |
| [#917](https://github.com/sillsdev/ptx2pdf/issues/917) | Import settings from ZIP with custom .py script | M | |
| [#991](https://github.com/sillsdev/ptx2pdf/issues/991) | Problem removing footnote from module | S | |
| [#992](https://github.com/sillsdev/ptx2pdf/issues/992) | Copyright overlay per piclist entry | M | |
| [#994](https://github.com/sillsdev/ptx2pdf/issues/994) | Compare PDFs with cropmarks / page offset | M | |
| ~~[#997](https://github.com/sillsdev/ptx2pdf/issues/997)~~ | ~~Picture Media settings not remembered~~ | ~~S~~ **DONE** | |
| [#998](https://github.com/sillsdev/ptx2pdf/issues/998) | Covers and diglots | M | |
| [#999](https://github.com/sillsdev/ptx2pdf/issues/999) | Random changes in Strong's numbering | M | 🔺 |
| ~~[#1028](https://github.com/sillsdev/ptx2pdf/issues/1028)~~ | ~~Issue page vs displayed page mismatch~~ | ~~S~~ **DONE Fixed?** | |
| ~~[#1049](https://github.com/sillsdev/ptx2pdf/issues/1049)~~ | ~~Disappearing image copyrights~~ | ~~S~~ **DONE Fixed?** | |
| [#1051](https://github.com/sillsdev/ptx2pdf/issues/1051) | `\w`→footnote makes nested footnotes | M | |
| [#1094](https://github.com/sillsdev/ptx2pdf/issues/1094) | Settings not stable after restart / upgrade | L | 🔺 |
| [#1137](https://github.com/sillsdev/ptx2pdf/issues/1137) | Stylesheet figures not archived / absolute paths | S | |
| [#1170](https://github.com/sillsdev/ptx2pdf/issues/1170) | Auto-check usfmtc version | S | |
| ~~[#1180](https://github.com/sillsdev/ptx2pdf/issues/1180)~~ | ~~Save a named custom page size~~ | ~~S~~ **DONE** | |
| [#1181](https://github.com/sillsdev/ptx2pdf/issues/1181) | Config diff viewer | L | |
| [#1184](https://github.com/sillsdev/ptx2pdf/issues/1184) | Colour-code AdjList rows by diglot shading | M | |
| [#1185](https://github.com/sillsdev/ptx2pdf/issues/1185) | Lock/rename a known-good PDF | L | |
| [#1186](https://github.com/sillsdev/ptx2pdf/issues/1186) | Configurable lock granularity | L | |
| ~~[#1193](https://github.com/sillsdev/ptx2pdf/issues/1193)~~ | ~~Push config: skip language-specific variables~~ | ~~S~~ **DONE** | |
| [#1194](https://github.com/sillsdev/ptx2pdf/issues/1194) | Request only unmerged L-side books | M | |
| [#1202](https://github.com/sillsdev/ptx2pdf/issues/1202) | Polyglot picture handling | L | 🔺 |
| [#1204](https://github.com/sillsdev/ptx2pdf/issues/1204) | Handle diglot/polyglot piclists (duplicate of #1202) | L | 🔺 |
| ~~[#1207](https://github.com/sillsdev/ptx2pdf/issues/1207)~~ | ~~First `_diff` is hard to produce~~ | ~~S~~ **DONE Fixed?** | |
| [#1210](https://github.com/sillsdev/ptx2pdf/issues/1210) | Multi-project push fine-grained control | L | 🔺 |
| [#1217](https://github.com/sillsdev/ptx2pdf/issues/1217) | Right-click polyglot style settings flaky | S **(PARKED: see above)** | |
| [#1229](https://github.com/sillsdev/ptx2pdf/issues/1229) | Archive woe list | M | |
| [#1232](https://github.com/sillsdev/ptx2pdf/issues/1232) | Sidebar options missing from the UI | M | |
| [#1233](https://github.com/sillsdev/ptx2pdf/issues/1233) | Testing framework | L | |
| ~~[#1238](https://github.com/sillsdev/ptx2pdf/issues/1238)~~ | ~~Non-breaking glue after Strong's number~~ | ~~S~~ **DONE Fixed?** | |
| [#1239](https://github.com/sillsdev/ptx2pdf/issues/1239) | Missing ending verse in cross-ref range | S | |
| [#1247](https://github.com/sillsdev/ptx2pdf/issues/1247) | Publications tab | L | 🔺 |
| [#1248](https://github.com/sillsdev/ptx2pdf/issues/1248) | Figure not printing in module | M | |

### Python + TeX (8)

| Issue | Title | Size | Senior | What touches TeX |
|---|---|---|---|---|
| [#785](https://github.com/sillsdev/ptx2pdf/issues/785) | Column cross-refs affect GLO layout | S | | Column reset for non-scripture books ❓ |
| [#1101](https://github.com/sillsdev/ptx2pdf/issues/1101) | Page-length estimation / breakable footnotes | L | 🔺 | Page filler (Python) and TeX page breaking |
| [#1183](https://github.com/sillsdev/ptx2pdf/issues/1183) | Header/footer twistie and override comment | M | | UI plus the comment written into the `.tex` |
| [#1192](https://github.com/sillsdev/ptx2pdf/issues/1192) | Shared vs per-column footnote callers | M | | Diglot tab option plus caller macros |
| [#1236](https://github.com/sillsdev/ptx2pdf/issues/1236) | Detect clashing headers | M | | Measure in TeX, report in Python |
| [#1242](https://github.com/sillsdev/ptx2pdf/issues/1242) | Un-styling of nested text | M | 🔺 | Stylesheet parsing plus macro style handling |
| [#1243](https://github.com/sillsdev/ptx2pdf/issues/1243) | `\polyglotpages{RL}` vs `\diglotSwaptrue` | L | 🔺 | Merge order (Python) and layout/header order (TeX) |
| [#1267](https://github.com/sillsdev/ptx2pdf/issues/1267) | Font fallback for symbols | L | 🔺 | Python finds the characters, TeX tests with `\iffontchar` |
