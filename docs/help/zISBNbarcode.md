# zISBNbarcode

## Summary
Generate an EAN-13  barcode, possibly accompanied by an EAN-5 pricing barcode.
## Examples
```
\esb \cat ISBNbox\cat* 
 \pc \zISBNbarcode|var="isbn" height="medium"\* 
\esbe

\zISBNbarcode|isbn="zvar::isbn"\*
\zISBNbarcode|isbn="0-201-541991" \*
\zISBNbarcode|isbn="978-0123-456789" font="MathJax_Caligraphic" fontheight="8pt"\* 
\zISBNbarcode|isbn="020-1-541991" price="$14.99" pricecode="51499" font="Andika" \* 
```

## Description
Generate a barcode for a 13 digit or 10 digit ISBN.  If the `pricecode`
attribute is provided, also generate a price barcode, as required in some
countries.  Everything is scaled to the numbers below the barcode. 
Normally, the above-barcode text is scaled to match the width of the barcode,
however this might cause unexpected crashes with some fonts, in which case the
boolean `\noScaleAboveISBNtexttrue` can be set.


## Attributes
* `isbn="0123-456-789" Specify the 10 or 13 digits of the ISBN. Other numbers
will fail. *DO* include dashes in the correct place as specified by your isbn
regulator, but *only* use U+002D Hyphen/Minus for this, no other separator. If
a 10 digit ISBN is provided, the checksum will be recaclulated.
* `var="isbn"` If the `isbn` attribute was not supplied, use the zvar specified to get the ISBN. 
* `font="Andika"` use the given font for the font below the barcode.
* `fontheight="9pt"` use the given fontsize for the font below the barcode.
* `height="normal|medium|short"` Specify how much vertical space the barcode can take.
* `price="$9.99 / £8.99"` Text string for the price barcode
* `pricecode="0899"` 5 digits that should be encoded into the price barcode.
* `pricevar="isbnprice"` If the `price` attribute is not supplied, use this zvar to get the price.
* `pricecodevar="isbnpricecode"` If the `pricecode` attribute is not supplied, use this zvar to get the price code.

## Price codes
The price code is a 5 digit number, made up, according to Wikipedia, of a 1
digit national prefix followed by 4 numerical digits, with no decimal
separator. Conventionally the code 59999 would otherwise $US 99.99, but apparently 
it indicates a price of $100 or more.

First Digit | Description
------------|------------
0 & 1 |	British pounds 
3 | $ Australia
4 | $ New Zealand
5 | $ US
6 | $ Canada

As this system leaves most of the world out, it is important to consult local
standards and practices.  The `price` attribute is intended for human use.

## See also
[variable processing](zvar.md)
[Wikipedia article on EAN-5](https://en.wikipedia.org/wiki/EAN-5)

\StyleType Milestone
%Show a 10 or 13digit ISBN as an EAN-13 barcode
\Attributes isbn height? var? font? fontheight? price? pricecode?


