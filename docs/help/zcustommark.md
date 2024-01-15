# zcustommark
## Summary
Remember something for header/footer/etc
## Examples
```
\zcustommark|Jesus cleanses the temple\*
\zcustommark|type="keyword" value="Pontius Pilate"\*
```
## Description
Sometimes it is desirable to have the header or footer with something other than the chapter-verse or a page number, e.g. a section title or key term in the glossary. `\zcustommark` puts a (non-printing) value  called a *mark*  into the page contents which behaves much like chapter-verse references.

There can be many of different classes of mark (though probably just one or two is sufficient!), and this milestone allows those classes to be named. If no type is given, the default `user` is used.

For each class of *mark* ,   XeTeX records three values for a page's contents when it is built, and these values can then be used in the header, footer, thumbtabs, etc. The values are:

* **top** - The *mark* that was in force at the top of page.
* **first** - If the page contains one or more *mark*s, what was the first one? Else, the same as `topmark`.
* **bottom** - If the page  contains one or more *marks*, what was the last one. Else, the same as `topmark`.

If the top mark and the bottom mark are the same, then unless a mark has been duplicated, the page has no marks on it. If the first and bottom marks are the same, but not the same as the top mark, then the page must have one mark on it. 
There is, however, no method to distinguish between 2 marks and hundreds, nor to determine if a page has some particular mark value on it.

## Attributes
* `type="id"` What kind of mark is this? If not supplied, then the id `user` is automatically supplied.
* `value="something"` What should be remembered?  The content should almost certainly be plain text, without styling.

## See also
* [zcustomtopmark - the typeset page's **top** mark](zcustomtopmark.md)
* [zcustomfirstmark- the typeset page's **first** mark](zcustomfirstmark.md)
* [zcustombotmark - the typeset page's **bottom** mark](zcustombotmark.md)
