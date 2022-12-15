# Covers

## General principles
The cover-generating macro (\\m@kecover) arranges four sidebars to make the cover:
1. The whole cover : `cover_whole`
2. The front cover : `cover_front`
3. The back cover : `cover_back`
4. The spine : `cover_spine`

The front, spine and back are laid up (on top of the `cover_whole` sidebar) in 
a sequence determined by the boolean `\ifBookOpensLeft`.

The contents are drawn from the three USFM-3.0 periphery sections :
`frontcover`, `backcover` and `spine`, plus an additional (and normally empty)
`wholecover` periphery.

An sample cover might have contents such as this:
```
\periph front|frontcover
\vfill
\esb \cat TitleBox\cat*
\mt3 The 
\mt1 Test-case Bible
\esbe
\vfill
\esb \cat footbox\cat*
\pc \sc Atlantis\sc* 2022
\p
\esbe
\p ~

\periph spine|spine
\pc The Test-Case Bible
\p

\periph back|backcover
\pc Test-Case
\vfill
\esb \cat ISBNbox\cat*
\pc \zISBNbarcode|isbn="978-012345-689-2" height="normal"\*
\esbe
\pc 0 copies, Klingon-Esperanto
\b
```

Each sidebar may have the normal array  normal sidebar foreground and
background images and colours may be defined (but clearly, not all options or 
combinations make sense).

## Parameters

```
\expandafter\edef\csname cover-bleed\endcsname{3mm}   % Bleed dimension
\expandafter\edef\csname cover-spine\endcsname{11.23mm}   % Actual spine width = book thickness, endpapers, board thickness, etc.
\expandafter\edef\csname cover-y\endcsname{21cm} % spine/book height 
\expandafter\edef\csname cover-x\endcsname{14.85cm} % Front/back cover
\expandafter\edef\csname cover-back-spinewrap\endcsname{0mm} %  Should the graphic/colour on the spine be given extra space?
\expandafter\edef\csname cover-front-spinewrap\endcsname{0mm} % 
```

The first four TeX values above determine the physical shape and size of the
cover. 
The final two allow the spine colour / image to wrap onto the
front / rear cover as is seen in some editions. 

## Special Formatting 
### Wrapped spine:
The revised Cornilescu Bible, (EDCR 2019, Societatea Biblică Interconfesională
din România,  ISBN 978-606-8279-63-3) has a solid background on the front and
spine that wraps approx 2cm onto the back cover, where a contrasting colour
provides a background for the majority of the rear cover.
To set up a similar cover, the `cover_front`, `cover_spine` and `cover_back` could have 
appropriate background colours set and the parameter `cover-back-spinewrap`
could be set to `2cm`.
### Upper/Lower band: BoxPadding for the whole cover.
Testing demonstrated a strange effect came about from setting the `BoxTPadding` and `BoxBPadding` 
style parameters the `cover_whole`, sidebar, where the covers were pushed off the page. This 
has been embraced as a (probably rarely used) feature: if these padding values are set 
to `>=1pt` then the upper and/or lower bleed is turned off for the other 3 sidebars, 
and background colour for the upper and lower edges will be set by the `cover_whole` sidebar.
Note that nothing from these sidebars should be able to reach into this area.





