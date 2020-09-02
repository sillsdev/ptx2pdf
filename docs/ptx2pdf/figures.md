[+d_figures]::

Pictures in the PTX macros are based around the `\fig` marker. The macros are in
transition from being USFM2 based, with an ordered set of parameters separated
by `|` to USFM3 which is key = "value" based. The macros support both at the
moment.

The parsing of the `\fig` options is done based around the `|`. The main fig
routine repeatedly calls `\getonep@ram` which splits the input on the first `|`
and retains everything after the `|` for future processing by the same function,
until there are no more `|` in the data. Each time it calls `\getonepairp@ram`
to do the real work and also to split off the key="val" pairs. Notice that if
this is a USFM2 style `\fig` there will be no key="val", instead we will only
have `val`. So to get the pattern matching macro to trigger, we append an extra
`=""` which will in effect pass val="". This gets noticed in the macro.

[=cfig_getoneparam]::

The `\stripspace` macro is a nifty piece of TeX footwork to strip off any
initial or final space from its parameter. The string is passed in both as `#1`
and as `#3`. Consider, for example, the string ` a ` with a space on either end.
The call to `\stripspace a \end/ \end/\relax{ a }` will match with `#1` having a
value of 'a' having its initial space removed and any single following space
matched away, `#2` will be ` \end/` and `#3` is the full string. Inside
the macro `#2` is not empty and so we recall `\stripspace a\end/ \end/relax{a}`.
Now this time around `#1` is 'a\end/' since the first space for the pattern
match is after the `\end/` and `#2` will be empty, with `#3` containing the `a`.
This time inside the macro, the test is true and we store `#3` or `a` as the
result and we are done.

[=cfig_stripspace]::

Processing a single parameter involves comparing against a list of strings. The
easiest way to handle this in TeX is to define macros for them all. On entry
into `\getonepairp@ram` we strip any spaces from around the key and value. Next
we test the key against each of the known keys in turn and come up with a
positional number for the key. If this is USFM2 the positional number is the
previous one plus 1. Then we test the value. If it is empty we ask ourselves
whether we know we are in a USFM3 fig (because there was a previous key=value
pair). If not then store the parameter id as the value for the positional
parameter and there is nothing more to do in this `|` slot.
We then set a flag to fail the next test.

If we have not yet stored anything, use the parameter number as the index and
the parameter value as the value. We also prepare to go around again by skipping
the final whitespace and trying again. Since we have now hit a standard USFM3
type attribute, we set a flag to say to process everything else as USFM3. After
all is said and done, we either go around again or return.

[=cfig_getonepair]::

The `\fig` marker is redirected to `\d@figure` which we will describe here. But
it is over 300 lines long, so we will take our time over it. The basic idea of
this macro is to parse the options; create a box for the figure and then either
put it in the right insert or in the right place on the page. The whole thing is
dependent on figures being included, otherwise we ignore the marker. We start by
assuming we are in USFM2 and that the image is not to be rotated. We also
collect the current column size for later. Then we get hold of the data in the
`\fig` and append a final `|` whether it is needed or not. This ensures that the
pattern matching routines on `|` will finish.

The next step is to clear all the parameters. Since there is a fixed number of
these positional parameters, we can simply test the count against a constant.
Each time we undefine the positional parameter. Next we process the parameters
by passing them to `\getonep@ram` which strips off one string up to a `|` and
processes it as either a positional parameter or a list of key=value pairs. If
the rest is empty, then we are done, otherwise go around again.

Next we pull out some of the fixed position parameters and store them for later
use.

[=cfig_dofigure_intro]::

The `size` option needs specific parsing. `#1` is the size option. `#2` is a
scale factor and `#3` may be empty or `*` depending whether the is a scale
factor. Then we store the sizeoption and the sizemultiple for later use.

[=cfig_parsesize]::

In the next section of `\d@figure` we process more parameters. If the page
location (`pgpos`) then we come up with a default based on the size option.
Basically we default pictures to the top or top left. We setup default picture
width and height and set some default flags (1). We then define more defaults:
pictures align centred in their box and on the page (for page type pictures).

The `\p@cinswid` is the width of the box into which the picture will be placed.
We set the width and height of the picture based on its size option. For full
page type size options we clear the flag to use inserts for the picture and set
an appropriate location and picture width and height. Finally, for this section
we clear the insert identifier ready to set it.

[=cfig_dofigure_1]::

In anticipation of the next code in `\d@figure` we describe the process of
parsing the location option. The location option (as described for the `pgpos`
attribute) consists of one or more characters. The primary location is described
by the first letter and the sub location within that, with the rest. There may
not be a second, in which case it will be empty, since the pattern match is
bounded by `\end`. If there is a second parameter then we subparse that. The
second parameter may itself be 1 or more characters with the secondary position
as the first character and the tertiary position as the rest.

If the location is `h`, meaning an inline graphic, then capture the main
location and the second parameter is the alignment: `l`, `r` or `c`. Since we are
inline, clear the flag to store the picture box in an insert. If the alignment
is `l` or `r` then narrow the picture.

If the location is `c` for a cutout, then again we capture the main location and
clear the inserts flag. Pictures need to be narrowed and the space available is
the column width. We also collect any cut skip which says how many lines down
the cutout starts.

If the location is `p` for pictures that are placed in line after the paragraph.
The width is the column width and the alignment the second character: `l`, `r`
or `c`. There is no insertion. If the alignment is `l` or `r` then set the
narrow picture flag.

If the location is `P` for page then set the picture width to the page width.
Likewise if the location is `F` for full (page to edge), then don't set a width.
In either case warn the user we are entering experimental waters and set the
alignment to be the second character and the vertical alignment the third.

[=cfig_parsepicuse]::

Returning to `\d@figure` we are still processing parameters and setting
defaults. We parse the location. For `t` and `b` type locations, set appropriate
defaults depending on the number of columns and also set the insert to use. We
also collect the current height of that insert to subtract from the insert
height later.

If we are using inserts for this picture, then if we still haven't decided on an
insert to use then work out some defaults. If we are not in a diglot then we
don't need to worry about the current height of the insert. If there is
insufficient horizontal space for our intended picture width then complain to
the user. Count the number of pictures in our document.

[=cfig_dofigure_2]::

In this section we create the vbox for the picture. If the picture is
narrowable, we set the width of this box to be the scaled width of the picture,
otherwise we set the box width to the specified available width for it. The user
may have called for the caption to come above the picture, if so, insert it
here.

Now we start building up the command to insert the picture. We start by choosing
the command to use, the filename and any mirror attribute value. (1) We also collect
on which page this picture occurred in a previous run. We need this to decide
how to interpret the mirroring attribute. We also parse any `x-xetex`
attribute value. We will return to this later. Next we test to see if the
filename is a .pdf file. If it is, then change the command used to open the
file.

[=cfig_checkpdf]::

If the image is to be rotated, then fit the image based
on its height rather than width.

We insert the picture, scaling it according to its width. But if it turns out
that results in something too high, then we try again but scale it according to
the available height.

Now we create the figure box which is what appears in the document and consists
of either the picture or a placeholder. At this point we write details of this
picture to the `.picpages` file. If the user has asked for placeholders instead
of pictures, then replace the box with  a box containing the filename.

[=cfig_dofigure_3]::

We pause our description of the figure box to revisit the parsing of `x-xetex`.
Parsing starts with the
last routine here (1). First we clear out the remainder and test to see if we
can short circuit with nothing to process. Otherwise we process the attribute
'word' by 'word' (2). We test to see if the word or what follows is empty (i.e.
there must be at least 2 'word's. If so then we are done otherwise we parse the
first word as `key=value=angle`. Alternatively the angle may be missing as in
`key=value` or simple `value`.

We grab the value. If there is no key, simply pass the value to XeTeX as part of
the remainder. Otherwise we need to analyse the key and value. The only
recognised key is `rotate`. `\whichp@ge` is the target page and we use that to
decide which way to rotate an image for the key values of `bind` and `edge`. For
values of `odd` or `even` then also collect the angle which will be used if the
page constraint is met.

[=cfig_parsextra]::

Returning to creating the figure vbox we set up a few variables for later use.
If the image is to be mirrored then define a prepic macro. In this we decide
whether the image actually needs to be mirrored because, for example, the
mirror calls for mirroring on odd pages and the image is going on an odd page.
If the image really needs mirroring then insert the necessary pdf special to
mirror the following image. We also define the postpic command which, if the
image is being mirrored, needs to finish off the pdf special and stop the
transform. We then turn the picture box into a possible transformed (mirrored)
picture box.

If the picture is being narrowed then decide where to place it within the
column. For example if the image is right aligned then insert any stretch or
shrink (for overly wide pictures) on the left, before the image. And so on.

Finally, if the caption came first, then insert a little space, otherwise insert
the caption.

[=cfig_dofigure_4]::

We are ready to describe caption processing. We collect the reference attribute
from the figure and strip its space. We also collect the caption text. The
location is different for USFM3 from USFM2. If there is no caption then we don't
use the reference either and we simply insert a small post caption gap.

We set up for creating a paragraph based on the `fig` style.
We set the appropriate justification for
that paragraph. We also do not allow page breaks in this text (because it is
being processed into a separate box). We then set the baseline for this
paragraph. Then we prepare the reference, if there is one. The user can change
the `\DecorateRef` macro to change how references will be add to the caption (to
the point of deleting it). Finally we start the paragraph and perhaps insert the
reference with a non-breaking space followed by the caption itself and then if
the reference comes at the end a non-breaking space and the reference. The
paragraph is completed and we add a half space at the end.

[=cfig_docaption]::

Now that we have a box containing the whole figure, we need to put it somewhere.
In the case that the box is to be `insert`ed, we test to see if we are in a
diglot. If so then we compare our height with that of the corresponding insert
heights on the other side. If we are less than theirs, then we come for free and
so set the height to 0pt. Else set our height to the difference between our
height and theirs. Then we insert the picture as an `insert`. We do not want the
picture to go on a different page, so disallow any breaks here. Setting the
`\splittopskip` to 0pt says that if there is a column break just before this
picture, then pull the picture right to the top. And also allow any depth for
the box when splitting. But do not let this picture float.

Then we call the gridbox routine to insert space before the picture to ensure
that the next line of text after the picture will be on the text grid.

[=cfig_dofigure_5]::

The rest of the routine is concerned with inline figures that do not go into an
`insert`. First we work out how many lines big this figure is. Then if the
picture is inline then allow a page break before it and if the picture is
assumed to be narrower than the column width, rebox it to be a column's width,
inserting appropriate shrink or stretch. The rest of the routine is handling
each of the figure location types.

Inline figures are inserted into the
vadjust using a XeTeX extension (`\vadjust pre`) that says the insertion should
happen before the current line rather than after it.

Post paragraph figures are stored into a diglot side appropriately named box. If
the picture can be narrowed, then rebox to column width with appropriate shrink
or stretch. We now create a macro to run at the end of the paragraph (again
diglot side appropriate). This will execute after the paragraph is output. This
macro gets hold of the diglot side appropriate picture box we just allocated and
grids it at that point as if it were a headings block and outputs it into the
main text flow. It also allows a page break after the image.

Next we count the number of lines we want to skip this image and make a string
of `D`s of that many and store that for the post paragraph figure handler to
make use of.

[=cfig_dofigure_6]::

Page and full pictures are treated the same except that they are given a
different magic penalty number after each one. Again this is stored ready for
shipping out at the right time with the appropriate shipout routine.

Cutout pictures really do not like occuring mid paragraph. Ideally they occur at
the start of a paragraph before the first text. But if they do occur mid
paragraph then either start a new paragraph of the same type or else the marker
before a `\v` occurred.

We calculate the vertical size of the image rounded up to the grid plus however
many lines down we need to go; the width of
the image with a small 10pt margin and the amount of space left in the column
once the cutout is removed. If this is too small (<5em) then complain to the
user.

Inserting the cutout is basically the same for both sides. Only the position of
the shrink and stretch and which side the cutout is, differs. We create a new
box that pushes the image down to fit into the cutout. We make the box look 0
sized, insert it and then add the cutout to the cutout system.

[=cfig_dofigure_7]::

## Inserting Pictures

Part of processing a paragraph is the insertion of figures after a paragraph.
This gets called at the end of a paragraph break. We start by collecting the
diglot side appropriate end of paragraph tokens that may have been added in the
paragraph when a paragraph picture was inserted. These get stored in `\pn@xt`.
There are lots of reasons not to execute these tokens: if there are none; if
inside a note; if at the start of a page. If we have tokens to run and we want
to run them, then get the `Delay` tokens. If they are not empty, then we don't
want to run the tokens since this image is to be delayed by the number of
paragraphs. So trim off a `D` from the Delay tokens to correspond to this
paragraph and store that back in the same `Delay` token list. Then clear the
endofpar identifier. Otherwise if we do have tokens but we don't want to execute
them, then clear them and forget the endofpar identifier.

If, after all this, we still have tokens to execute then clear the origin of
those tokens and execute them. This outputs the image at this point.

[=cpar_doendofthispar]::

If there is a page picture to output, then we want to ship it out after the
current page. Each page output routine calls `\nextshipout` after shipping out a
page which hooks us in.

If there is a picture waiting to be output we split the vbox to the page size
and we rebox the result, leaving the remainder back in the `wholepagepic`. We
also capture the final penalty, which uses a protocol of special numbers to
communicate whether this image is a full page within margins or full page to the
edge image. If this image goes to the limits of the physical page then svae the
page width and height and ship the image as a page and restore the physical page
dimensions and advance the page number. Otherwise this is a normal page filling
image to the margins and we create a `pagecontents` that consists of the image
which we shipout via the normal route.

[=cfig_dofigpage]::

The special routine for shipping out a full page image is nearly identical to
the routine for shipping a page with cropmarks. It starts out identically by
adjusting the physical page dimensions to account for any additional cropmarks.
The page is shifted from the default 1 inch from top left that TeX uses. Then we
shipout a 0 size vbox with appropriate page information in the PDF. At this
point (1) the special routine becomes much simpler. It simply inserts a box of
the page size with shrink and stretch all round it, consisting of the box passed
in. Finally it adds any actual cropmarks.

[=c_shipcomplete]::

## .picpages

The `.picpages` file has a number of roles. It contains information about each
figure in the document including it's page number, the filename of the figure,
its `pgpos` the copyright information and anything else that may affect its
position and size. The `.picpages` file gets used by ptxprint to autogenerate
the copyright statement for the verso pages, for example. Within the ptx macros
the information is used to test whether figures have moved around or not. This
allows us to know whether a rerun is needed to help stabalise image positions.

The entry point to the `.picpages` handling is `\openpicpages` which reads in
the existing `.picpages` file if present and adds a hook to the end of the
document to see if any figures moved. In reading the `.picpages` file
`\figonpage` is called for each figure that was previously output. This then
saves an appropriate variable with information about the position of the figure.

As we go through we write new `\figonpage` calls into a new `.picpages` file of
the same name. Then at the end of the job, we reread that new file, but instead
of just storing the information, we switch to using `\checkfigpage` which
compares what has been read with what was stored for the previous read of the
`.picpages` file. If there are any difference, then a message is given to the
user implying they should rerun.

[=cfig_openpicpages]::

## .piclist

At the end of picture handling is the use of `.piclist` files which are at their
core a list of `\fig` statements, but without the `\fig` and with an anchor so
that the macros know where to place the figure.

`.piclist` files are read by testing that they can be open and then opening the
file and reading the first entry. At the end `\closepiclist` is called to close
the file.

[=cpic_read]::

`.piclist` files are read sequentially an interpretted sequentially. Only the
next picture is read and its location is stored. If that location never matches,
no new picture lines will be read, of if there is a syntax error, the rest of
the file will be ignored.

In reading a line from the file the catcodes of various characters are put back
to normal while the line is read. The next line from the file is read. If the
line is blank or empty then we keep recursing until we either get to the end or find
something worth parsing. Parsing a line involves expanding the line after the
`\parsep@cline` which uses pattern matching to break up the components. Thus the
syntax of a `.piclist` file is pretty strict. `#1` is the book id, `#2` the
chapter and `#3` is the verse. The verse needs to directly correspond to what is
found as the parameter to `\v` so may include briding elements or suffixes. `#4`
is everything that would be in a `\fig` range, thus may be USFM2 or USFM3.

[=cpic_parse]::

Before each verse (1), `\ch@ckpiclist` is run to see if a figure is to be
inserted at this point. The check creates a reference from the current book,
chapter and verse and this is tested with the current picture reference which
was created when the last `.piclist` line was parsed. If it matches then `dop@c`
is called which does the work of calling `\d@figure` to insert the picture and
then to read the next line from the `.piclist` file. And, in case there is more
than one entry for a verse, we check again.

If the check failed and we are in a diglot, then try again but add an `L` or `R`
suffix to the book id.

[=cpic_check]::


[-d_figures]::
