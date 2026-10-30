## What this tab is for

The **Fonts+Script** tab controls *how the letters look* and *how the writing system behaves*: the fonts, the script (writing system), the writing direction, hyphenation and spacing.

Come here when you start a new publication, when some characters print as empty boxes, when your language uses a non-Latin script (for example Arabic, Devanagari, Myanmar, Thai or Chinese), or when you need to hyphenate long words.

Some words used in this chapter:

* **Font** – a set of letter shapes, for example *Charis SIL* or *Gentium Plus*.
* **Typeface** (or face) – one style of a font: Regular, Bold, Italic or Bold Italic.
* **Script** – a writing system, for example Latin, Arabic, Devanagari, Myanmar or Han (Chinese).
* **Glyph** – the shape the font draws for a character.
* **Font feature** – an option built into a font, for example a different shape for one letter, or different digits.
* **Tofu** – the empty box ☐ printed when the font has no shape for a character.
* **Hyphenation** – breaking a long word at the end of a line and continuing it on the next line.
* **pt (point)** – a small unit used for type. 1 pt is about 0.35 mm.

If the whole tab is greyed out, **Lock UI Layout Settings** is ticked on the **Advanced** tab (see the **Layout tab** chapter).

## Font Configuration

PTXprint uses four fonts for the main text: **Regular**, **Bold**, **Italic** and **Bold Italic**. Each has a **Select Font...** button that shows the font now in use.

* Choose the **Regular** font first. Each time you click **OK** in the **Pick a Font** dialog for **Regular**, PTXprint fills in **Bold**, **Italic** and **Bold Italic** from the same family, with the same features and options. So choose a different bold or italic font only *after* you have finished with Regular.
* If the family has no bold or italic typeface, PTXprint *fakes* it (makes the letters thicker or slanted). The button then shows the style in brackets, for example *(bold)*. Faked styles are usable, but a real typeface looks better.
* If your Paratext project's language settings name font features for this font, PTXprint uses them when you choose it (unless you have already set features).
* Only the **Regular** button is shown in the **Mini** view. The other three are shown from the **Basic** view upwards.

Click **Refresh Font List** if a newly installed font is not in the list.

**Enable Colored Text (as Specified in Stylesheet)** prints text in colour where a style asks for it (for example red letters for the words of Jesus). If it is not ticked, all text is black.

**Script for Numbers** is a link that opens the **Pick a Font** dialog with **Digit mapping** highlighted (see below).

## Pick a Font (and Typeface) dialog

This dialog opens when you click any **Select Font...** button.

1. Type part of the font name in the search box.
2. Click a font in the list. Fonts shown in **bold** have all four typefaces.
3. Choose the **Typeface**.
4. Change other options if needed, then click **OK**.

If a font is missing from the list, it may not be installed for all users. Install it, then click **Refresh Font List** on the **Fonts+Script** tab.

The other options are:

* **Fake Bold/Italic** – make bold and/or italic from the regular typeface. **Embolden** sets how much thicker; **Slant** sets how much the letters lean (0.15 is a normal italic slant; negative leans the other way).
* **Stretch** – make all letters wider (above 1.00) or narrower (below 1.00). 0.95 makes text 5% narrower, so more fits on a line. Use small changes only; the letter shapes become distorted.
* **Graphite Rendering** – use SIL's Graphite technology. Tick it only for fonts made for Graphite that need it (the font's documentation says so). Ticking or unticking it clears the font features.
* **Contextual Spaces** – tick only if the font itself changes the width of spaces depending on the letters around them. When ticked for the Regular font, **Between Letters** spacing is not used.
* **Font features** (text box) and **Select Features...** – turn special options in the font on or off.
* **Digit mapping** – print numbers in another script's digits.

### Digit mapping (numbers in your own script)

Many scripts have their own digits, for example Arabic-Indic ٠١٢٣, Devanagari ०१२३, Myanmar ၀၁၂၃ or Thai ๐๑๒๓. If your text uses the Western digits 0–9 but you want your script's digits, choose your script in **Digit mapping**. PTXprint then changes the digits when it prints, for numbers in that font (for example chapter and verse numbers).

* Check that your font has these digits. If not, you will see empty boxes.
* When you change **Text Script**, PTXprint also tries to choose the matching digit mapping. Check it.
* If your text already contains your script's digits, leave **Digit mapping** on **Default**.

### Select Font Features dialog

**Select Features...** lists the selected font's features as tick boxes and drop-down lists. Hover over a feature name to see a short description (when the font gives one).

* **Language** – choose a language the font knows. Some fonts use different letter shapes for different languages. Choosing one sets the features to that language's defaults.
* With **Graphite Rendering** ticked you see the font's Graphite features; otherwise its OpenType features.
* **OK** writes your choices into the font features text box, for example `language=ur, cv12=1`. Only features you changed from the default are written.

Choosing a different font in the list clears the font features.

## Use Fallback Font

Some fonts do not contain every character in your text, for example special quotation marks or the glossary markers. These print as empty boxes (tofu). A *fallback font* is a second font used only for those characters.

1. Tick **Use Fallback Font**.
2. Click **Find Missing Characters**. PTXprint checks the books selected on the **Basic** tab against the Regular font and lists the missing characters. Select as many books as possible first. If nothing is missing, PTXprint tells you and unticks **Use Fallback Font**.
3. Click **Select Font...** next to the list and choose a font that has these characters. If the label turns **red**, that font lacks some of them too; choose another.

You can add characters to the list by hand, separated by spaces. You can type a character code as `\u` plus four hex digits, for example `\u2E24`. Straight and curly quotation marks (‘ ’ “ ”) and `*`, `#` and `%` are ignored by the fallback font.

These settings are shown in the **Regular** and **Full** views.

## Writing System

This area tells PTXprint how your script works. It is very important for non-Latin scripts.

### Text Flow Direction

* **Left-to-Right** – for example Latin, Cyrillic, Devanagari, Ethiopic, Thai and Myanmar.
* **Right-to-Left** – for example Arabic, Hebrew, Syriac and Thaana. This also ticks **RTL Book Binding**.
* **Top-to-Bottom (and Left-to-Right)** – vertical text, with the lines going from left to right.

### RTL Book Binding

A right-to-left book is bound on the right and opens from the "back" (as seen by a left-to-right reader). Tick **RTL Book Binding** so that the binding gutter, the page order in PDF viewers and the cover are correct for such a book.

### Text Script

**Text Script** tells the font which script rules to use. These rules join letters (for example in Arabic), place vowel marks and other marks, and reorder letters where needed (for example in Indic scripts).

* If **Text Script** is **Default** when a project is opened, PTXprint tries to detect the script. Check that it is right.
* The right script also switches on extra processing that PTXprint has for some scripts (see below).
* For most Latin-script languages, leave it on **Default** or **Latin**.

### Additional Script Settings...

This button opens a small dialog with extra options for some scripts:

* **Myanmar (Burmese)** – **Syllable line breaking**: break lines between syllables, not only at spaces.
* **Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya** – **Syllable line breaking**: break long words between syllables. **Show Hyphen**: print a hyphen where a word is broken (if not ticked, the break is invisible).
* **Arabic** – **First verse on left**: how verse references are written.
* **Han (Simplified)** and **Han (Traditional)** – **Enabling horizontal gridding**: align chapter numbers with the character grid and remove spaces before verses. **Automatic halfwidth punctuation pairs**: two punctuation marks together share the width of one full character.

### Scripts that do not use spaces between words

Some scripts (for example Thai, Lao, Khmer, Myanmar, Tai Tham, New Tai Lue, Chinese and Japanese) do not put spaces between words. PTXprint must know where it may break a line. There are two ways:

* **Mark break points in the text with "/".** For Thai, Lao, Myanmar, Tai Tham (Lanna) and New Tai Lue, when **Text Script** is set to that script, each `/` becomes an invisible break point. The `/` is not printed.
* **Use a line-break dictionary.** Tick **Specify Line Break Locale** and type a code: `th` (Thai), `km` (Khmer), `my` (Myanmar), `zh` (Chinese), `ja` (Japanese), `ko` (Korean), or `gr` for the line-breaking rules inside a Graphite font. Choosing a Han, Japanese or Korean script in **Text Script** fills this in for you.

These options are shown in the **Regular** and **Full** views.

## Hyphenation

PTXprint can hyphenate using your Paratext project's hyphenation list. In Paratext, the Wordlist tool suggests where words can be broken, and you approve the suggestions. PTXprint turns that list into one it can use.

1. Click **Create List...**. The **Create List** dialog opens.
2. Choose the options (see below) and click **OK**. A message says how many words were used.
3. Tick **Hyphenate**.
4. Click **Print**.

Create the list again only when the Paratext hyphenation list changes.

Ticking **Hyphenate** unticks **Between Letters** in **Spacing Adjustments**, because letter spacing stops hyphenation from working well. The status bar tells you this.

**Omit '-'Hyphen** makes the hyphen invisible, for scripts that break words but show no hyphen.

**Make Hyphens Non-Breaking** stops lines breaking at hyphens already in the text. Create the hyphenation list again after you change this.

### Create List dialog (hyphenation)

* **Only Use Approved Hyphenation Words** (ticked by default) – use only words whose break points you approved in Paratext. Untick it to include Paratext's unchecked guesses. If the list comes out empty, try unticking this.
* **Limit Hyphenation List to Words Found in** – use only words in the books you are printing (listed beside it). Use it when the full list is too long.
* **Add Syllable-Based Hyphenated Words** – only for scripts where **Syllable line breaking** is ticked in **Additional Script Settings...**. Adds break points for more words using the syllable rules.
* **Advanced** – limits on which words are added: **Minimum affix**, **Minimum length** and **Min non-hyphen**.

## Spacing Adjustments

When text is justified (both edges straight), PTXprint stretches or shrinks the spaces in each line. This area controls how much.

* **Between Words** – the smallest (**Min/Shrink**) and largest (**Max/Stretch**) space between words, as a percentage of a normal space. A lower minimum fits more words on a line. A higher maximum lets lines stretch more. Too low makes words hard to separate; too high leaves big gaps ("rivers" of white space).
* **Between Letters** – also lets PTXprint add or remove a very small amount of space between letters, as a percentage of the font size. Keep the numbers small. Use it only when really needed: it can make text look uneven and stops hyphenation from working well.

**Between Letters** is greyed out when **Interlinear & Code** is ticked on the **Advanced** tab. It is not used when **Contextual Spaces** is ticked for the Regular font, and it is unticked when you tick **Hyphenate**.

These settings are shown in the **Regular** and **Full** views.

## Add Tatweel (kashida) Rules dialog

In Arabic script, a *tatweel* (also *kashida*, the character ـ) is a joining stroke that makes a word longer, to make lines look better or to fill a line. This dialog writes a *change rule* that adds tatweels to one word at one verse. The rule goes into the project's changes file (changes.txt), which PTXprint applies every time it prints.

To open it (advanced): on the **View+Edit** tab, open the changes file. In the **Code Snippets** area at the side, click **Arabic**, then **Add Tatweels**.

1. In Paratext (or anywhere), copy the word or short phrase to lengthen (up to 60 characters). The dialog fills in **Word / Phrase** from the clipboard. On Windows, it also fills in **Reference** from the current Paratext reference.
2. Check the **Reference**.
3. Set **Tatweels to insert**.
4. Click in **Word / Phrase** where the tatweels should go and press **Ctrl+`** (Ctrl and the grave-accent key). Repeat for other places.
5. Check the rule in **The rule to be added to Changes.txt**. It looks like `at REF 'original' > 'new'`.
6. Click **Insert Rule**. The rule is added at the cursor in the file open on the **View+Edit** tab.
7. Save the file and click **Print**.

## Common tasks

### How do I change the main font?

1. On the **Fonts+Script** tab, **Font Configuration**, click **Select Font...** next to **Regular**.
2. Type part of the font name, click the font, and click **OK**.
3. Check the **Bold**, **Italic** and **Bold Italic** buttons. A style in brackets will be faked.
4. Click **Print**.

### How do I get rid of empty boxes (tofu) in the printed text?

1. Select all the books on the **Basic** tab.
2. Follow the steps in **Use Fallback Font** above.
3. Click **Print**.

### How do I print numbers in my own script's digits?

1. On the **Fonts+Script** tab, click the **Script for Numbers** link (or **Select Font...** for **Regular**).
2. Choose your script in **Digit mapping**.
3. Click **OK**, then **Print**. Check that the font has those digits.

### How do I set up a right-to-left script (for example Arabic or Hebrew)?

1. On the **Fonts+Script** tab, choose a font made for your script.
2. In **Writing System**, set **Text Flow Direction** to **Right-to-Left**. **RTL Book Binding** is ticked for you.
3. Set **Text Script** to your script (for example **Arabic** or **Hebrew**).
4. If your font needs Graphite (for example some Nastaliq fonts), open **Select Font...**, tick **Graphite Rendering** and click **OK**.
5. Click **Print**.

### How do I set up a script that has no spaces between words?

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. If your text marks word breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue), nothing more is needed.
3. Otherwise, tick **Specify Line Break Locale** and type the code (for example `th`, `km`, `my`, `zh`, `ja` or `ko`).
4. For Myanmar or Indic scripts, consider **Syllable line breaking** in **Additional Script Settings...**.
5. Click **Print**.

### How do I turn on hyphenation?

1. Make sure hyphenation points have been approved in the Paratext Wordlist.
2. Follow the steps in **Hyphenation** above.

### How do I choose a different form of a letter that the font offers?

1. Click **Select Font...** for **Regular**, then **Select Features...**.
2. Choose your language in **Language** (if listed), then tick or choose the feature.
3. Click **OK** in both dialogs, then **Print**. PTXprint copies the Regular font's features to the Bold, Italic and Bold Italic fonts.

### How do I fit more text on each line?

1. In **Spacing Adjustments**, make **Min/Shrink** (Between Words) a little smaller.
2. Or, in the **Pick a Font** dialog, set **Stretch** slightly below 1.00 (for example 0.97).
3. Click **Print** and check that the text is still easy to read.

## Common problems

### The whole Fonts+Script tab is greyed out

**Cause:** **Lock UI Layout Settings** is ticked on the **Advanced** tab.

**What to do:** Change to the **Full** view. On the **Advanced** tab, **Main** tab, **General** area, untick **Lock UI Layout Settings**.

### Some characters print as empty boxes

**Cause:** The Regular font does not contain those characters.

**What to do:** Use **Use Fallback Font** and **Find Missing Characters**, or choose a Regular font that supports your whole character set.

### My font is not in the list

**Cause:** The font is not installed, was installed only for one user, or the list has not been refreshed.

**What to do:** Install the font for all users, then click **Refresh Font List**.

### Bold or italic looks thick, blurred or slanted wrongly

**Cause:** The font has no real bold or italic, so PTXprint fakes it (the style is in brackets on the button).

**What to do:** Choose a family with real bold and italic typefaces, or change **Embolden** and **Slant** in the **Pick a Font** dialog.

### Letters do not join, or marks are in the wrong place

**Cause:** **Text Script** may be wrong, or the font needs Graphite rendering.

**What to do:** Set **Text Script** to your script. For a Graphite font, tick **Graphite Rendering** in the **Pick a Font** dialog.

### Additional Script Settings... is greyed out

**Cause:** The script in **Text Script** has no extra options.

### Long lines do not break in Thai, Khmer, Myanmar, Chinese and similar scripts

**Cause:** PTXprint does not know where it may break the line.

**What to do:** Set **Text Script**, and either mark breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue) or tick **Specify Line Break Locale** and type the language code.

### Hyphenation does not work

* No list was created. Click **Create List...** first.
* The list is empty because no words are approved in Paratext. Untick **Only Use Approved Hyphenation Words** and create the list again, or approve words in Paratext.
* **Between Letters** is ticked. Untick it.
* **Hyphenate** is not ticked.

### Between Letters is greyed out

**Cause:** **Interlinear & Code** is ticked on the **Advanced** tab. The two cannot be used together.

### Font features I set have disappeared

**Cause:** Choosing another font, or ticking or unticking **Graphite Rendering**, clears the features.

**What to do:** Set the features again after choosing the font and the Graphite option.

### Numbers print as boxes after choosing a digit mapping

**Cause:** The font does not have the digits for that script.

**What to do:** Choose a font that has these digits, or set **Digit mapping** back to **Default**.

### Text is printed in black even though styles have colours

**Cause:** **Enable Colored Text (as Specified in Stylesheet)** is not ticked.

## Control notes

### @btn_gnr8pl_ok1
Creates the list and shows how many words were used. Read the message: it tells you if the list was empty or had to be shortened.

### @btn_gnr8pl_cancel1
Closes the dialog without creating a list.

### @c_addSyllableBasedHyphens
Syllable line breaking is available for Myanmar and some Indic scripts. Use this when Paratext's list covers only some words.

### @c_hyphenLimitBooks
The books are listed beside this option.

### @c_hyphenApprovedWords
The safe choice. If you untick it, check the printed result carefully.

### @s_hyphMinprefix
Stops very short pieces (one or two letters) being left at the end of a line or carried to the next. The default of 3 is usually good.

### @s_hyphMinWord
Only words longer than this are added. Short words rarely need to be broken.

### @s_hyphMinBlock
PTXprint counts long words that have no break points, but at present this number does not change the list created. Leave it at the default.

### @btn_tatweel_insertRule
Inserts the rule at the cursor in the file open on the **View+Edit** tab. Make sure that file is the changes file, and save it afterwards.

### @btn_tatweel_close
Closes the dialog and stops it watching the clipboard.

### @t_tatweelRef
For example `GEN 1:1`. On Windows it updates each time you copy a new word. The rule only changes the word at this reference.

### @t_tatweelText
The "before" part of the rule is the text you copied, so copy the exact word from the text; do not just type it here.

### @s_tatweelLength
Applies each time you press **Ctrl+`**. Start with 1 or 2 and check the printed result.

### @t_tatweelPreview
Form: `at REF 'original' > 'new'`. Check it before you click **Insert Rule**.

### @btn_font_ok
Uses the selected font, typeface and options for the button you clicked.

### @btn_font_cancel
Closes the dialog without changing the font.

### @tv_fontFamily
Choosing a different font clears the font features.

### @fcb_fontFaces
Normally **Regular** for the Regular button, **Bold** for the Bold button, and so on. Some fonts also offer faces such as Light or Semibold.

### @t_fontSearch
Part of the name is enough.

### @c_fontFake
Use it only when the font has no real bold or italic. PTXprint also fakes missing styles automatically; the font button then shows the style in brackets.

### @s_fontExtend
Small changes (0.95–1.05) can help fit text; large changes distort the letters. A value set for the Regular font is copied to Bold, Italic and Bold Italic.

### @t_fontFeatures
May also contain `language=xx`. The easy way to fill it is **Select Features...**. It is cleared when you choose a different font or change **Graphite Rendering**.

### @c_fontCtxtSpaces
Tick only if the font's documentation says so. When ticked for the Regular font, PTXprint switches off **Between Letters** spacing.

### @c_fontGraphite
Replaces the normal (OpenType) rendering. Some complex-script fonts work best, or only, with Graphite. When ticked, **Select Features...** shows Graphite features.

### @btn_fontFeatures
Works on the font selected in the list. Shows Graphite features if **Graphite Rendering** is ticked, otherwise OpenType features.

### @fcb_fontdigits
For example Arabic-Indic, Devanagari, Myanmar or Thai. Use it when the text contains 0–9 but the publication should show your script's digits. Leave it on **Default** if the text already has the right digits. The list holds many more scripts than the four shown above.

### @s_fontBold
Larger numbers give thicker letters. Check the result in print: too much makes letters fill in.

### @s_fontItalic
A negative value leans the letters the other way. 0 means no slant.

### @btn_feats_ok
Writes the changed features into the font features box of the **Pick a Font** dialog. Only features that differ from the default are written.

### @btn_feats_cancel
Closes the dialog without changing the features.

### @fcb_featsLangs
Choosing a language also sets the features to that language's defaults.

### @bl_fontR
Choose it first. Each time you click **OK** for it, PTXprint fills in Bold, Italic and Bold Italic from the same family with the same features, replacing any you chose by hand. All styles that do not name their own font use this font. Font features listed in your Paratext language settings are used too.

### @bl_fontB
Filled in automatically when you choose the Regular font.

### @bl_fontI
Filled in automatically when you choose the Regular font.

### @bl_fontBI
Filled in automatically when you choose the Regular font.

### @btn_refreshFonts
Reloads the font list from the computer.

### @c_colorfonts
Also covers coloured headings or any other colour set in the styles. Check with your printer whether colour printing is possible and what it costs.

### @lb_NumberScript
Opens the dialog for the Regular font.

### @btn_findMissingChars
Digits and markers are not checked. If characters are missing, **Use Fallback Font** is ticked; if not, PTXprint says a fallback font is not needed and unticks it. Hover over the list afterwards to see the character codes.

### @bl_fontExtraR
It must be a different font from the Regular font.

### @t_missingChars
Codes can be typed like `\u2E24`. Quotation marks (‘ ’ “ ”) and `*`, `#`, `%` are ignored.

### @c_useFallbackFont
Then use **Find Missing Characters** and choose a fallback font. **Find Missing Characters** ticks or unticks this automatically.

### @c_hyphenate
Create the list first. Ticking it unticks **Between Letters** spacing. When unticked, PTXprint does not hyphenate at all.

### @btn_generateHyphenationList
Opens the **Create List** dialog. Do this again when the Paratext list changes.

### @c_omitHyphen
Makes the hyphen at a line break invisible.

### @c_nonBreakingHyphens
Create the hyphenation list again after changing this, because the list is made with the chosen kind of hyphen.

### @c_spacing
Uses the **Min/Shrink** and **Max/Stretch** values. When unticked, standard values are used.

### @c_letterSpacing
Use it only when needed. PTXprint unticks it when you tick **Hyphenate**.

### @s_minSpace
Lower values fit more text on a line, but words may become hard to tell apart. About 50–80 is common.

### @s_maxSpace
Higher values let lines stretch more, but can leave big gaps. About 150–200 is common.

### @s_letterShrink
Keep it small (a few percent at most).

### @s_letterStretch
Keep it small.

### @fcb_textDirection
**Right-to-Left** also ticks **RTL Book Binding**. Changing this changes the whole layout.

### @fcb_script
For example, it makes `/` a word-break mark in Thai, Lao, Myanmar, Tai Tham and New Tai Lue. Changing it may also change **Digit mapping** and **Specify Line Break Locale**.

### @btn_scrsettings
Only active for scripts that have options: Myanmar, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, Arabic, and Han (Simplified and Traditional).

### @c_linebreakon
For scripts with no spaces between words. Ticked automatically when you choose a Han, Japanese or Korean script.

### @t_linebreaklocale
`gr` uses the line-breaking rules built into a Graphite font.

### @c_RTLbookBinding
Affects where the binding gutter goes, how PDF viewers show the pages, and the cover. Ticked automatically when you choose **Right-to-Left** text direction.
