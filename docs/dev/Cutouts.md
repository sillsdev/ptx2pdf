# Cutouts for chapters and figures

## Algorithm 
![ ](/home/david/src/ptx2pdf/docs/dev/Cutouts.svg  "New algorithm")

## Basic calculations
The TeX macros must run multiple times to figure out where to put a cutout, as paragraph shape (cutouts, etc) 
has to be set before the paragraph is finished, and until the paragraph is finished there's no way to determine 
where any given event (e.g. verse 5) occurs.

The `.parlocs` file is written - *at output* - to record the position of
paragraph starts/ends, and column starts/ends. The positional numbers in the file are in TeX's sp (smallest possible) units.
They are  always {X}{Y} and the last or last-but one item. 
On the vertical acess, they are measured from the bottom edge of the page, with a +72pt offset.
I.e.  Vertical distance  = (Y/2^16) - 72. Possibly this offset is  is 72.27,
but for measuring on a screen this is not significant.

At each paragaph, the `\@parstart` line is written, which now contains the appropriate value of \baselineskip.
Polyglot columns use `\@Poly@colstart`  and `\@Poly@colstop`   both of these
record the polyglot column as the final parameter.

The position of the various elements are measured and converted into line counts as per the algorithm graphic above, 
and a warning message is given if the calculations based on these absolute
positions is not in agreement with the `\@parlines` that occus after a `\@parend` for a paragraph that contains 
a delayed item.

Note that once the `.parlocs` file has been read at the end of the `XeTeX` run,
its job is done. Instructions for the next run are contained in the `.delayed`
file.

## Complexities, Loops and Re-run messages.
The postition of the cutout adjusts the pagination of the text. With balanced columns it can alter the final 
arangement of a whole page. Adjusting the cutout postion thus requires that the process be repeated.
It is quite possible that a loop situation is reached, where moving the cutout down moves the anchor up one line.
Moving the anchor up to follow the anchor point then moves the anchor down again. To avoid this situation,
a certain amount of 'slop' or hysteresis is permitted in cutout positions; if an item is within a certain closeness 
to idea, rather than adjusting the cutout, the chapter number / image  is raised or lowered so that *it* goes to the 
cutout rather than the cutout forming around it.
The `.parlocs` file / `.delayed` file for the job (in this case `examples/testcases/fig/test.tex`) shows this:

```
\DelayedItem{droppic1}{TST1.3-preverse}{0}{(53.677ptx8@0)L}
\RaiseItem{droppic3}{TST1.7-preverse}{2}
\DelayedItem{droppic3}{TST1.7-preverse}{11}{(58.91803ptx8@-4)R}
\RaiseItem{chapter}{TST2.0}{1}
\DelayedItem{chapter}{TST2.0}{42}{(18.96863ptx2@0)L}
\RaiseItem{droppic4}{TST2.1-preverse}{1}
\DelayedItem{droppic4}{TST2.1-preverse}{42}{(62.41293ptx6@0)R}
\RaiseItem{droppic5}{TST2.1-preverse}{1}
\DelayedItem{droppic5}{TST2.1-preverse}{45}{(53.677ptx6@3)L}
```


Item `droppic1` is occurring in it's natural place, but other items have all
been raised by one or 2 lines.  Control over the amount of slop uses the
name/category, or a default value is supplied. Thus all chapters get the same range, and (normally) 
pictures use the default. For `chapter`s in a `\\nb` run-on paragraph,  the
allowable slop is set to permit the chapter number to raise by one line. line
above.  The limits  are controlled by the following commands:

 ```
\setCutoutSlopDefault{RAISE}{LOWER}
\setCutoutSlop{droppic3}{RAISE}{LOWER}
```
Where `RAISE` and `LOWER` are positive integers. At present the values are thus:
```
\setCutoutSlopDefault{2}{1}
\setCutoutSlop{chapter}{1}{0}
```

### Log-file entries.
Each time when the slop is not sufficient, the log file should contain entries
of the following type, near the relevant `Rerun...` line.
```
Current slop: \setCutoutSlop{droppic3}{2}{1}
Would use RaiseItem if: \setCutoutSlop{droppic3}{2}{8}
```
This indicates that (on this run) the picture was set 8 lines below the ideal
target point. This is not a particularly useful message, but if it had been `{2}`,
then it might be appropriate to set such a command.

### Effect of slop settings on job cycles.
A `Raiseitem` entry still requires a re-run, to position the image within the
box, but of course that should be the final run caused by that entry. 
In the test case, using the unmodified defaults, the job must run 7 times
before it settles.
Adding the line below, the run count is reduced to 4:
```
\setCutoutSlop{droppic3}{2}{2}
```

Specifying a more restrictive default `\setCutoutSlopDefault{1}{1}` causes an 
endless loop. If A-F are states, then the runs proceeded in the following manner: 
A-B-C-D-E-F-E-F-E-F....etc.  Thus, while the present defaults are not guaranteed 
to produce no loops, it is known that stricter settings produces them. 

### An idea for loop detection and mitigation
If (excluding other changes) any two runs in a sequence give an identical `\jobname.delayed` file, 
then the system has entered a loop. Loops with 2 steps (E-F-E-F above) are
common, but more complex 3 or 4 step loops have been seen when paragraphing or 
even pagination changes come into effect. (e.g. imagine how big a disturbance
may result if moving an image by a line has knock-on changes that  alter whether 
a long footnote is included or not, or the anchor verse for an image set
top-left). 

A fully automatic loop detection and mitigation strategy might look like this:

1) After each run, a checksum (even a weak sum such as md5 ought to be suficient!) is calculated for the 
`\jobname.delayed` file. This is added to a table of known results. The 
corresponding .delayed file could be remembered.

2) After cycle numbers >= 3, the logfile can be examined for 'Would use
RaiseItem...' lines to determine the most troublesome items and mitigation
strategies. 

3) If a loop is detected (using checksum table in (1)), the least impactful
RAISE or LOWER parameter(s) can be selected for each affected item.
These can then be inserted into the job file.

4) If the least impactful parameter is found *before* the loop is entered (e.g.
in state *D* above), then either the .delayed file  corresponding to the state
*C* could be restored or (at the cost of needlessly repeating runs) the
`.delayed` file could just be deleted.

### What problems would sloppier defaults bring or exacerbate?
If a user specifies that an image should occur 2 lines below the verse or keyword 
that it's illustrating, we must assume that they *wanted* it to be there. With the
present, *fixed* defaults, the image could occur anywhere from 0 to 3 lines
below the anchor point. There is no memory in the code or the state about how
hard it has tried to put it there, so if re-paragraphing from an earlier run
end up with it on the same line as the anchor, or 3 lines below, the code will
say 'OK, that's good enough', even if exact positioning was perfectly possible.
This problem only increases with bigger default sloppiness.

Another problem with this sloppiness is that (as state is preserved between runs)
the final output can end up depending on a historical that, due to subsequent
changes, has been lost, and so the final output will not be reproducible on another
day or another machine. In the context of reproducing output or indeed reproducing 
rare error conditions, this is not a desirable result.

