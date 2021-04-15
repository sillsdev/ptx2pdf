# Trigger mechanism

In addition to the special-purpose `piclist` and `adjlist` files, there are now
two methods to insert generic USFM mark-up or TeX code into the input.  Both
methods use the same mechanism, indeed the same mechanism is used by piclists
and adjustlits (with some behind-the-scenes modifications) and specially
formated files. In a `.tex` file (e.g. `ptxprint-mods.tex`), it is possible to add
short pieces of text or code like this:

```\addtrigger{REV20.14-preverse}{\code}```

Which will execute `\code` at the specified trigger point. Note that `\code` here cannot 
include any USFM codes such as `\s1` that contain a number, and nor can it
include any blank lines.

As a more friendly interface, separate trigger files  may be used.  Both job-wide 
(```[jobname].trigger```) and SFM-file specific (```Whatever.SFM.trigger```) 
trigger files are checked.

##  Trigger file format 
``` 
\AddTrigger REV20.14-preverse
\esb
\cat symbols\cat*
\s1 The lake of fire

\p The destruction of death and hades (the place of the dead) in the lake of
fire demonstrates ....
\esbe
\EndTrigger
```

This will create an extended sidebar that will be triggered before the verse
number for `Rev20:14`. Blank lines as in the example above do not trigger an error.

There are three classes of trigger point -- those expecting words, and those expecting 
a block (in-line image or sidebar, or paragraphs of text), and those that
tolerate either well. Either may be used to trigger, say, a side-bar that does
not appear inline, and if the original pararaphing is to be interrupted then
blocks can occur in either.  See later for *inappropriate* uses.


## Trigger points expecting blocks (if at start of paragraph) or words
* ```REV20.14-preverse``` Triggers before the verse number. 
* ```GLOk.LakeofFire-preverse``` Triggers before the glossary entry ```\k Lake of Fire\k*```
* ```ms:zif```	Triggers before any stand-alone milestone  of type ```zif```, e.g.  ```\zif |file="wombats"\*```
* ```ms:zwombat=a542``` Triggers before the unique stand-alone milestone ```\zwombat| id="a542"\*```
* ```Borrogroves``` Triggers at any stand-alone milestone with a matching  id ```\zfiga|Borrogroves```

## Trigger points expecting words.

* ```REV20.14``` Triggers mid-paragraph, after the post-versenumber space.
* ```GLOk.Herrod``` Triggers mid-paragraph, after the glossary entry ```\k Herrod\k*```

## Trigger points only expecting blocks 
NB for all of these (and piclist entries) ```\SetTriggerParagraphSeparator{=@=}``` or similar may be used to define the
separator between the identifier and the paragraph number if ```=``` is somehow inappropriate.

* ```REV20.14=2``` Triggers before any content (includin the indent) at the second paragraph of the verse.
* ```GLOk.HerrodTheGreat=2``` Triggers before any content (includin the indent) at the second paragraph of the definition.
* ```ms:zif=2``` Triggers the second paragraph after ```\zif |file="wombats"\*```, if this is in introductory matter or 
after the glossary section, or other book in which the verse counter has not been used.
* ```Borrogroves=3``` Triggers the third paragraph after ```\zfigb |id="Borrogroves"\*```, if this is in introductory matter, after 
the glossary, or in another book in which the verse counter has not been used.


# Considerations in the selecting of a trigger point

Triggers that would insert an inline block (e.g. an image or sidebar with a
pgpos of `h`, or an extra paragraph of text block of text), should 
normally use a trigger point that is not in the middle of a piece of text. 
There is no logic to inspect the contents of a trigger block and thus 
perform contents-appropriate ending paragraphs, etc. 

Similarly, block-expecting trigger points, while they will accept text, may not
be *appropriate* for text. In particular, the trigger point `GEN1.1=2` (2nd
paragraph of that verse) occurs *before* the space that indents the paragraph,
not after it.  This is correct for images, but confusing for words. Inserting a
word there will go in an unindented position, and the indent will occur after
any inserted material. 





