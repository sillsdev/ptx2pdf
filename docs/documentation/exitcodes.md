# PTXprint exit codes

When PTXprint runs from the command line (with `-P`, or with a command such as
`fill`), it ends with one of these exit codes. Scripts and the regression tests
(`ptxprint-manager`) use them to tell what happened.

| Code | Meaning |
|------|---------|
| 0 | Success. The PDF was made, or the command finished without problems. |
| 1 | Failure. Nothing usable was made: a bad project or configuration, no books to print, a XeTeX error, or PTXprint was stopped or killed. XeTeX's own exit codes, and any other unexpected code, are reported as 1. |
| 3 | The PDF was made, but the processing afterwards failed (for example making the cover or extracting inserts), so the finished PDF may be faulty. |
| 4 | XeTeX finished, but xdvipdfmx could not write the PDF. This is usually a font that can't be embedded, or a picture or font that couldn't be loaded. Details are in the `.xdvi_log` file in the working folder. |
| 5 | The PDF was made, but a comparison was asked for and there was no earlier PDF to compare it with. This is not a failure of the print. |
| 6 | `fill` only: every book was typeset, but at least one could not be filled to the page count asked for. This is a warning. |

Code 2 is not used.

## Notes

- Several publications printed together (`-B`) give 0 only if every one of
  them printed, and 1 otherwise.
- `fill` gives 1 if nothing was filled or any book couldn't be typeset at all.
  Otherwise it gives 6 if any book was typeset but not filled, and 0 if all were
  filled.
- In the GUI these codes aren't shown. The same situations appear as messages
  in the status line or in an error dialog.

The code is set in `python/lib/ptxprint/runjob.py` (`RunJob.res`) and turned into
the process exit code in `python/lib/ptxprint/main.py`.
