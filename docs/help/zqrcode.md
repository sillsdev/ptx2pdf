# zqrcode
A milestone that will generate a QR code
## Examples
```
\zqrcode|data="http://link.to.web/page" cat="oneside"\*

\zqrcode|pgpos="H" background="1 1 0.5" colour="0 0 .5" vmax="2" unicode="T" size="1.5cm" data="http://somewhere.com/țară.html"\*

```
## Description
 Generates a QR-code from attribute data (which may not contain double-quotes), with the specified size (or from FontSize, if cat is provided). 

While the ISO standard allows codes to be as small as 1cm, and the code can generate them at any size that fits on the page, it is generaly recommended that a QR-code not be smaller than 2cm, for scanning at 20cm. Lower-end phones may not be able to focus sufficiently closely for smaller codes. The resolution of the printer also impacts the size of a printable QR code (see section later on)

## Attributes
* `data="contents"` the data to be turned into a QR code.
* `unicode="T"` If `"T"` then a small temporary file is written and re-read byte by byte. This reduces processing speed, but renders unicode data correctly. Otherwise, that step is skipped, but if unicode characters (outside the range U+0000 to U+007F) are used in the data, then either there may be crashes or the QR code will not be generated properly, (testing shows the latter, but crashes are not impossible).
* `size="2cm"` Set the size (including 'quiet zone') to 2cm, or whatever. (any TeX measurement can be used, e.g. `cm`, `pt`, `bp`). If not given, the style-sheet's `fontsize` setting will be used, in the same units as fonts are normally set to. 
* `cat="category"` Select a particular category of QR code from the stylesheet (i.e. `cat="sections"` will look in the stylesheet for  for  `cat:sections|zqrcode`, falling back to styling for `zqrcode` for missing parameters).
* `pgpos="position` Position  can be 'H' (a simple box, here), or any valid figure position. 
* `vmin="number"` Specify a minimum version. Potentially use a more complex code (more dots) than the default would.  See section on typesetting implications below.
* `vmax="number"` Specify a maximum version. Create an error if the "version number" (complexity) of the QR code is too high. I.e. the data is too big. Potentially reduces error-correcting below the default level to save dots. See below.
*  `colour="R G B"` set the foreground colour for the QR code (overriding the stylesheet `color` setting). `R` `G` and `B` are decimals in the range of 0 to 1, e.g. `colour="0.1 1 0.3" . American spelling is also accepted.
* `background="R G B"` set the background colour for the QR code.
* `spacebeside="5pt"` Specify the `spacebeside` value for this QR code - a horizontal measurement tweaking the position/spacing of the QR code (see figure documentation).   If not given the  stylesheet's `spacebeside` setting will be used (or `0pt`).

## QR code Versions
The QR code generator does its work automatically. I.e. you probably don't need to know this. What follows is to help the typesetter understand what's going on and why, and how to get the most out of the capabilities.

QRcodes exist in different '*versions*'. The version number (up to 40) determines how many 'modules' (dots) are on each side - 4 × version number + 17 dots on each side.  A QR code always contains some data reserved for error-correcting, but the *amount* of error-correcting data varies, depending on the 'error-correcting level'.
The number of characters that can be encoded further depends on the
*type* of data: numeric data is the most efficient, (3.33 bits/character); then alpha-numeric (`0-9`, `A-Z`, space and a few symbols, but **no** lower case -- 5.5 bits/character); or other 8-bit data. Unicode data is stored according to UTF-8, and so may require several 8-bit bytes.

### Some gruesome details...
There are 4 error correcting levels, (`L`, `M`, `Q` and `H`, with Q and H being recommended for use in dirty environments, and M being considered 'normal use').
**A QR code does not necessarily contain a single type of data**, and the type of data must also be encoded (further reducing the number of  bits available for data).

### Helpful result
If a URL can be written with only upper-case and does not contain `&`,  `?`, `#` or quotes,  then it probably all qualifies as alpha-numeric.  However, while site-names are case-insensitive (and thus, if written in upper case can be encoded more economically), the rest of the URL is case sensitive (i.e. the link [HTTPS://EN.WIKIPEDIA.ORG/wiki/QR_code](HTTPS://EN.WIKIPEDIA.ORG/wiki/QR_code) is still a valid link, and a long block of alphanumeric data like this will be encoded more economically than the more normal version of the URL).

### Capacity of some QR code versions
Version | Size | Data bits: ... L | ... M | ... Q |... H | Bytes of binary data
---------- | ------| ----------- | --------- | ---- | ---- | ----
1 | 21x21 | 152 | 128 | 104 | 72 | 7-17
2 | 25x25 |  272 | 224 | 176 | 128 | 14-32
3 | 29x29 | 440 | 352 | 272 | 208 | 24-53
4 | 33x33 | 640 | 512 | 384 |288 | 34-78
5 | 37x37 | 864 | 688 | 496 | 368 | 44-106
6 | 41x41 | 1088| 864 | 608 | 480 | 56-134
8 | 49x49 | 1552 | 1232 | 880 | 688 | 84-192
10 | 57x57 | 2192 | 1728 | 1232|976 | 119-271


### Size implications of versions
If  a home-style printer is being used, which might have a resolution of, say 600dpi, then 1pt (1/72.27 in) represents just over 8 printer dots. That's not many dots to draw a square, especially since a printer's nozzles sometimes block. Probably 1pt squares are going to be too small to be printed / read reliably. It might be decided that each 'module' in the QR code should be at least 16 printer dots, or 1.92pt. Even that would probably give some noticable pixelised effects if there were no fuzziness from the ink/toner. This example gives the following minimum sizes for the printed area:

| Ver | Size | Dimension at 1.92pt/square
|------| ------ | ------------- 
| 2  |  21x21 | 1.67 cm 
| 3  | 29x29| 1.94 cm 
| 4  | 33x33 | 2.2 cm
| 5  | 37x37 | 2.5 cm
| 6 | 41x41| 2.75 cm
| 8 | 49x49 | 3.28 cm
| 10 | 57x57 | 3.81 cm

**NOTE** that the size parameter for `\zqrcode` is the total size of the code, including the surrouding frame or 'quite zone'.

### Typesetting implications of versions
From the above, it should be clear that visually similar QR codes (same number of dots per side) can hold different quantities of data.  If consecutive pages in a publication have QR codes, (representing, say, links to on-line media for the relevant sections), it may be preferable that all be the same version despite variations in the link length. It may also be preferable to enforce a maximum version number to force an error rather than print a URL which will have dots too small to scan in practice. E.g. a QR code of size 2.5cm shouldn't 
This is the motivation for the `vmin` and `vmax` parameters.

## Further reading
* [Wikipedia article on QR codes](https://en.wikipedia.org/wiki/QR_code) 
* [Data sizes of QR codes](https://www.qrcode.com/en/about/version.html)
* [figure documentation](../documentation/figures.md)