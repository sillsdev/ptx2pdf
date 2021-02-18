# Diglot debugging

There are a lot of things that can have gone wrong in diglots over the years,
and a lot of tracing elements have been added.  One of the most basic
steps (in David's opinion) is to do the folowing:

```
\VisTracetrue
\tracing{d}
\tracing{D}
```

`VisTrace` adds visible notes into the output, recording the `\TRACEcount` value at given key points (adding 
text to a chunk, joining vertical boxes, etc). `\TRACEcount` is output at major events in the log file (normally
`tracing{d}` lines), as in the sample below.

```
+19564: diglot@run@nxt@trial
n@xttrial L (R)
dglt@calc@vailht L
inserts: 0.0pt=0.0pt? 0.0pt=0.0pt?
final:468.54942pt
+19565: run@a@trial LRR, 468.54942pt>14.99442pt?, etp:-10005
partialL: 0.0pt+0.0ptx0.0pt
excessL: 0.0pt+254.90506ptx170.65913pt
Preparing for trial
Running trial 468.54942pt, 254.90506pt+0.0pt(0.0pt+0.0ptleft for next time)
diglot@any@trial 468.54942pt+0.0pthIns=0(==0 1st time) op=-10005, etp=-10005, d
c=1, xs:0.0pt+0.0pt, th:468.54942pt
```

Above there are two `\TRACEcount` marked events, 19564 and 19565. Also note that 
there are comments in the log file about expected results. `hIns=0(==0 1st time)` indicates that 
if hIns (\holdinginserts) is not 0 for the first entry into `\diglot@any@trial` after a trial is 
started then something has gone badly wrong.  As there's no point processing
inserts after the first chunk, the macro sets `\holdinginserts` to 1 for any 
subsequent calls.

## Extra visual tracing

Also potentially useful is:
```
\VisTraceExtratrue
```
Which enables extra visual tracing which (while useful) may alter the page
layout by a few points per page, and thus change the conditions triggering the 
bug you're trying to debug, so the intermittent fault hides again.
(This is *why* they are not enabled by the main `\VisTracetrue` toggle).

More detailed debugging code may be triggered by other tracing codes (see `ptx-tracing.tex`),
so that e.g. if you are trying to debug the calculation of `\availht` (height
left on the page), you may wish to  enable ```\tracing{Dh}```.

## showbox and showlists
If `\scrollmode`
is set (which scrolls past errors and normal stop conditions, carrying on until a fatal error is 
found) is set, some parts of the code automatically trigger extra debugging
when an unsual event occurs e.g. when they get told to add a zero-height box to
the page, they display its contents for inspection. Since showbox stops processing, this
automatic debugging output only makes sense in this particular case. 

Some of the `\TRACEcount` displaying trace points also have code to test the
value this counter with `\diglotDbgJoinboxes` As the name suggests, this
started off for displaying the content of boxes that were being joined.
Normally setting this will trigger the display of one or more boxes' contents
via `\showbox`, some positions e.g. trial-related locations the correct value
will also trigger `\showlists`.  For increased detail of the boxes, the numbers
`\showboxdepth` and `\showboxbredth` should be set to a higher number than the
defaults. (99 for each will almost certainly show you the entire box contents).




