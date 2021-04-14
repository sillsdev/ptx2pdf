# Trigger code

TeX files may specify code (or usfm) to be added to the input 
at various places. The piclist and adjust list are specialist applications of 
this now generalised feature.

* ```\addtrigger{REV20.14-preverse}{\code}```
Run ```\code``` immediately before the verse number is
added to the output.

* ```\addtrigger{REV20.14}{\code}```
Run ```\code``` after the verse number is
added to the output

* ```\addtrigger{REV20.14=#}{\code}```
Run ```\code``` at the start of paragraph `#` of the
verse. (Paragraph 1 contains the verse number). Note
that the paragraph number resets at each verse. This
is equivalent to the adjustlist paragraph numbering,
not the piclist 'after N paragraphs'.
In some jobs the ```=``` separator may be altered from the default
```\SetTriggerParagraphSeparator{=}```


* ```\addtrigger{ms:zif}{\code}```
* ```\addtrigger{ms:zif=#}{\code}```
Run ```\code``` at any zif milestone, e.g.  ```\zif |file="foo"\*``` 
or (second case) at the start of paragraph `#` after
that milestone, assuming there are no other trigger
points such as verse numbers, milestones, etc.

* ```\addtrigger{ms:zid=1234}{\code}```
* ```\addtrigger{ms:zid=1234=#}{\code}```
Run ```\code``` at the uniquely identified milestone ```\zid |id="1234"\*``` 
or (second case) at the start of paragraph `#` after
that milestone, assuming there are no other trigger
points such as verse numbers, milestones, etc. 

# Trigger files
As a more friendly interface, trigger files  may be used.  Both job-wide 
(```[jobname].trigger```) and SFM-file specific (```Whatever.SFM.trigger```) 
trigger files are checked.

##  Trigger file format 
```
\NewTrigger REV20.14-preverse
\esb
\cat symbols\cat*
\s The lake of fire

\p The destruction of death and hades (the place of the dead) in the lake of
fire demonstrates ....
\esbe
\EndTrigger
```
Create an extended sidebar that will be triggered before the verse number for Rev20:14. Blank lines 
as in the example above do not trigger an error.

