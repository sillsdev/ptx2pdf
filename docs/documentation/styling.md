
# Application of styling in complex situations
Consider this example piece of USFM.
```
\p
\v 1 The Angel of the \nd Lord\nd* said, <<\qt-s|Angel\*Thus says the \nd Lord\nd* ...
```

Styling of items such as ```\nd``` are relatively simple matters, but there are more complex casese.
## Styling of ranged milestones
Milestones such as `\qt-s \* ... \qt-e \*` define a range of text that cuts
across normal boundaries of paragraphs or word styles. 


```
\Marker Angel|qt-s
\Color x00FF00

\Marker qt-s
\Color x00007f

```

With the above custom stylesheet then: 
* The USFM code ```\qt-s|Angel\* ... \qt-e\*``` will mark all text bright green;
* the USFM code ```\qt-s\* ... \qt-e\*``` will mark all text dark blue (matching the unattributed definition);
* the USFM code ```\qt-s|Pilate\* ... \qt-e\*``` will normally mark all text dark blue
(because there is no ```\Marker Pilate|qt-s``` entry in the stylesheet overriding the value(s) of the default). If this fall-back to the unattributed style is not desired the command:
```
\AttrMilestoneMatchesUnattrfalse
```
may be given. Note that this affects all milestones.



## Introduction to the style stack. 
The XeTeX code has a concept of a 'style stack', a pile of  styles that may are active at any moment in time.

As processing moves through the text the stack takes the following values, `+` can be read as "added to"
1. `p`
2. `v + p`
3. `p`
4. `nd + p`
5. `p`
6. `Angel|qt-s + p`
7. `nd + Angel|qt-s + p`
8. `Angel|qt-s + p`

Occaisionally it is useful to specify a particular styling for not just the very top stack entry, but 
the top two (in the given example, an `\nd` following the `\qt-s`), or even the entire style stack.
This is possible using the method below.


###


