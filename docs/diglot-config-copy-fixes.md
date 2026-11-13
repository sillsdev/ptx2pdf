# Copying a diglot configuration to another project: what was wrong and what has changed

Branches: `diglot-config-copy-fixes`, and `multiproject-manager` which is built on it (neither is in a release yet)
Written: 13 November 2026
Source of the bug reports: John Nystrom's testing notes, sections "Version 3.1" to "Wrong cover prints" (PTXprint 3.1.4 to 3.1.6)

This document has three parts:

1. For John: what each problem was, what has been fixed, and what you still need to do yourself.
2. Notes and questions for Martin.
3. Notes and questions for David.

---

## Part 1: For John

### Summary

| Your report | Cause | Status |
|---|---|---|
| Diglot config copied to a new project keeps Arop in the T1 slot and won't let me change it | The copy kept the source project's name as the left-hand text | Fixed |
| "Impossible path" `...\cGoi\aArpBT\shared\InsertGLOcounterpart.py` | PTXprint had changed what `${settingsdir}` means, so older configs pointed to the wrong place | Fixed |
| Crash mentioning `${prjdir}\InsertGLOcounterpart.py` when shrinking a paragraph, moving a picture, or turning off thumb tabs | Making an archive left PTXprint holding the wrong name for your script | Fixed |
| Wrong cover: James printed with the Colossians titles and ISBN | An old cover file from an earlier print was being shown | Fixed, and one setting for you to check |
| PTXprint complains about `ob00227.png`, a picture from a different project | The right-hand text was still aArpBT, and aArpBT's glossary has a faulty picture entry | Partly fixed; two things for you to do |
| Printed the Arop BT instead of cOGBT | Same cause: the right-hand text is still the source project's | Now warned about; you set it yourself |
| Arop publications appearing in another project after a copy | Publications were copied even when "keep each project's own variables" was ticked | Fixed |
| `! Missing number ... \tri@lsplitRejR` in bSum | Probably: the R row names a project "bSumBT", which does not exist | PTXprint now says so plainly; you set the R row (see section 10) |
| Cannot print the glossary with a publication in cGoi | Not yet investigated; probably the same wrong right-hand text | Open |
| Cannot print with a publication: "PTXprint doesn't do anything, it doesn't even update the PDF" | PTXprint stopped the typesetting of a publication after one second | Fixed (section 11) |
| Jude fails in aArpAux, aMal and aSno with DiglotA5 (found by test printing, not reported by you) | Not found yet: an error in the diglot typesetting | Open (with David) |
| Picture printing twice at the end of bPou Matthew | Not investigated here | Open (with Martin and David) |
| Archive target folder not opening automatically | Not investigated here | Open |
| PTXprint crashed and reopened in a different language | Not investigated here | Open |

### 1. The copied diglot config kept Arop as the T1 text

**What you saw.** After copying DiglotA5 from aArp to bSum, the Diglot tab showed aArp in the T1 (L) row, and PTXprint would not let you change it.

**What was wrong.** When PTXprint copied a configuration to another project, it copied the settings file exactly as it was. That file records which project is the left-hand text, so the copy still said "aArp". The L row is locked on purpose, because the left-hand text is always the project you have open. So the table showed the wrong name and gave you no way to correct it.

The printing itself was not affected by this: the left-hand column always comes from the open project, which is why your T1 text printed in the right language even though the table said Arop.

**What has changed.**

- When you copy a configuration to another project, the left-hand (L) row is now set to that project.
- Configurations you have already copied repair themselves. The next time you open one, the L row shows the right project. You do not need to edit any file by hand or find a GUID.

### 2. The right-hand (T2) text is not changed by a copy

**What you saw.** A diglot printed the Arop BT (aArpBT) when the team wanted cOGBT.

**What was wrong.** Nothing was wrong in the program here, but it was not obvious. PTXprint cannot know which back translation each target project uses, so the R row stays as it was in the source project.

**What has changed.** After you copy a diglot configuration, a message now appears in the status bar naming the projects you copied to and telling you to set each one's secondary (R) project on the Diglot tab.

**What you need to do.** After copying a diglot configuration, open each target project, go to the Diglot tab, and choose the right project and configuration in the R row.

### 3. The "impossible path" to InsertGLOcounterpart.py

**What you saw.** Errors such as:

`The system cannot find the path specified: 'C:/My Paratext 9 Projects/cGoi/aArpBT/shared/InsertGLOcounterpart.py'`

**What was wrong.** Your older configurations store the script location as `${settingsdir}/aArpBT\shared\InsertGLOcounterpart.py`. `${settingsdir}` used to mean "the folder that holds all the Paratext projects". In August 2025 a change made it mean "this project's own folder" instead. From then on, PTXprint looked for aArpBT inside cGoi, which does not exist.

**What has changed.** `${settingsdir}` means the projects folder again, so those configurations find the script where it really is. You do not need to change anything.

### 4. The crash mentioning `${prjdir}\InsertGLOcounterpart.py`

**What you saw.** After making an archive, asking PTXprint to shrink a paragraph, move a picture, or turn off thumb tabs gave an error that named `${prjdir}\InsertGLOcounterpart.py`.

**What was wrong.** While it builds an archive, PTXprint briefly renames a few file locations (the script, a Bible module, included PDFs) so that they make sense inside the archive. It was supposed to put the real locations back afterwards, but it put back the temporary names. The next print then looked for a script with a name that is not a real path.

**What has changed.** The real locations are now put back after an archive is made. (Version 3.1.6 onwards already avoids the crash itself; this fixes the cause.)

### 5. Files that only the source project has

**What was wrong.** If the source configuration used a file inside its own project, for example a script in `aArp\shared`, the copied configuration looked for a file of the same name inside the target project. If it was not there, the print failed or quietly skipped it.

**What has changed.** When a configuration is copied to another project, PTXprint checks each such file. If the target project does not have it but the source project does, the copy points back to the file in the source project. This covers the script, the Bible module, and included PDFs.

**What to be aware of.** The copy does not duplicate the file. If you want each project to have its own version of a script, copy the script yourself and select it on the Advanced tab.

### 6. Publications and the "keep each project's own variables" option

**What was wrong.** The option "Keep each project's own language-specific variables" is ticked by default. It kept the target project's variables, but it still copied the source project's publications. So Arop publications, with Arop titles, turned up in other languages' projects.

**What has changed.** With that option ticked, the target project now keeps its own publications as well as its own variables.

**What to be aware of.** Because this option is ticked by default, a copy leaves the target project's existing variables alone. If the target project already had a DiglotA5 configuration with titles from an earlier job (for example Colossians), those titles are still there after the copy. Check the variables on the Peripherals tab before printing.

### 7. The wrong cover (James with the Colossians titles)

**What you saw.** James printed correctly, but the cover showed the Colossians T1 title, T2 title and ISBN.

**What was wrong.** Your archive shows that the variables were correct: the configuration and the file PTXprint generated both contain the James titles. The variable names (t1title, t2title) were not the problem.

The cause is that **Make Cover Page was turned off** in that configuration, so no new cover was produced. The preview shows any cover file it finds next to the main PDF, and an old cover file from an earlier print of James was still there, made when the variables still held the Colossians values. Nothing was removing it. (That old file is not in the archive, so this explanation is drawn from the settings and the program code.)

**What has changed.** When a print produces no cover, PTXprint now deletes the old cover file for those books, so the preview cannot show an out-of-date one.

**What you need to do.** If you want a cover, turn Make Cover Page back on (Cover tab) in the copied configuration.

### 8. The picture from a different project (`ob00227.png`)

**What you saw.** Printing James with the glossary in cGoi failed with an error naming `ob00227.png`, which is not in the Goiniri project.

**What was wrong.** Two things together:

1. The right-hand text of the copied configuration was still aArpBT (see section 2), so cGoi's glossary was paired with the Arop BT glossary.
2. One picture entry in the Arop BT glossary is put together wrongly. It is in the paragraph that begins "Dispela em narapela kain rais" and reads:

   `\fig Ol |src="ob00227.png" size="span" loc="paw" ref="1.0"\w Juda\w* i save kisim sids bilong wit na wokim bret\fig*`

   The caption has been split in two: it starts ("Ol"), then come the picture's settings, then the rest of the caption follows them. Everything in the caption should come before the `|`. Because of this, PTXprint does not recognise the entry as a normal picture, leaves it in the text, and the typesetting engine stops when it reaches it. (`loc="paw"` itself is fine: all your pictures have it.)

**What you need to do.**

- Set the R row to the right project in cGoi (section 2). This removes the error for cGoi.
- Correct that entry in the aArpBT glossary in Paratext so that the whole caption comes first: `\fig Ol \w Juda\w* i save kisim sids bilong wit na wokim bret|src="ob00227.png" size="span" loc="paw" ref="1.0"\fig*`. Otherwise it may cause the same error whenever the aArpBT glossary is printed.

### 9. Smaller fix

Pressing Print while on the Publications tab with no publication highlighted could raise an error. It now prints the current settings.

### 10. Two more fixes found while checking all 14 projects (13 November)

**A diglot whose other project cannot be found.** The current bSum DiglotA5 has "bSumBT" in the R row. There is no project of that name (bSum's own project settings say its back translation is cOGBT). PTXprint used to carry on without the second text and without telling you, which ends in a confusing error from the typesetting engine, or a page with only one text. This is the most likely cause of your `\tri@lsplitRejR` error, though we have not been able to reproduce that exact message. PTXprint now stops before typesetting and tells you which row names a project or configuration it cannot find.

*What you need to do:* in bSum, set the R row on the Diglot tab to the right back translation project.

**Script paths that version 3.1 saved wrongly.** While `${settingsdir}` had the wrong meaning (section 3), opening and saving a configuration rewrote the script location as `${prjdir}/aArpBT\shared\InsertGLOcounterpart.py`, that is, a folder called aArpBT *inside* the project. Six of the fourteen DiglotA5 configurations are in this state (aMal, aSno, bBar, bG1BT, cOGBT, cWol). PTXprint now recognises this when it loads a configuration and uses the file in the other project, as was meant. You do not need to change anything.

### 11. Publications that would not print

**What you saw.** Printing with a publication did nothing: no new PDF, or a "Failed to create" message.

**What was wrong.** When PTXprint printed a publication it gave the typesetting a time limit of zero seconds by mistake, and stopped it after the first second. Only a publication small enough to typeset in under a second ever came out. This had nothing to do with your settings or your variables.

**What has changed.** A publication now has no time limit unless one is set. Your "James" publication in cGoi, which failed before, now prints in about 13 seconds.

### 12. A new tool: the PTXprint Multi-Project Manager

This is a separate program for looking after the same configuration in many projects at once. It is still being built and is on its own branch (`multiproject-manager`). What it does so far:

- **Problems:** checks one configuration (for example DiglotA5) in every project that has it, explains what is wrong in plain words, and offers repairs with a tick box each. Nothing is changed until you agree.
- **Diglot texts:** shows which project each diglot has on its other side, and lets you choose a different one.
- **Test print:** prints a book you choose in every project and shows which printed and which failed, and why. A test print does not change any of the project's settings files.
- **Publications:** one table of titles, ISBNs and books for every project, edited in place; a publication can be added to every project at once.
- **Compare settings** and **Compare styles:** show where one project's configuration differs from the others'.

### Still open
- **Cannot print the glossary with a publication (cGoi).** Not yet examined. It may have the same cause as section 8.
- **Picture printing twice at the end of bPou Matthew.** Already raised with Martin.
- **Archive folder not opening automatically**, and **PTXprint reopening in a different language after a crash.** Not yet examined.

### One thing that is intended, not a bug

Printing a publication from the Publications tab now copies that publication's variables and book list into the main settings, and they stay there. This was decided on purpose: the Publications tab is for advanced users (Full view only). It means that after printing a publication, the Peripherals tab holds that publication's titles until you change them or print another publication.

---

## Part 2: Notes and questions for Martin

### What changed in the code

| File | Change |
|---|---|
| `utils.py` | `varpaths`: `settingsdir` is the project's parent folder again |
| `view.py` `readConfig` | `polyglots["L"]` always takes `prj`, `prjguid` and `cfg` from the open project and config |
| `view.py` `applyConfig` | After copying `ptxprint.cfg` to another project, calls new `_adaptCopiedConfig` |
| `view.py` `_adaptCopiedConfig` (new) | Sets `[diglot_L]` projectid, projectguid, config; `[project] id`; `[config] name`. Re-points `${prjdir}/...` and `${workingdir}/...` values to the source project when the file exists only there |
| `view.py` `_readLangVars` / `_writeLangVars` | Also keep `[vars.publishable]` and `[publication.*]` when `skipvars` is set |
| `view.py` `_archiveAdd` | Captures each widget's value before changing it, and restores that value unconverted |
| `runjob.py` `procpdf` | Removes `<name>_cover.pdf` when the run produced no cover |
| `publications.py` `applyToView` | Returns if no publication row is highlighted |
| `gtkview.py` `onChooseTargetProjectsClicked` | Status message after copying a diglot config |
| `test/test_headless.py` | `TestCopyDiglotConfig` (four tests) and `TestCommandLine.test_old_cover_removed` |

### Questions

1. **`${settingsdir}`.** Commit `48aa71efc` (21 Aug 2025, "End of Ayahs have the space before moved after") changed `settingsdir` from `os.path.join(p.path, '..')` to `p.path`. Was that intended? The configs in `test/projects` (WSG Strongs, WSGlatin Cover and CoverJON) and John's older configs all use `${settingsdir}/OtherProject/...`, which only works with the parent-folder meaning. Since that commit `withvars` has never written `${settingsdir}`, because `${prjdir}` is tested first and gives an equally short path, so restoring it should not break anything saved since. Please confirm, or say what the change was for.

2. **Publications overwriting the variables (`4e8e7cbe4`).** Mark confirms this is intended. One consequence to be aware of: `applyToView` also sets `r_book` and `ecb_booklist`, and all of it is saved with the config, so the "master" variables are whatever publication was printed last. Is that also what you want for the book list?

3. **Path values in copied configs.** `_adaptCopiedConfig` re-points a missing file to the source project as `${prjdir}/../aArp/shared/x.py`; on the next save `withvars` turns it into `${settingsdir}/aArp/shared/x.py`. The alternative is to copy the file into the target, as `importConfig` does for scripts. Re-pointing was chosen because John shares one script between projects, but it means a project sent to another machine by send/receive depends on the source project being there too. Do you prefer copying?

4. **`_archiveAdd`.** Besides the restore, the `else` branch did `self.set(k, str(v))` on a tuple such as `(False, None)` (for `c_useCustomFolder`), which set the widget to the string `"(False, None)"`. It now uses `v[0]`. Please check that this is what the archive should contain.

5. **Stale cover.** The stale `_cover.pdf` is removed in `RunJob.procpdf`. `pdf_viewer.loadnshow` still shows any `_cover` or `_diff` file it finds. Is there a similar risk for a stale `_diff.pdf`?

6. **R equal to the target project.** If a diglot config is copied to the project that is its own R side, L and R end up as the same project and config. Nothing handles this yet.

7. **Picture printing twice at the end of bPou Matthew** (Mark's comment to you in John's document, 12 Nov). Not looked at in this branch.

### Added later on 13 November (branch `multiproject-manager`)

8. **The Styles tab and TeX read the style sheets in a different order.** TeX is given them as `usfm_sb.sty`, `ptx2pdf.sty`, `custom.sty`, `ptxprint.sty`, then `ptxprint-mods.sty` (`template.tex` lines 25 to 35), so where both set the same attribute of a style, **mods wins on the page**. `ViewModel.getStyleSheets` returns them as `usfm_sb.sty`, `ptx2pdf.sty`, `custom.sty`, `ptxprint-mods.sty`, then `ptxprint.sty`, and `StyleEditor.load` takes the last as the sheet being edited and the rest as its base. So in the Styles tab **`ptxprint.sty` wins**, and the tab can show a value that is not what prints. It also means `ptxprint.sty` is saved as a difference from a base that includes mods, although TeX applies mods afterwards. Which order is intended? The manager's style comparison follows TeX. (The diglot snippet has the same order as the template: `ptxprint.sty` then `ptxprint-mods.sty`.)

9. **Publications were stopped after one second** (`0bcc0dc09`). `BuildParams.timeout` defaults to `0`, and `WorkerContext.execute_job` started its watchdog for anything but `None`, so `threading.Timer(0, ...)` set `printer.timedout` at once and `RunJob._communicate` killed XeTeX at its first one-second check. The publication jobs from `publications.py` and `main.py --pub` don't pass a timeout. The fix is `if job.build_params.timeout:`. The existing test passed because its book typesets in under a second; there is now a test of the watchdog itself. Would you rather `BuildParams.timeout` defaulted to `None`?

10. **`--readonly`** (`ab914a084`). A command line print called `savePics`, `saveStyles` and `saveAdjlists` before printing, and `readConfig` rewrites a config it has brought forward from an older version. The content was equivalent but tidied (`\Occursunder` to `\OccursUnder`, repeated `JUD L 1` lines in adjust lists dropped, adjust lists with only zero entries deleted, `picChecks.txt` rewritten), so every headless print left modified files for Mercurial. With `--readonly`, `ViewModel.readOnly` makes `writeConfig`, `savePics` and `saveStyles` leave the shared files alone, `saveAdjlists` only makes the triggers, and the print gets its own `ptxprint.sty` in the working folder through a new `/styrpath` in the template. Two things to check: is anything else written to `shared/` during a print that I have missed (hyphenation?), and should the normal print be writing these files at all when nothing has changed?

11. **A missing diglot project now stops the print** (`8204612bb`): `RunJob.doit` fails with a message naming the side, project and configuration if a `diglot_X` view can't be made, rather than carrying on without that text.

12. **The manager tool** is in `python/lib/ptxprint/manager/`, with `python/scripts/ptxprint-manager` and an entry point in `pyproject.toml`. It reads and writes `ptxprint.cfg` with `configparser` and does not load a `ViewModel`, except that test prints run `ptxprint` as a subprocess. It is not yet in the PyInstaller spec or the installer.

### Testing

- New tests fail without the fixes and pass with them.
- The full headless suite was run after the first commit: one failure, `TestPolyFill.test_diglot_fill_jas`, which fails the same way on master on Mark's machine because the font "Andika New Basic CompactNonlit" is not installed there. It was not re-run in full after the second commit.
- The status-bar message has not been tested, as it needs the GUI.

---

## Part 3: Notes and questions for David

1. **`\tri@lsplitRejR` undefined (bSum DiglotA5, 3.1.6).** John's error, from several books:

   ```
   ! Missing number, treated as zero.
   <to be read again>
          \tri@lsplitRejR
   \n@xt ...sname tri@lsplitRej\c@rrdstat \endcsname
                     \ifnum \csname saved\c@rrd...
   \after@this ...ount by 1 \relax \check@and@update
   <output> {\diglot@any@trial }
   ...
   l.151 \polyglotendcols
   ```

   `tri@lsplitRej#1` is given a default of `0pt` when a column is declared (`ptx-diglot.tex`, about line 4102), so it looks as though column R was never declared with `\newPolyglotCol` although the merged text uses it. The config had been copied from another project and partly edited by hand, and John reported that it printed once after he changed the T2 width and then failed again. We have no archive for this. What would let R be used without being declared, and what should we ask John to capture?

2. **A malformed `\fig` reaching TeX with `loc="paw"`.** aArpBT's glossary has `\fig Ol |src="ob00227.png" size="span" loc="paw" ref="1.0"\w Juda\w* i save ...\fig*` (attributes in the middle of the caption). The Python side passes it on as `\fig Ol ... bret|size="span" loc="paw" ref="1.0" src="ob00227.png"\fig*`, and TeX stops in `\d@figurePar` with "Missing number" on the `w`: it reads `loc` as a page position. All of John's figures carry `loc="paw"` (the old media field), and normally they never reach TeX because the picture list replaces them. Should TeX ignore a `loc` it can't read as a position, with a warning, rather than stop? The current hint ("Possibly a missing +/- value in the Adjust List") sent John in the wrong direction.

3. **Picture printing twice at the end of bPou Matthew.** A picture set to the bottom of the page, in the last part of the book, appears twice (or once at the end of Matthew and again at the start of the glossary). Setting it to the top of the page avoids it. John says he has seen this in other publications that week. It resembles the duplicate-picture problem fixed for 3.1; is this a remaining case at the end of a book?

4. **Jude fails with DiglotA5 in aArpAux, aMal and aSno** (found on 13 November by test printing every project). XeTeX stops with `! Dimension too large.` at `\polyglotendcols` (l.133 or l.135 of the merged file). All three have aArpBT on the right. aArp itself prints Jude with the same configuration, and all three print 3 John. To reproduce: `ptxprint-manager testprint -c DiglotA5 -b JUD -P aMal`, or print JUD in aMal with DiglotA5. Not investigated further.

5. **Page Fill on diglots (3.1.4).** For reference only: John found the result a net improvement on 2JN and 3JN, with one place in 3JN where a three-line difference between columns became five lines. Martin has already replied in John's document.
