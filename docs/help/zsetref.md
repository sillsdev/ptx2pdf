# zsetref
## Summary
Tell the code where the next bit of text is from.
## Examples
`\zsetref|book="GEN" chapter="5" verse="6"\*`
## Description
In certain circumstances, mainly in modules, XeTeX may have no idea what book or chapter a given paragraph is from. That makes it impossible for it to determine which triggers, images, etc. should be included when it meets e.g. `\v 10`
 This milestone is provided to supply that information.
 
## Attributes
* `book` The book name
* `bkid` The book ID
* `chapter` The chapter number
* `verse` The verse.
