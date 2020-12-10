# Trigger code

* ```\addtrigger{REV20.14-preverse}{\code}```
Run ```\code``` immediately before the verse number is
added to the output.

* ```\addtrigger{REV20.14}{\code}```
Run ```\code``` after the verse number is
added to the output

* ```\addtrigger{REV20.14-#}{\code}```
Run ```\code``` at the start of paragraph `#` of the
verse. (Paragraph 1 contains the verse number). Note
that the paragraph number resets at each verse. This
is equivalent to the adjustlist paragraph numbering,
not the piclist 'after N paragraphs'.


* ```\addtrigger{ms:zif}{\code}```
* ```\addtrigger{ms:zif-#}{\code}```
Run ```\code``` at any zif milestone, e.g.  ```\zif |file="foo"\*``` 
or (second case) at the start of paragraph `#` after
that milestone, assuming there are no other trigger
points such as verse numbers, milestones, etc.

* ```\addtrigger{ms:zid=1234}{\code}```
* ```\addtrigger{ms:zid=1234-#}{\code}```
Run ```\code``` at the uniquely identified milestone ```\zid |id="1234"\*``` 
or (second case) at the start of paragraph `#` after
that milestone, assuming there are no other trigger
points such as verse numbers, milestones, etc.

