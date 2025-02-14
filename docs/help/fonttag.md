# Font tags
## Why this file?
This file exists because sometimes  the user is expected to understand font tags, and they can be a bit cryptic.
For example, the error message:
```
Font \font<zfooterR-12.0+h>="Wombats Literacy Compact" at 
11.00006pt not loadable: Metric (TFM) file or installed font not found.
```
Errors like this might crop up if you're using someone else's project in a diglot, for instance.  So, the "top-level" bug is that computer can't find a font. Perhaps you just need to install it, but maybe you need to change the font to one that's actually available. In order to do that, you possibly have to understand the tag for the requested font, so you know which style(s) to look at.

## Worked examples of font tag decoding 
###`font<zfooterR-12.0+h>`
* `zfooterR`  The character font is `zfooter`, and the `R` means this is the secondary text version of it (in a diglot). `zfooter` which is an automatically-applied style in use when typesetting the running footer. 
* `-12` Fontsize is the same as body text.
* `+h` The paragraph is in the header.

 For technical reasons the footer is normally  generated before the header, and indeed most projects don't define any special formatting for the footer.
Moreover, in some projects, the header and footer are generated before any normal body text is typeset, thus if there's a problem with the font designated for `\Regular` this may be the first occurrence of it.  **Recommended checking sequence**:
 
1.  the basic font choices in the secondary project. 
2. Styling for `\h` in the secondary project
3. Styling for `\zfooter` in the secondary project.

###`font<id:GLO|k-12.0+p>` 
* `id:GLO|`  The style only applies in book GLO
*  `k` The character style is `\k`, and as there's no `L` or `R` or anything else at the end,  it's in a monoglot.
* `-12`  Fontsize is normal for paragraph text (12 font units).
* `+p` The character style above occurred in the context of a `\p` paragraph (in the glossary).

If there's a problem reported with that style, then the **recommended checking sequence** is:

1.  Styling for `id:GLO|k`
2.  Styling for `\k`
3. Styling for `id:GLO|p`
4. Styling for `\p` 


## Font tag syntax

The font tag is the bit inside the angle brackets of `font<` ... `>` and it should uniquely specify the situation in which the font is being used. 
The syntax is:

 [`id_prefix` ] [`category_prefix`] [`milestone_prefix`] style [`side`] `-` `fontsize` [ `context`]

*  id_prefix: `id:` `Book_Code` `|`
    * Book_Code: [A-Z]{3} *(three letter book code, e.g. GEN)*
* category_prefix: `cat:`  [A-Za-z0-9]\*  `|` *(currently active category)*
* milestone_prefix: `ms:` [A-Za-z0-9]\* `|`  *(currently active milestone(s))*
* side: [LRABCDEF] | *(in a diglot/polyglot) 
* context: `+` style [`context`] 
 
Context is normally the paragraph style in which a character style is found. In the case of a nested character style, the context will also include all intermediate character styles.

## Monoglot examples
|USFM|Font tag|Notes
|---------|-------------|---------
|`\p text`| `font<p-12.0>`| Paragraph styles have no context.
|`\p ... \nd text\nd*`  | `font<nd-12.0+p>` |  If `\nd` does not affect the font size.
|`\c 10` | `font<c-34.03125>` | Calculated font sizes are rarely whole numbers
| `\p .... \nd text\nd*` |  `font<nd-10.8+p>` | If `\nd` uses \FontScale 0.9
|`\s1 ... \nd text\nd*`  | `font<nd-14.0+s1>` | Note the different context
|`\p \qt ... \+nd text\+nd*`| `font<nd-12+qt+p>` | When context is stacked, the inner-most style comes first. 

## Diglot examples
|USFM|Font tag|Notes
|---------|-------------|---------
`\p text` | `font<pL-12.0>` | Primary  text
 `\p ... \nd text\nd*`   | `font<ndL-12.0+p>`  |Primary text, if `\nd` does not affect the font size.
 `\p .... \nd text\nd*` | `font<ndR-10.8+p>`  | Secondary text, if the stylesheet entry for `\nd` uses `\FontScale 0.9` or `\FontSize 10.8`