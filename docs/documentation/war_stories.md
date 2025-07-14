# War Stories

This file contains stories of subtle user errors that one would not expect a
user to spot immediately. It differs from (snippets.md) in problems people have
had with their projects rather than discussing new features and capabilities.
See here for troubleshooting type stories and warnings and ways around such
problems.

## Processing FRT

### Problem

Lines of the form:

```
\periph Title Page|id="title"
```

Result in a TeX error:

```
! Undefined control sequence
\qt@st #1 -> \def \@@qt@st
    ##1#1##2\E {\edef \tmp {##2}\ifx \tmp \empty \qt@st...
```

### Investigation

It turns out that the " in the periph line is getting turned into smart quotes.
This is triggering the smart quote handling code in the TeX macros where it
shouldn't be happening.

What is causing the quotes to get changed is the user has a changes.txt file
that includes their PrintDraftChanges.txt file that has rules to change regular
quotes into smart quotes. By default these are commented out, but this user
decided to enable them. His changes.txt file is being run on the front matter
containing the periph.

### Solution

Changes.txt has the ability to group rules into sections that are only applied
in certain context. The default section for a changes.txt file is "default",
which is applied to scripture files, etc. There is also a section "periph" that
is applied to peripheral books. PTXprint runs the "periph" section over the FRT
book if it exists, otherwise it runs the "default" section. To stop PTXprint
from running the "default" section, we simply need to create a "periph" section,
which can be empty. Simply add

```
sections("periph")
```

as the last line of the changes.txt (thus giving an empty set of rules) and all
is well.

## Can't Print Due to Buggy USFM File

### Problem

The user's USFM file has a fault. But they only want to print the chapters that
occur before the fault.

### Investigation

There is a chicken and egg problem here. PTXprint does some of its work by
converting the USFM file into an internal XML representation, and then
outputting it again as USFM. One of the functions it needs the XML
representation for is subsetting the document to only print certain chapters.
But in order to read the USFM file it must parse. The parser in PTXprint tries
to be very forgiving and never fail, but that doesn't stop some files causing
problems.

### Solution

There is a section of the changes.txt file that is run over the USFM file before
anything else happens to it. This is the "initial" section. So, say there is a
bug in chapter 3 of Mark, we could use the changes.txt file to delete everything from
`\c 3` onwards:

```
sections("initial")
at MRK "(?s)\\c 3\s.+" > ""
```

The `(?s)` says to allow `.` to match new lines and everything, so the `.+` matches
to the end of the file.

