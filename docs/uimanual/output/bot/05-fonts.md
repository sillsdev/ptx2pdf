# 6. Fonts+Script tab

## 6.1 What this tab is for

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

## 6.2 Font Configuration

PTXprint uses four fonts for the main text: **Regular**, **Bold**, **Italic** and **Bold Italic**. Each has a **Select Font...** button that shows the font now in use.

* Choose the **Regular** font first. Each time you click **OK** in the **Pick a Font** dialog for **Regular**, PTXprint fills in **Bold**, **Italic** and **Bold Italic** from the same family, with the same features and options. So choose a different bold or italic font only *after* you have finished with Regular.
* If the family has no bold or italic typeface, PTXprint *fakes* it (makes the letters thicker or slanted). The button then shows the style in brackets, for example *(bold)*. Faked styles are usable, but a real typeface looks better.
* If your Paratext project's language settings name font features for this font, PTXprint uses them when you choose it (unless you have already set features).
* Only the **Regular** button is shown in the **Mini** view. The other three are shown from the **Basic** view upwards.

Click **Refresh Font List** if a newly installed font is not in the list.

**Enable Colored Text (as Specified in Stylesheet)** prints text in colour where a style asks for it (for example red letters for the words of Jesus). If it is not ticked, all text is black.

**Script for Numbers** is a link that opens the **Pick a Font** dialog with **Digit mapping** highlighted (see below).

## 6.3 Pick a Font (and Typeface) dialog

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

## 6.4 Use Fallback Font

Some fonts do not contain every character in your text, for example special quotation marks or the glossary markers. These print as empty boxes (tofu). A *fallback font* is a second font used only for those characters.

1. Tick **Use Fallback Font**.
2. Click **Find Missing Characters**. PTXprint checks the books selected on the **Basic** tab against the Regular font and lists the missing characters. Select as many books as possible first. If nothing is missing, PTXprint tells you and unticks **Use Fallback Font**.
3. Click **Select Font...** next to the list and choose a font that has these characters. If the label turns **red**, that font lacks some of them too; choose another.

You can add characters to the list by hand, separated by spaces. You can type a character code as `\u` plus four hex digits, for example `\u2E24`. Straight and curly quotation marks (‘ ’ “ ”) and `*`, `#` and `%` are ignored by the fallback font.

These settings are shown in the **Regular** and **Full** views.

## 6.5 Writing System

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

## 6.6 Hyphenation

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

## 6.7 Spacing Adjustments

When text is justified (both edges straight), PTXprint stretches or shrinks the spaces in each line. This area controls how much.

* **Between Words** – the smallest (**Min/Shrink**) and largest (**Max/Stretch**) space between words, as a percentage of a normal space. A lower minimum fits more words on a line. A higher maximum lets lines stretch more. Too low makes words hard to separate; too high leaves big gaps ("rivers" of white space).
* **Between Letters** – also lets PTXprint add or remove a very small amount of space between letters, as a percentage of the font size. Keep the numbers small. Use it only when really needed: it can make text look uneven and stops hyphenation from working well.

**Between Letters** is greyed out when **Interlinear & Code** is ticked on the **Advanced** tab. It is not used when **Contextual Spaces** is ticked for the Regular font, and it is unticked when you tick **Hyphenate**.

These settings are shown in the **Regular** and **Full** views.

## 6.8 Add Tatweel (kashida) Rules dialog

In Arabic script, a *tatweel* (also *kashida*, the character ـ) is a joining stroke that makes a word longer, to make lines look better or to fill a line. This dialog writes a *change rule* that adds tatweels to one word at one verse. The rule goes into the project's changes file (changes.txt), which PTXprint applies every time it prints.

To open it (advanced): on the **View+Edit** tab, open the changes file. In the **Code Snippets** area at the side, click **Arabic**, then **Add Tatweels**.

1. In Paratext (or anywhere), copy the word or short phrase to lengthen (up to 60 characters). The dialog fills in **Word / Phrase** from the clipboard. On Windows, it also fills in **Reference** from the current Paratext reference.
2. Check the **Reference**.
3. Set **Tatweels to insert**.
4. Click in **Word / Phrase** where the tatweels should go and press **Ctrl+`** (Ctrl and the grave-accent key). Repeat for other places.
5. Check the rule in **The rule to be added to Changes.txt**. It looks like `at REF 'original' > 'new'`.
6. Click **Insert Rule**. The rule is added at the cursor in the file open on the **View+Edit** tab.
7. Save the file and click **Print**.

## 6.9 Common tasks

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

## 6.10 Common problems

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

## 6.11 Settings reference

### Create List (dialog)

#### OK

Button · Regular+ · `btn_gnr8pl_ok1`

Creates the list and shows how many words were used. Read the message: it tells you if the list was empty or had to be shortened.

#### Cancel

Button · Regular+ · `btn_gnr8pl_cancel1`

Closes the dialog without creating a list.

#### When Creating Hyphenation List

##### Add Syllable-Based Hyphenated Words

Checkbox, off · Regular+ · `c_addSyllableBasedHyphens` · cfg `paragraph/ifsylhyphens`  
Also: Append syllable-based hyphenated words to hyphen list

> This advanced hybrid option is only available if Syllable Line Breaking has been enabled under Additional Script Settings for Complex Scripts.
>
> If enabled, it will use Syllable Line Breaking to hyphenate words from the books selected so that a combination of manually-marked hyphenation along with automated hyphenation is possible.

Syllable line breaking is available for Myanmar and some Indic scripts. Use this when Paratext's list covers only some words.

##### Limit Hyphenation List to Words Found in

Checkbox, off · Regular+ · `c_hyphenLimitBooks` · cfg `paragraph/ifhyphlimitbks`  
Also: Limit hyphenation list to only include words in active books

> Normally ALL hyphenated words from ALL books are included in PTXprint's hyphenated wordlist.
>
> However, if the list of hyphenated words is too long (greater than 63929 words) then you can prioritize which words to include by enabling this option to only use words from the books being printed.
>
> Note that if there are too many words in the Paratext hyphenation file, PTXprint will automatically prioritize the list created for XeTeX based on frequency.

The books are listed beside this option.

##### Only Use Approved Hyphenation Words

Checkbox, on · Regular+ · `c_hyphenApprovedWords` · cfg `paragraph/ifhyphapproved`  
Also: Only use words where hyphenation points have been approved in Paratext

> The Paratext WordList tool guesses hyphenation points based on syllable structure and patterns in the language.
>
> However, it expects the user to (i) check and, if appropriate, (ii) approve the suggested hyphenation points (by clicking the check mark making it appear green).
>
> Normally only the approved hyphenated words will be used when creating the hyphenation list for PTXprint/TeX to use.
>
> However, if you wish to include ALL words (regardless of their approval status) then disable this option.

The safe choice. If you untick it, check the printed result carefully.

##### Advanced

###### Minimum affix

Number · Regular+ · `s_hyphMinprefix`  
Values: 1–10 (default 3)

> Do not add any words to the hyphenation list that include an optional hyphen less than this number of characters at the beginning or end of the word.

Stops very short pieces (one or two letters) being left at the end of a line or carried to the next. The default of 3 is usually good.

###### Minimum length

Number · Regular+ · `s_hyphMinWord`  
Values: 3–50 (default 7)

> The minimum word length (including optional hyphens) that will be added to the hyphenation list.

Only words longer than this are added. Short words rarely need to be broken.

###### Min non-hyphen

Number · Regular+ · `s_hyphMinBlock`  
Values: 1–50 (default 9)

> Minimum word length for a word to block hyphenation.

PTXprint counts long words that have no break points, but at present this number does not change the list created. Leave it at the default.

### Add Tatweel (kashida) Rules (dialog)

#### Insert Rule

Button · Regular+ · `btn_tatweel_insertRule`

Inserts the rule at the cursor in the file open on the **View+Edit** tab. Make sure that file is the changes file, and save it afterwards.

#### Close

Button · Regular+ · `btn_tatweel_close`

Closes the dialog and stops it watching the clipboard.

#### Reference – Tatweel Dialog: Enter reference

Text box · Regular+ · `t_tatweelRef`

> Enter the verse reference where the word is located.
>
> (Note that the reference is automatically updated from the current Paratext reference.)

For example `GEN 1:1`. On Windows it updates each time you copy a new word. The rule only changes the word at this reference.

#### Word / Phrase – Tatweel Dialog: Enter word or phrase to be lengthened

Text box · Regular+ · `t_tatweelText`

> Enter the word to be lengthened and place the cursor at the location and use shortcut Ctrl-` (Ctrl-grave) to insert Tatweels. Repeat at other words and/or locations.
>
> (Note that this box is automatically updated from the clipboard if the word/phrase is 60 characters or less).

The "before" part of the rule is the text you copied, so copy the exact word from the text; do not just type it here.

#### Tatweels to insert – Tatweel Dialog: Number of Tatweels to insert

Number · Regular+ · `s_tatweelLength`  
Values: 1–20

> How many Tatweels should be inserted at the current cursor location?

Applies each time you press **Ctrl+`**. Start with 1 or 2 and check the printed result.

#### The rule to be added to Changes.txt

Text box · Regular+ · `t_tatweelPreview`

> The rule to be added to Changes.txt

Form: `at REF 'original' > 'new'`. Check it before you click **Insert Rule**.

### Pick a Font (and Typeface) (dialog)

#### OK

Button · Regular+ · `btn_font_ok`

Uses the selected font, typeface and options for the button you clicked.

#### Cancel

Button · Regular+ · `btn_font_cancel`

Closes the dialog without changing the font.

#### Choose a font from the installed fonts. Fonts shown in BOLD ...

Table · Mini+ · `tv_fontFamily`

> Choose a font from the installed fonts. Fonts shown in BOLD have all 4 typefaces.
>
> If you cannot locate the desired font in this list, then it is quite likely that it has not been installed "For all Users" in the Windows system.

Choosing a different font clears the font features.

#### Typeface – Font Selection Dialog: Typeface

Drop-down · Mini+ · `fcb_fontFaces`  
Choices: Regular | Bold | Italic | Bold Italic

> Fonts which have all 4 typefaces (regular, bold, italic, and bold-italic) are shown in BOLD in the list above.
>
> If you cannot locate the desired font in this list, then it is quite likely that it has not been installed "For all Users" in the Windows system.

Normally **Regular** for the Regular button, **Bold** for the Bold button, and so on. Some fonts also offer faces such as Light or Semibold.

#### Font Selection Dialog: Find a font

Search box · Mini+ · `t_fontSearch`

> Type the start of a font name to jump to it in the list.

Part of the name is enough.

#### Fake Bold/Italic

Checkbox, off · Basic+ · `c_fontFake`  
Also: Font Selection Dialog: Fake bold or italic typeface

> If the font you are using doesn't have multiple typefaces (such as Bold, Italic and Bold-Italic) then you can "fake" these by adding boldness and/or slant to the regular typeface.

Use it only when the font has no real bold or italic. PTXprint also fakes missing styles automatically; the font button then shows the style in brackets.

#### Stretch – Font Selection Dialog: Stretch (or shrink) font setting

Number · Regular+ · `s_fontExtend`  
Values: 0.5–2 (default 1)

> The shapes of the characters can be stretched (larger) or condensed (smaller) to occupy more horizontal space, or less (shrink text).  
> 1.00 = 100% = normal  
> 0.95 =   95% = shrink text  
> 1.05 = 105% = expand text

Small changes (0.95–1.05) can help fit text; large changes distort the letters. A value set for the Regular font is copied to Bold, Italic and Bold Italic.

#### Font Selection Dialog: Selected font features

Text box · Regular+ · `t_fontFeatures`

> You can enable/disable any font features for the selected font. For example:  
> smcp=1, cv12=2 Use 'Select Features...' to choose them from a list.

May also contain `language=xx`. The easy way to fill it is **Select Features...**. It is cleared when you choose a different font or change **Graphite Rendering**.

#### Contextual Spaces

Checkbox, off · Regular+ · `c_fontCtxtSpaces`  
Also: Font Selection Dialog: Use contextual spaces

> Set this option if the font changes the width of spaces depending on the text around them.

Tick only if the font's documentation says so. When ticked for the Regular font, PTXprint switches off **Between Letters** spacing.

#### Graphite Rendering

Checkbox, off · Regular+ · `c_fontGraphite`  
Also: Font Selection Dialog: Use Graphite rendering

> If you require this font to use SIL's Graphite Rendering technology, then enable this.
>
> Changing this clears the font features.

Replaces the normal (OpenType) rendering. Some complex-script fonts work best, or only, with Graphite. When ticked, **Select Features...** shows Graphite features.

#### Select Features...

Button · Regular+ · `btn_fontFeatures`  
Also: Font Selection Dialog: Select font features

> Choose font features (and the language) from a list of those this font supports.

Works on the font selected in the list. Shows Graphite features if **Graphite Rendering** is ticked, otherwise OpenType features.

#### Digit mapping – Font Selection Dialog: Digit (number) script mapping

Drop-down · Regular+ · `fcb_fontdigits`  
Choices: Default | Arabic-Hindi | Arabic-Farsi | Burmese

> All known unicode-encoded number/digit systems are catered for. So if you don't want to use the Latin/Arabic numbers [0-9], you can pick the appropriate script here. (Make sure the font you are using supports these digits too.)

For example Arabic-Indic, Devanagari, Myanmar or Thai. Use it when the text contains 0–9 but the publication should show your script's digits. Leave it on **Default** if the text already has the right digits. The list holds many more scripts than the four shown above.

#### Fake Bold/Italic

##### Embolden – Font Selection Dialog: Fake bold setting

Number · Basic+ · `s_fontBold`  
Needs: “Fake Bold/Italic”

> If the required font doesn't have a BOLD typeface, you can use this setting to create the BOLD effect. (For example, setting Embolden to 1.6 would thicken the Regular typeface making it appear as bold.)

Larger numbers give thicker letters. Check the result in print: too much makes letters fill in.

##### Slant – Font Selection Dialog: Fake italic setting

Number · Basic+ · `s_fontItalic`  
Values: -1–1 (default 0.15) · Needs: “Fake Bold/Italic”

> If the required font does not have an ITALIC typeface, you can use this setting to create the ITALIC effect. (For example, setting Slant to 0.15 would slant the Regular typeface by 15% making it appear as italic.)

A negative value leans the letters the other way. 0 means no slant.

### Select Font Features... (dialog)

#### OK

Button · Regular+ · `btn_feats_ok`

Writes the changed features into the font features box of the **Pick a Font** dialog. Only features that differ from the default are written.

#### Cancel

Button · Regular+ · `btn_feats_cancel`

Closes the dialog without changing the features.

#### Language

Drop-down · Regular+ · `fcb_featsLangs`

> Choose the language the font should use. Some fonts change letter shapes for particular languages.

Choosing a language also sets the features to that language's defaults.

### Fonts+Script

#### Use Fallback Font

Checkbox, off · Regular+ · `c_useFallbackFont` · cfg `paragraph/ifusefallback`  
Greyed out by: “Lock UI Layout Settings”

> This setting is used to prevent "tofu" boxes [] in the printed text. If the primary font is missing any special characters (for example curly quotes), then an alternative "fallback" font can be used to ensure that they are displayed properly.

Then use **Find Missing Characters** and choose a fallback font. **Find Missing Characters** ticks or unticks this automatically.

#### Font Configuration

##### Select Font...

Button · Mini+ · `bl_fontR` · cfg `document/fontregular`  
Also: Select Regular font · Greyed out by: “Lock UI Layout Settings”

> Click to select the main font for the publication. Note that the font chooser dialog also has a number of other options for setting advanced font features and, if needed, Graphite rendering.

Choose it first. Each time you click **OK** for it, PTXprint fills in Bold, Italic and Bold Italic from the same family with the same features, replacing any you chose by hand. All styles that do not name their own font use this font. Font features listed in your Paratext language settings are used too.

##### Select Font...

Button · Basic+ · `bl_fontB` · cfg `document/fontbold`  
Also: Select Bold font · Greyed out by: “Lock UI Layout Settings”

> If you see the style in parentheses (bold) this indicates that PTXprint could not locate the bold style and will fake the style.

Filled in automatically when you choose the Regular font.

##### Select Font...

Button · Basic+ · `bl_fontI` · cfg `document/fontitalic`  
Also: Select Italic font · Greyed out by: “Lock UI Layout Settings”

> If you see the style in parentheses (italic) this indicates that PTXprint could not locate the italic style and will fake the style.

Filled in automatically when you choose the Regular font.

##### Select Font...

Button · Basic+ · `bl_fontBI` · cfg `document/fontbolditalic`  
Also: Select Bold Italic font · Greyed out by: “Lock UI Layout Settings”

> If you see either of the styles in parentheses (bold) or (italic) this indicates that PTXprint could not locate the style and will fake the bold-italic style.

Filled in automatically when you choose the Regular font.

##### Refresh Font List button

Button · Regular+ · `btn_refreshFonts`  
Greyed out by: “Lock UI Layout Settings”

> Refresh Font List:  
> If you have recently installed a font but it doesn't show in the font list, then try clicking this button to refresh the list.
>
> If it still doesn't show up, then try re-installing the font (in Windows, locate the font file, then right-click on it and select "Install For All Users").
>
> And remember to Refresh the Font List again.

Reloads the font list from the computer.

##### Enable Colored Text (as Specified in Stylesheet)

Checkbox, off · Regular+ · `c_colorfonts` · cfg `document/ifcolorfonts`  
Greyed out by: “Lock UI Layout Settings”

> The marker specifications in stylesheets also include the \Color parameter. If this option is checked, then these settings will be used to produce colored text output. For example the \wj Words of Jesus\wj* marker might specify \Color Red which will only take effect if this option is also enabled - otherwise all text will appear in black.

Also covers coloured headings or any other colour set in the styles. Check with your printer whether colour printing is possible and what it costs.

##### Script for Numbers

Link · Regular+ · `lb_NumberScript`  
Greyed out by: “Lock UI Layout Settings”

> To change the script for numbers, click here to locate the Digit Mapping setting at the end of the Font selection dialog.

Opens the dialog for the Regular font.

#### Use Fallback Font

##### Find Missing Characters

Button · Regular+ · `btn_findMissingChars`  
Also: Find Missing Characters button · Needs: “Use Fallback Font” · Greyed out by: “Lock UI Layout Settings”

> If the primary font is missing any characters (special punctuation, quotes or glossary markers), then these can be listed here, and handled using the Font specified below.
>
> It is recommended that you select as many scripture books as available before using this tool to find missing characters.
>
> Note that the following characters are reserved and are ignored by the Fallback font functionality:  
>            \u2018 \u2019 \u201c \u201d * # %

Digits and markers are not checked. If characters are missing, **Use Fallback Font** is ticked; if not, PTXprint says a fallback font is not needed and unticks it. Hover over the list afterwards to see the character codes.

##### Select Font...

Button · Regular+ · `bl_fontExtraR` · cfg `document/fontextraregular`  
Also: Select font to display missing characters · Needs: “Use Fallback Font” · Greyed out by: “Lock UI Layout Settings”

> Click to select a font to be used as a substitute or "fallback" for the characters listed above which are not in the Regular font.
>
> Select a font to be used as a substitute or "fallback" for the characters listed above which are not in the Regular font.
>
> Note that if the label text is RED, it means that the font currently selected doesn't have all the missing characters either, so it is wise to choose another font.

It must be a different font from the Regular font.

##### Missing Characters

Text box · Regular+ · `t_missingChars` · cfg `paragraph/missingchars`  
Needs: “Use Fallback Font” · Greyed out by: “Lock UI Layout Settings”

> First use the button (on the left) to find any characters missing from the primary font. You may add to this list if needed. Use spaces between items. Note that you can also use \u0ABC codes to enter hard-to-type characters.

Codes can be typed like `\u2E24`. Quotation marks (‘ ’ “ ”) and `*`, `#`, `%` are ignored.

#### Hyphenation

##### Hyphenate

Checkbox, off · Regular+ · `c_hyphenate` · cfg `paragraph/ifhyphenate`, `paragraph/ifnothyphenate`  
Greyed out by: “Lock UI Layout Settings”

> To hyphenate properly you need to first create a Hyphenation List using the 'Create List...' button. This will create a XeTeX hyphenation list from the hyphenation list in Paratext.
>
> Note that for Hyphenation to work properly, the Spacing Adjustments 'Between Letters' option needs to be disabled.

Create the list first. Ticking it unticks **Between Letters** spacing. When unticked, PTXprint does not hyphenate at all.

##### Create List...

Button · Regular+ · `btn_generateHyphenationList`  
Also: Create Hyphenation List · Greyed out by: “Lock UI Layout Settings”

> Click this button to generate a hyphenation list that can be used by XeTeX to optimize hyphenation. This will read Paratext's HyphenatedWords.txt list and create a TeX hyphen list for this language.

Opens the **Create List** dialog. Do this again when the Paratext list changes.

##### Omit '-'Hyphen

Checkbox, off · Regular+ · `c_omitHyphen` · cfg `paragraph/ifomithyphen`  
Also: Omit hyphen from hyphenated words · Greyed out by: “Lock UI Layout Settings”

> Some scripts use hyphenation to break long words onto the next line, BUT don't need to display the actual '-' character. If this option is checked, then "hyphens" will be invisible.

Makes the hyphen at a line break invisible.

##### Make Hyphens Non-Breaking

Checkbox, off · Regular+ · `c_nonBreakingHyphens` · cfg `paragraph/ifnbhyphens`  
Greyed out by: “Lock UI Layout Settings”

> Enable this option to ensure that word-medial hyphens within the text never break across two lines.
>
> By default, lines may break at word-medial hyphens.
>
> If enabled, lines will not break at these hyphens.

Create the hyphenation list again after changing this, because the list is made with the chosen kind of hyphen.

#### Spacing Adjustments

##### Between Words

Checkbox, on · Regular+ · `c_spacing` · cfg `document/ifspacing`  
Also: Spacing Between Words · Greyed out by: “Lock UI Layout Settings”

> The horizontal distance that the space character can use between words is adjustable - and allows a greater degree of flexibility when trying to shrink or grow paragrahs when balancing pages.

Uses the **Min/Shrink** and **Max/Stretch** values. When unticked, standard values are used.

##### Between Letters

Checkbox, on · Regular+ · `c_letterSpacing` · cfg `document/ifletter`, `document/letterspace`  
Also: Spacing Between Letters · Greyed out by: “Interlinear  &  Code”, “Lock UI Layout Settings”

> Enabling letter spacing allows the spaces between characters to be adjusted (usually by a very small percentage). This might help alleviate space problems. Values are in percentage of the text point size and get used everywhere.
>
> Warning: Only use this if really needed! In some cases, enabling this setting will prevent hyphenation from working at all. In other cases it can make the text look very ugly.
>
> Note that if this option is disabled, then it is due to the Interlinear option being set on the Advanced page. These two settings are mutually exclusive.
>
> Letter spacing is also not used if 'Contextual Spaces' is set for the Regular font.

Use it only when needed. PTXprint unticks it when you tick **Hyphenate**.

##### Min/Shrink – Spacing Between Words (Min/Shrink)

Number · Regular+ · `s_minSpace` · cfg `document/spaceshrink`  
Values: 10–200 (default 50) · Needs: “Between Words” · Greyed out by: “Lock UI Layout Settings”

> When justifying paragraphs, and especially when trying to shrink or grow a paragraph to take fewer or more lines, the horizontal distance that a space uses can be adjusted - allowing the text to shrink or grow. Lower values will enable a 'tighter' text and make it more flexible, but keep the readers in mind - and their need to distinguish word-breaks with ease. This value is a % percentage of a normal space width. TeX's default value is 66%.
>
> Minimum size % that a space can shrink to when necessary.

Lower values fit more text on a line, but words may become hard to tell apart. About 50–80 is common.

##### Max/Stretch – Spacing Between Words (Max/Stretch)

Number · Regular+ · `s_maxSpace` · cfg `document/spacestretch`  
Values: 50–999 (default 200) · Needs: “Between Words” · Greyed out by: “Lock UI Layout Settings”

> When justifying paragraphs, and especially when trying to shrink or grow a paragraph to take fewer or more lines, the horizontal distance that a space uses can be adjusted - allowing the text to shrink or grow. Larger values will enable a 'looser' text and make it more flexible to grow, but be careful to avoid 'rivers' or white space in paragraphs. This value is a % percentage of a normal space width. TeX's default value is 150%.
>
> Maximum size % that a space can grow to when necessary.

Higher values let lines stretch more, but can leave big gaps. About 150–200 is common.

##### Spacing Between Letters (Min/Shrink)

Number · Regular+ · `s_letterShrink` · cfg `document/lettershrink`  
Needs: “Between Letters” · Greyed out by: “Interlinear  &  Code”, “Lock UI Layout Settings”

> Values are in percentage of the text point size.

Keep it small (a few percent at most).

##### Spacing Between Letters (Max/Stretch)

Number · Regular+ · `s_letterStretch` · cfg `document/letterstretch`  
Needs: “Between Letters” · Greyed out by: “Interlinear  &  Code”, “Lock UI Layout Settings”

> Values are in percentage of the text point size.

Keep it small.

#### Writing System

##### Text Flow Direction – Text direction (Right-to-left RTL etc)

Drop-down · Basic+ · `fcb_textDirection` · cfg `document/ifrtl`, `document/toptobottom`  
Choices: Left-to-Right | Right-to-Left | Top-to-Bottom (and Left-to-Right) · Greyed out by: “Lock UI Layout Settings”

> Select the direction for the text to flow. Note that the option for "Top to Bottom" lays out the vertical lines left to right.

**Right-to-Left** also ticks **RTL Book Binding**. Changing this changes the whole layout.

##### Text Script

Drop-down · Basic+ · `fcb_script` · cfg `document/script`  
Choices: Latn · Greyed out by: “Lock UI Layout Settings”

> Choose the script of the text. It is used for font shaping, and PTXprint provides additional typesetting functionality for some scripts:  
> Arabic, Myanmar, Thai, Lao, Tai Tham, New Tai Lue, Bengali, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, and Chinese (Han).
>
> If set to "Default", PTXprint tries to detect the script when the project is opened.

For example, it makes `/` a word-break mark in Thai, Lao, Myanmar, Tai Tham and New Tai Lue. Changing it may also change **Digit mapping** and **Specify Line Break Locale**.

##### Additional Script Settings...

Button · Basic+ · `btn_scrsettings`  
Greyed out by: “Lock UI Layout Settings”

> A small number of complex scripts (such as Myanmar, Indic, Arabic & Han) have additional options which can be set individually.

Only active for scripts that have options: Myanmar, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, Arabic, and Han (Simplified and Traditional).

##### Specify Line Break Locale

Checkbox, off · Regular+ · `c_linebreakon` · cfg `document/iflinebreakon`  
Also: Enable Line Break Locale · Greyed out by: “Lock UI Layout Settings”

> Some languages that use complex scripts need dictionary support for line breaking. Note that the dictionary used will be LWC-specific. For example, zh for Chinese, ko for Korean, etc. Note that Graphite fonts can also have line breaking rules which can be enabled by using the gr locale.

For scripts with no spaces between words. Ticked automatically when you choose a Han, Japanese or Korean script.

##### Set Line Break Locale

Text box · Regular+ · `t_linebreaklocale` · cfg `document/linebreaklocale`  
Needs: “Specify Line Break Locale” · Greyed out by: “Lock UI Layout Settings”

> Language code for dictionary-based line breaking (for scripts without spaces between words):  
> ja = Japanese km = Khmer ko = Korean my = Myanmar th = Thai zh = Chinese  
>    OR gr = Graphite

`gr` uses the line-breaking rules built into a Graphite font.

##### RTL Book Binding

Checkbox, off · Regular+ · `c_RTLbookBinding` · cfg `cover/rtlbookbinding`  
Also: Set the binding to Right (for RTL publications) · Greyed out by: “Lock UI Layout Settings”

> Enable this for Right-to-Left publications (so that the book is bound on the right hand side).

Affects where the binding gutter goes, how PDF viewers show the pages, and the cover. Ticked automatically when you choose **Right-to-Left** text direction.
