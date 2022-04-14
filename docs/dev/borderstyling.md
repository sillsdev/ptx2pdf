## Named border styles
`\SetBorder`  Defines a new border style. `\SetBorder foo` is precisely equivalent to `\Marker b@rder-foo` 
`\BorderRef`  Defines indicates that the present style inherits the border settings from another style.
`\BorderStyle` Can is overloaded. If the given parameter not recognised as a valid procesing engine (plain, double, or - if plugin is loaded - ornaments), then it calls `\BorderRef`


###  Ineritance processing.
Inheritance processing is a once-only step which occurs at the first USFM file. There can only be one parent from which a style 
inherits. However nesting of A builds on B which builds on C (etc) is allowed.
The process operates as follows:

1. When a `\BorderRef womble`  is encountered:
  a. The param `borderref`  is set to womble 
  b. the current marker is added to `\dep@ndlist`.
2. When inheritance processing is underway `\dep@ndlist` is read item by item.
  a. If the item pointed to by the borderref does not exist, a warning is given
  b. If the item pointed to by the borderref  has itself a non-empty `borderref`, the item is postponed
  c. Each item in the list of border parameters is checked. If there is no value, the value from the borderef item is copied
  d. The borderref entry for the item is deleted.
3. If the list of postponed items is not empty, `\dep@ndlist` is set to the postponed list, and the postponed list emptied. Go to 2

### Results of this
As with normal stylesheet parameters, anything defined in any `\SetBorder` can be overridden (before the first usfm file), and takes 
full effect. Input sequence is only important in that the last-read file wins. 
The sidebar or zrule definition may include or override any setting.

