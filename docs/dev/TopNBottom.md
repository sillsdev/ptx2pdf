# Top and Bottom

## Introduction

So far in the ptx macros, we have been able to do side by side typesetting of
single and double column, full page, text. Another approach to pairing data is
to split the page horizontally. Once we can do that, we can then split those
horizontal panes into multiple columns themselves. This then gives us access to
all kinds of layouts: study bible, multiglot, etc.

This document is a discussion document towards what would need to be written to
support top and bottom panes. So far we have been able to do a little bit of
adding panes via treating text boxes as top or bottom figures. But this is
insufficient for real flowed text. The height of the panes needs to be
calculated in terms of the amount of synchronised content we can fit in and this
involves us in a different kind of balancing, that the figure boxes approach
cannot address.

To help in the discussion we introduce some terminology:

**Pane** A pane is a variably sized area on the page that contains content that
come from a particular flow. Each page contains all the same panes, unless they
are empty for that page.

**Flow** A flow is a collection of content intended to be output in a pane. Text
may enter a flow through various means. For a diglot, different source texts are
merged with the various sources being routed to different flows. A flow may also
be fed by inline notes in the main text, which itself is being routed to the
main flow.

**Main Flow** The main flow is the driving flow of what is considered the main
text and governs what is on a page. It is not necessary to have a model that
involves a main flow.

## Models

Here we discuss various solutions to the problem.

### Mark Synchronisation

The basic principle is that for the various flows of text a page will consist of
the same amount of content such that the page contains the same marks in all the
flows. Marks are considered ordered and no pane may contain a mark that is
greater than the last mark in the main flow content for that page. Thus if the
main flow has a final mark of 3.15. Other panes may contain text up to 3.14 (if
they have no 3.15) but may not contain text with 3.16. This brings us to a
second mark constraint. No pane may contain text with a mark that is less than
the first mark on the page in the main flow.

To achieve an appropriate flexing in what text is on a page, it is probable that
the first marks and last marks will be of different classes. This allows a page
to start a note on a verse and complete it on the next page, for example.

Mark synchronisation allows us to measure how much space is needed on a page for
a given amount of main flow text.

### Measure and Allocate

One basic model for pane size calculation is to work out the text from each flow
and then to measure the required pane size for that amount of text. If the total
space is greater than the space available on the page, then we reduce the amount
of main text flow text and so also the other flows and try again, until we have
a set of panes that will fit. This can be done via binary search. The aim being
to know the sizes of each of the panes. Once we find a position that will fit
all the text on the page, we go back one step to the smallest amount of main
text that will overfill the page. Then we trim each pane in priority order until
the text fits. This is done line by line.

This approach differs from the existing page building that knows the required
pane size before it starts and therefore does not need to calculate the space
needed, just how much text will fit into the given pane size. I realise this is
somewhat simplistic since the pane size does change with content, due to inserts
and footnotes.

We would therefore, probably have to write a new set of output routines to
implement this algorithm. How much can then be shared into the new code or
shared back, remains to be seen.

