# Using ptxprint-mods.tex

While ptxprint has a number of controls to allow people to typset scripture in a
variety of styles, there are extreme cases where people need more control than
is available via the GUI. The designers of ptxprint felt that exposing such
controls to a wider audience of users could cause problems for the unwary. As
such they have been left off the GUI.

Thankfully, TeX is extremely configurable and there are numerous controls
available to users willing to type in some boilerplate type text into
ptxprint-mods.tex. This document aims to describe some of those controls, what
they do and how to control them.

## Basics

# \XeTeXuseglyphmetrics

Normally XeTeX measures the height of a line based on a fixed value as specified
by the font. This is equivalent of \XeTeXuseglyphmetrics=0. But there are some
scripts with extremely variable line heights for which setting a fixed line
height on the maximum possible would be uncomfortably wide for the average text
case. Readers are willing to put up with the occasional irregular wide line to
keep the minimum line height to something comfortable. The effect breaks the
regular line grid and will almost certainly result in slight errors in column
balancing (up to half a line). But that is a small price to pay in some
circumstances. Bearing all that in mind, if you really need such irregular line
spacing, then add:

```tex
\XeTeXuseglyphmetrics=1
```

to your ptxprint-mods.tex and have the surety of never crashing lines again.

# Display Paragraph numbers
```
\MarkTriggerPointstrue
```
Will add indications to the output of trigger points for paragraphs and verse numbers. These may be useful 
adjust-lists, triggers, or image anchors.

# Broken paragraph counting in diglots
Until late Nov 2021, paragraph counting in diglots did not keep track of paragraphs on a per-column basis.
It may be that adjust lists or triggers have been set-up relying on this aberrant behaviour.
```\def\KeepMyBrokenAdjList{}```
If this is defined, then old-stlye (broken) paragraph numbering for adjust lists and triggers will be restored.

```\let\KeepMyBrokenAdjList\undefined```
Will reset to correctly numbered paragraphs. (for the next USFM file read)




