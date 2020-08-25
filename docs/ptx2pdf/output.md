[+d_output]::
The output routines constitute the core of the typesetting system. They control
the layout of the page and is the most complex part of the system.

There are two layouts described here: single and double column. We start by
examining single column output. A document starts by setting the output routine
to `\onecol`. TeX collects paragraphs into the main page builder. Once the page builder has
more than a page full of text, the `\output` routine is called with the contents
of the main page in box255.

## Single Column Output

(1) The onecol macro takes this box and processes it by storing it in the `\galley`
box. This allows us to reprocess it as often as is needed during output. (+) Next we
do a noddy vsplit (to the maximum dimension so that everything goes in the first
box). This is just to collect any final mark on the page so far. And we set a flag
to say whether there are marks on this page. (+) We collect the `\outputpenalty`
which is the cost of the page break that caused the output to run. We will need
this to add it back when we put the excess back into the page builder to start
the next page. The page height used for testing for the best page break is
calculated. The `partial` box contains any material that was collected in a
previous forced page break. For example when we transition from single to double
columns at the end of introductory material at chapter 1. We switch the output routine to the processing
function whose job is to iterate the pagesize down until the text just fits on
the page. If there are no marks on the page then clear the first page mark for
the page. We tell the page breaker to extract the inserts from the copy of the
page we are going to reprocess. Then we reprocess the page and add on the
penalty we just copied.

(+) The TeXbook describes how an output routine is called. If there is a penalty at
the page break point, that is stored in `\outputpenalty` and a penalty in the
actual list is set to 10000. On the other hand, if there is no penalty, then the
`\outputpenalty` is set to 10000. Our aim to set the end of the contributions
list to be the same as it was in the main contribution list, i.e. with 0 or a
penalty. This also deals with the issue of not wanting to break pages mid
paragraph, at least for the output routines. This also explains why this has to
be done every time we use the contribution list to trigger a new output routine.

[=c_onecol]::

The next macro is what does the work of assessing and assembling the page. We
collect the marks for this page. We collect the height that is available for
this page, and will reduce it by the height of the notes and the top and bottom
inserts. For this we use the `\decr` macro that simply reduces by the skip and
height of the insert:
[=c_incrdecr]
At this point we test to see if there is any space left on the page for any
text. If not then complain, but keep going because if we reduce the original
pagesize perhaps one of the footnotes or a picture will not be on this page.
Continuing, we take a copy of the reduced page that we are seeing will fit on
this page. We check to see if when we split the text to the space left on the
page whether anything is left. If there is, then we will have to go round again.

[=c_onecoltrial_intro]::

But we examine what happens if it does completely fit on the page. If it does,
then it is the largest amount of text that does otherwise a previous round would
have fit.

The macro we create here returns a list of vboxes to be output as the main body
of the page, excluding headers.
We calculate the width of the page being the textwidth minus the ExtraRMargin
that allows for unbalanced pages. The side margins are set together to be the
same. This allows a user to unbalance them if they really want. The first vbox
is the partial content from a previous book or whatever. Then comes the topins
insert containing any top span images. Then we measure the depth of the main
text box and output it. If there is a bottomins (bottom span images) then we
remove the depth in order to get the content to balance, and output the
bottomins. Finally we output the notes. This is done using m@kenotebox which
outputs all the notes into box2:
[=c_makenotebox]::
This macro uses the note processing macros to collect the content of the notes
into the vbox2. If there are no notes, then potentially warn users that some
notes that were seen earlier haven't been output and perhaps some notes will
appear on the wrong page. Also if there are no notes, we turn the box into an
empty filler that expands to take up the rest of the page. Notice we have to
undo the initial note spacing kern. On the other hand if there are notes then we
take off the last box from the list, measure its depth, put it back and then
kern upwards to ignore the depth.
[=c_onecoltrial_pagecontents]::

Having created the pagecontent macro, we reset the vertical page size back to
full size:
[=c_resetvsize]::
Then, if there is actually some text to output we run the `\plainoutput` to ship
out the pagecontents. We also reset the page marks and if there are figure pages
to output, ship those out too. Otherwise there is no contents on this page so
dump anything that is left from splitting off this page (which should be
nothing). Now we prepare to return to main text processing. We start capturing
inserts again. But we may have been executed from a previous output routine that
found it had more than a page full while trying to collect for a partial page.
In which case we need to go back to where we came from and clear the flag.
Otherwise just set the output routine back to normal single column processing.
[=c_onecoltrial_pagefit]::

But what if the contents overfilled the page. We need to reduce the textheight
that the page breaker works with (`vsize`) and go around again. We do this line
by line in case there are figures or notes that would therefore be removed from
the page by such a reduction. The mechanics are pretty straightforward. We
reduce the `vsize` by a line; clear out the various insertion boxes; clear the
note boxes; clear the processing box and turn off insertion expansion. Then we
set the variable that tells the `backingup` macro which macro to rerun. Then we
set the output routine to the backingup macro and rerun with the same galley we
started with.
[=c_onecoltrial_fail]::

### Backing up

The backing up macro is a shared macro for all page layouts. This is the main
iteration routine for when the trial routine needs to reduce the page size and
try again. It resets `deadcycles` so that TeX won't complain if we have tried
more than say 25 times. Since this macro is an output routine, box255 is what
was output, which was the previous value of `galley` anyway. So we capture it
back into the galley box, and also capture the outputpenalty used. We set the
output routine to whatever we were told to make it. Since we are
running a trial, we want to expand out the inserts and again we reprocess all
the text, but with the new `vsize` so the cut will be in a different place.
Again we set the penalty.
[=c_backingup]::

### Partial Pages

The third component to a layout is the partial page macro that collects the end
of some text in that layout into the `partial` box ready to switch layout. The
macro starts by collecting the page bottom mark. We calculate a trial height and
then update it by inserts and notes.

c@lcavailht is the routine for calculating and setting up the various parameters
for a page measurement. It sets the marks and sets available height to the trial
heigth. Then it reduces  that available height by the heights of the notes, then
we round the result up to the nearest line grid. Then we subtract any top and
bottom inserts (figures). Advancing by `-\dp255` and `\dp255` just shifts the
grid somewhat (the amount of actual descent of the last line in the text).
[=c_calcavailht]::

Having calculated the available height we split the page to that height. If
there is nothing left then we are dealing with a simple partial capture.
Otherwise we will need to output a full page and then capture the rest.

The partial box is much like a page contents box. It starts with any previous
partial box followed by any top insert. Then comes the text contents and bottom
inserts. Then come any notes.

Since we have got to the end of a notional page, we reset the `vsize`. We ship
out any remaining ship outs. If there is text there is the added question of
whether this partial page takes up too much of a page to put anything under it.
In that case we ship it out as page content.

If, on the other hand there is more content than can fit on a page, then we need
to back up and reprocess as a single column full page, but we tell the single
page page output to call us back once it has finished. We do this by clearing
the insert and note boxes, telling backingup what to call and then calling
`backingup`.
[=c_savepartialpage]::

## Two Column Page Output

Two column output follows the same overall structure as single column output,
but it is more complicated. The `\twocols` macro is the output routine that is
called when a page fills in two column mode. This macro is identical to the
single column version `\onecol`, with the only difference being the output
routine that is called afterwards.

[=c_twocols]::

The trial routine is called for each trial page size. It starts by calculating
the available height for the text and copying the unsplit page. The next step is
to create two vboxes, containing the text for the two columns: `colA` and
`colB`. The aim here is to have both boxes be balanced, even if, due to column
specific images, they are not the same size. To do this we use the `\balanced`
macro.

### Balanced

The task of `\balanced` is to answer whether we need to go around again with a
smaller page size. It starts by setting up the intended column heights based on
the available height. It then splits the text into two columns according to
their heights. We use routines to do these functions.

`s@tcols` calculates the specific column heights from the given initial overall
height. It does this by subtracting the heights of the column specific inserts
from each column:

[=c_setcolhts]::

Splitting a vbox into the column boxes involves copying the text box and
splitting it into each column box in turn. If the break involved in splitting a
box is impossibly bad then the split is undone and that column box is empty. If
after splitting the column boxes the left column is empty but the right isn't
and the right could fit into the space then swap the boxes. On the other hand if
the left column is overfull and the right column is empty and has space, then
swap the boxes. Left and right in this discussion is swapped for RTL text. We
also collect the bottom mark based on what was split.

[=c_splitcols]::

Returning to balanced, we have done an initial split into two columns. It's
possible to specify a threshold as a number of baselines, that specifies if a
column is less than the threshold then shorten the page and go again. If there
is no more text left from the columns split then the text `fitonpage`. The
rebalance flag says whether to keep trying (with shorter pages). The basic loop
we will enter is measuring what if we were to shorten the page, with just the
text we have for this page, would we get a better balance between columns. For
example if the page is too long, then more text will end up in colA, whereas if
we were to shorten it, more would end up in colB until either we can't get all
the text in, or the columns balance.

Before that loop, we see if we haven't actually got any text onto the page. If
so then complain and put everything into colA and bail out. If the odd case
occurs that nothing was put on the page, but we consider the page full, then we
are totally confused and we bail the whole job! But enough of edge cases. If the
text all fits on the page, then we want to try to get a good balance. Otherwise
we are done and the calling routine can go around again.

We set up for the loop by calculating a `shortavail` variable which gets used to
decide how out of balance we are. It is the sum of the amount of space left in
each column after the split. If the difference is really bad then to save time,
we take the average of the two column spaces and reduce both columns by that
amount. Then we do a quick loop splitting the columns to see if they still fit
into the page. If not, increase the allocation for each column by a baseline and
try again. We try keep trying until we find a pair of column allocations that
will consume all the text (given even our starting values achieved that).

Since we are after a new overall available height, we need to think in terms of
the original `availht` that would result in the colhts we have. To do this we call
`\g@tcolhts`. This does the opposite from `\s@tcolhts` in that it adds back the
heights of the inserts:

[=c_getcolhts]::

We set our test height to the taller of the two columns. We then reduce colhtA
by a line and see if it would be less than colhtB, if so then we still need to
rebalance and we use colhtB for our test height. Then we advance the test height
by a line to make sure that the first time we go round the loop we process the
currently calculated heights.

[=c_balanced_intro]::

Now for the main rebalancing loop. We initialise it by keeping track of how many
times we have been around the loop. We also turn off overfull box warnings,
which have already happened for the boxes we are involved in. We don't need the
same warning 20 times. We enter the loop.

Inside the loop we advance the loop counter and reduce the test height by a
line. We copy the box of text and we adjust the actualy height by the depths of
the current columns. Not ideal, but better than nothing. Then we set up for this
new trial height and split to the column boxes again at this new height.
`rem@inder` if false, indicates that if the page is not
consumed at this height then we should backup and break out of the loop by
setting `\rebalancefalse`. We use the `rebalance` flag to tell us if we are
bailing from the loop and so not to do other tests. The next test is whether
either column is too short according to our threshold (as in really short as in
0 lines long). If it is then back up to the previous test height and stop
looping.

The next test tests the difference in full column beights (including the column
inserts). If the difference in heights is within a line of each other, we have
won. We calculate the resulting winning height as the greater of the two column
heights and then set the flag to say we are done.

The next two tests are boundary conditions. If the we are down to less than 2
lines or we've been around 20 times, then either reset the test height to the
starting value or just back up one line and stop looping. Otherwise go round
again and try a new shorter test height.

After finishing the loop, assuming we ran it and even if not, update the test
height with the greater of the depths of the two columns, set the official
returned requested column heights to the test height and resplit finally on the
actual s@vedpage we were tasked with splitting.

[=c_balanced_loop]::

### Two Column Trial

Returning to the two column trial routine, we have set up the trial height and
run `balanced` to try to balance the columns. We test to see if everything did fit
on the page. If it did but `balanced` left some over, then we didn't. On the
other hand if the page size has shrunk to 0 then anything will fit, let's just
ship a page and see if we can do better next time.

[=c_twocoltrial_intro]::

If we fit on the page, we better output it. The first thing we do is calculate
the box heights. To do this we get the full heights of each column, including
inserts. We then include those inserts into the two column boxes, also including
their text depths, which we set to be the same. We also return the height of the
tallest column including its depth as dimen3.

[=c_calcboxheights]::

As we output the page, the column boxes contain their column inserts. If the
right column is empty then make it empty, but not void. Set both boxes heights
to be the height allocated for them. We are ready now to create the pagecontents
macro that fills the core of the page. We start by calculating a width for the
contents. We output the previous partial content. Then we output any top insert
content. Then we output the column boxes. Note for right to left text, left is
right and right is left. I.e. really left is first and right is second. Then we
append any bottom inserts. Finally we output the notes as a single column.

To output the page, we clear the box we were passed and reset vsize. Then we
call the `\plainoutput` routine to ship out the page. We will examine that
later. We clear the page reference marks and shipout any extra pages for full
page figures, etc. We reset holdinginserts back to what needs to happen for
normal page building. If we were called by a partial page builder, then we need
to call it back, otherwise reset ready the output routine for normal two column
page building and put back any unused content.

If not everything fit on the page, then we need to reduce the page size a bit
and try again with a shorter page until it does all fit. To do that we have to
clear the various inserts and notes boxes, setup `backingup` to call us back and
set the output routine to `\backingup` and put everything back for reprocessing
at this new shorter height.

[=c_twocoltrial]::

### Partial Two Column Pages

When the macros transition from two columns to one column, then the two column
material needs to be collected into a `partial` box for later output when the
page ends. 

The entry routine for saving the partial page when in two columns is
`\savepartialpagedbounce` which prepares the way for calling `\savepartialpage`
by setting the stage in such a way as if a previous page had just been output by
`\twocoltrial`. It sets up the trial height and calculates an `availht`. It sets
the page length to double that size (for two columns) but reduces that by one
line. _why?_ It then sets the output routine to `\savepartialpaged` to do the
actual page processing. It collects the output text into a galley box and
reboxes it at its natural height, in case it has been forced to a height. It then splits
the box to infinity to get the bottom mark. It turns of holdinginserts so that
the inserts get pulled out into boxes and reprocesses the main text passed in
and forces a page break. No need for subtleties here since we are wanting to
force output.

_The reason for the bounce is to do with holdinginserts=0 when we need 1_

[=c_savepartialpagedbounce]::

Now we come to the actual saving of the partial page. This is much like the two
column trial. We start by calculating the trial and available heights. We
collect the saved page at a natural height (no stretch of shrink). The natural
height is probably only useful for debug.

If there is no room on the page, we still balance because it sets things up for
us, even when there is no space. But normally we balance the columns. If
everything fits on the page then we have all we need to collect the partial box.
We calculate the two column boxes and their heights and we collect the
depth of the previous partial box. In creating a new partial box we include the
previous partial box and then undo the vertical space added for the depth of the
box. This is doubled because it was added when the partial box was created and
it was added in the unvboxing (_this is probably nonsense_) The we add the top
insert. Then we calculate the width of the two columns and the gutter and create
a box that horizontally has the first column, the guttern, the second column and
any `ExtraRMargin`. The order is reversed for right to left layout.

[=c_savepartialpaged_intro]::

The column gutter is not the simplest thing to create and so we have a macro for
it. This is given the height of the column boxes to calculate the height of the
vertical column gutter rule, the height of the column boxes again to give the
height of the box that is to be returned and the maximum depth of the two
columns, which is a side effect of running `\c@lcboxheights`. From these we
assemble a box that is centred. If there is a ColumnGutterRule then we create a
vertical rule of an appropriate heigh inside an hbox which is shifted down by
the ColumnGutterRuleSkip. This whole box is given an appropriate depth as passed
in and then centred with a right hand column shift. This is passed back for
inclusion in the horizontal list of boxes. 

[=c_makecolumngutter]::

The resulting horizontal list, for left to right is: colA, hfil,
vbox(hbox(vrule) vrule) hfil columnshift colB ExtraRMargin.

Having created the partial box, we reset ready to resume text collection. Then,
now that we have a new partial box, we calculate the space left on the page. If
it's less than 2 lines, we ship out a completed page and then put all remaining
text (of which there should be none) back onto the contributions list, with a
reset penalty.

But, if the text does not fit on a page, then we need to output a page to use up
the text and try again. To do that we empty the insert boxes and set up the
backingup to use `\twocoltrial` which we also set up to call us back when it is
done. If the galley is empty then use whatever was passed to us, now in
`s@vedpage`, otherwise use the galley.

[=c_savepartialpaged]::

## Switching Column Layouts

There are two macros that switch between the two layouts. The first is triggered
when switching from single column to double column, for examples between
introductory material and the main text of a book. We start by undoing the
last depth to bring the baseline back to the baseline and then close of any
headings. Between layouts is a pretty good place to break and if there is no
break here, insert a line's worth of gap. Now collect the current contributions
into a single column partial. We measure the partial to see if it is larger than
the specified PageFullFactor of a page. If it is then set up to output as a full
single column page. Since there may actually be a number of pages worth, which
will all be output, we reduce the measurement to modulo a page size. Then unbox
the partial back into the contributions and if we still are over the
PageFullFactor then fill up the rest of the page and force the page break.
Otherwise switch to collecting into partial and force the page break to collect
it.

Now set up for 2 column mode. Set the `hsize` and `vsize` taking into account
partials and that we double the `vsize` since we need to fill two column's worth
of text before page breaking. We redefine `\resetvsize` so that it does that
appropriately for 2 columns. Then set the appropriate output routine for page
breaking and we are now in 2 column mode. Top and bottom inserts basically cost
double because they take up space in both columns. We reset the count for each
note class, described below.

[=c_doublecolumns]::

Each not class, since it is associated with an insert, has a count associated
with it. This count is a multiplier of the size of the insert against the
overall height of the page. The routine to clear the count for a particular note
class finds the particular note class for a note type. It is then checked for
whether it is paragraphed notes (those that run on into one paragraph total for
all notes). Then the count for the insert is set based on paragraphed notes
costing 0, diglot notes costing half and full width notes costing whatever a
span insert costs, which for double column is 2. In addition every note has an
`AboveNoteSpace` fixed cost as well.

[=c_setnotecount]::

Switching to single column mode is somewhat simpler than switching to double
column mode since there is no worry about the grid. We close any headings and
set up to capture the current content into a 2 column partial. Then we simply
eject twice to really ensure everything is output. Then we set up for single
column working with `hsize` and `vsize. If the partial page is enough to trigger
a complete page, we output that. Then we reset to single columns and change the
output routine to single column layout. As per the other we set the cost of a
span to 1 and set the costs of notes accordingly.

If the partial is not empty, we reset it to its natural height and then consider
what to do because we are basically between books. If we are not to eject
between books then we need to set the first mark for the new book otherwise we
insert a line gap and then insert a rule across the page with a 2 line gap under
it.

[=c_singlecolumn]::

## Shipping Out The Page

The driving routine for shipping out a page is `\plainoutput`. The routine
conserves the pdf page dimensions, which the `shipwithcr@pmarks` may modify.
Then it passes a box for the page to the routine that adds any cropmarks. The
contents of that page are the head line the page body and the foot line. After
that we restore the pdf page dimensions and advance the page number. There is
check that the document is not stupidly long. The value of `@MM` is 20000 and is
only emmitted in a supereject. Thus we are merely passing the supereject along.
Otherwise clear various flags.

[=c_plainoutput]::

The routines for creating the components of a page are not too complex. The
`\pagebody` routine just makes a box of the pagecontents. `\makeheadline` does a
bit more work in creating a box that is of the right height and shifted
appropriately for the head line. First it sets up to use the `\h` styling
information. Then it creates a vbox that looks to be 0 size, but is in fact
shifted up by the `topm@rgin` so that it touches the top of the paper. Then it
contains a vbox which is shifted down by the `\HeaderPosition` multiplier of
`\MarginUnit`. Then we create a box of the headline. The box is set to be 0.7
times the ascender of the `\h` font, and the headline box is added to the top
box we are creating. If there needs to be a heading rule, then this is
positioned and added. The inner box has infinite stretch and shrink added so
that it's size can be 0.

The footline is much simpler. It is merely a 0 height box containing a shift to
the bottom of the paper and then back up to the `FooterPosition`, where an hbox
of the correct width is added containing the footline macro expansion. Again
infinite vertical shrink and stretch is added to keep the box 0 height.

Details of the `\headline` and `\footline` may be found in the References
section.

[=c_pagebody]::

We are slowly following the path to the actual `\shipout` command that is found in
this routine. First we grow the pdf page if there crop marks are being added,
otherwise not. We undo TeX's default of shifting the page by 1in and then we
shipout the vbox for the page. Inside the vbox we insert special PDF structures
to store details about the page size. This is primarily towards providing
PDF/X1-A support. Next we decide which side any gutter margin goes on. Then we
do some magic for a certain class of document. Such documents achieve vertical
text through:

- Rotating the page so that left to right text is rendered vertically from top to
  bottom.
- Instructing TeX to assemble lines from the bottom of the page to the top.

`\ifrotate` is set in the first case. To ensure consistent results, we turn of
the uer's assembly issues. Also turn of rendering paragraphs from bottom to top.
We achieve the rotation by inserting a special to tell the xdvi converter to
rotate the page for us. After this we merge in any page specific underlays. The
`\m@rgepdf` is for watermarks. `\pl@ceborder` is for bringing in special page
borders. `\offinterlineskip` tells TeX not to output any inter line
space which might follow the `\special` or images. At last we come to the actual box that
is set to the PDF page height, but can stretch or shrink either way to keep its
contents in the centre vertically. Likewise it contains an hbox corresponding to
the page width containing the contents of whatever is being shipped out. Again
this is centred horizontally, even if it is wider than the box. Finally we do
any cropmarks.

[=c_shipwithcropmarks]::

Actually outputting any cropmarks is done by `\docr@pmarks`. If no crop marks
are to be output, this routine does nothing. If the two boxes for the top and
bottom crop marks don't yet exist, then make them. Then we create a 0 size vbox
containing the top and bottom crop marks carefully positioned. Also in the
bottom crop marks we output whatever is in `\c@rrID`, again into a 0 height box
with whatever shrink or stretch glue is needed after it.

[=c_docropmarks]::

Making the crop marks boxes is all about rules and kerns in the right place. The
top cropmarks box contains a horizontal line 25pt long starting 30pt to the left
of the page. Then a vertical line that is 25pt but is 5pt away from the other
line. So the lines would join, if extended, at the corner of the main page box.
But they are given a 5pt margin. Another line that is slightly shorter at 15pt
is output in line with the top margin down within the page. As text, across the
top between the crop marks, is output the jobname and timestamp. Then the
corresponding lines are drawn on the right hand side.

The same happens for the bottom box except the text along the bottom is
generated per page instead of per job and the margin lines correspond to the
bottom margin.

[=c_makecropmarks]::

[-d_output]::

