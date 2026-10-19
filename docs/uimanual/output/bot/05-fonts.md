# Fonts+Script tab

## What this tab is for

The **Fonts+Script** tab controls *how the letters look* and *how the writing system behaves*. Here you choose the fonts, tell PTXprint which script (writing system) the text uses, choose the writing direction, and control hyphenation and spacing.

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

* Choose the **Regular** font first. PTXprint then fills in **Bold**, **Italic** and **Bold Italic** for you from the same font family, with the same features and options. This happens every time you click **OK** in the **Pick a Font** dialog for **Regular**. So if you want a different bold or italic font, choose it *after* you have finished with the Regular font.
* If the font family does not have a bold or italic typeface, PTXprint *fakes* it (makes the regular letters thicker or slanted). The button then shows the style in brackets, for example *(bold)*. Faked bold and italic are usable, but a real bold or italic typeface looks better.
* If your Paratext project's language settings name font features for this font, PTXprint uses those features when you choose it (unless you have already set features).
* Only the **Regular** button is shown in the **Mini** view. The other three are shown from the **Basic** view upwards.

Click **Refresh Font List** if you have just installed a font and it is not in the list.

**Enable Colored Text (as Specified in Stylesheet)** prints text in colour where a style asks for a colour (for example red letters for the words of Jesus). If it is not ticked, all text is black.

**Script for Numbers** is a link. It opens the **Pick a Font** dialog with the **Digit mapping** setting highlighted (see below).

## Pick a Font (and Typeface) dialog

This dialog opens when you click any **Select Font...** button.

1. Type part of the font name in the search box to find it quickly.
2. Click a font in the list. Fonts shown in **bold** in the list have all four typefaces (Regular, Bold, Italic, Bold Italic).
3. Choose the **Typeface** you want.
4. Change other options if needed (see below), then click **OK**.

If a font is missing from the list, it may not be installed for all users on the computer. Install it, then click **Refresh Font List** on the **Fonts+Script** tab.

The other options in the dialog are:

* **Fake Bold/Italic** – make bold and/or italic from the regular typeface. **Embolden** sets how much thicker the letters become. **Slant** sets how much they lean (0.15 is a normal italic slant; a negative value leans the other way).
* **Stretch** – make all letters wider (more than 1.00) or narrower (less than 1.00). For example 0.95 makes text 5% narrower, so more fits on a line. Use small changes only, because the letter shapes become distorted.
* **Graphite Rendering** – use SIL's Graphite technology for this font. Tick it only for fonts that are made for Graphite and need it (the font's documentation will say so). Ticking or unticking it clears the font features.
* **Contextual Spaces** – tick only if the font itself changes the width of spaces depending on the letters around them. When this is ticked for the Regular font, **Between Letters** spacing is not used.
* **Font features** (the text box) and **Select Features...** – turn on or off special options in the font.
* **Digit mapping** – print numbers in another script's digits.

### Digit mapping (numbers in your own script)

Many scripts have their own digits, for example Arabic-Indic ٠١٢٣, Devanagari ०१२३, Myanmar ၀၁၂၃ or Thai ๐๑๒๓. If your Paratext text uses the Western digits 0–9 but you want to print your script's digits, choose your script in **Digit mapping**. PTXprint then changes the digits when it prints, for numbers printed in that font (for example chapter and verse numbers).

* Check that your font has shapes for these digits. If it does not, you will see empty boxes.
* When you change **Text Script** on the **Fonts+Script** tab, PTXprint also tries to choose the matching digit mapping. Check it and change it if needed.
* If your text already contains your script's digits, leave **Digit mapping** on **Default**.

### Select Font Features dialog

Click **Select Features...** to see the features in the selected font as a list of tick boxes and drop-down lists. Hover the mouse over a feature name to see a short description (when the font gives one).

* The **Language** list lets you choose a language that the font knows about. Some fonts use different letter shapes for different languages. When you choose a language, the features change to that language's defaults.
* If **Graphite Rendering** is ticked, you see the font's Graphite features. If not, you see its OpenType features.
* When you click **OK**, PTXprint writes your choices into the font features text box, for example `language=ur, cv12=1`. Only features you changed from the default are written.

Choosing a different font in the list clears the font features.

## Use Fallback Font

Some fonts do not contain every character in your text, for example special quotation marks or the glossary markers. These characters then print as empty boxes (tofu). A *fallback font* is a second font that PTXprint uses only for those characters.

1. Tick **Use Fallback Font**.
2. Click **Find Missing Characters**. PTXprint checks the books you have selected (on the **Basic** tab) against the Regular font, and lists the characters that are missing. Select as many books as possible first. If nothing is missing, PTXprint tells you and unticks **Use Fallback Font**.
3. Click **Select Font...** next to the list and choose a font that has these characters. If the label turns **red**, the chosen font does not have all the characters either; choose another one.

You can add characters to the list by hand, separated by spaces. You can type a character code as `\u` plus four hex digits, for example `⸤`. Straight and curly quotation marks (‘ ’ “ ”) and the characters `*`, `#` and `%` are ignored by the fallback font.

These settings are shown in the **Default** and **Full** views.

## Writing System

This area tells PTXprint how your script works. It is very important for non-Latin scripts.

### Text Flow Direction

* **Left-to-Right** – for scripts such as Latin, Cyrillic, Devanagari, Ethiopic, Thai and Myanmar.
* **Right-to-Left** – for scripts such as Arabic, Hebrew, Syriac and Thaana. When you choose this, PTXprint also ticks **RTL Book Binding**.
* **Top-to-Bottom (and Left-to-Right)** – vertical text, with the lines going from left to right.

### RTL Book Binding

A right-to-left book is bound on the right side and opens from the "back" (as seen by a left-to-right reader). Tick **RTL Book Binding** so that PTXprint places the binding gutter, the page order in PDF viewers and the cover correctly for a right-to-left book.

### Text Script

**Text Script** tells the font which script rules to use. These rules join letters (for example in Arabic), place vowel marks and other marks correctly, and reorder letters where needed (for example in Indic scripts).

* When a project is opened and **Text Script** is **Default**, PTXprint looks at the text and tries to choose the script for you. Check that it is right.
* Choosing the right script also switches on extra processing that PTXprint has for some scripts (see the next section).
* For most Latin-script languages you can leave it on **Default** or **Latin**.

### Additional Script Settings...

This button is only active when the chosen script has extra options. It opens a small dialog. The options are:

* **Myanmar (Burmese)** – **Syllable line breaking**: let PTXprint break lines between syllables, not only at spaces.
* **Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya** – **Syllable line breaking**: let PTXprint break long words between syllables. **Show Hyphen**: print a hyphen where a word is broken (if not ticked, the break is invisible).
* **Arabic** – **First verse on left**: a setting for how verse references are written.
* **Han (Simplified)** and **Han (Traditional)** – **Enabling horizontal gridding**: align chapter numbers with the character grid and remove spaces before verses. **Automatic halfwidth punctuation pairs**: when two punctuation marks come together, make them share the width of one full character.

### Scripts that do not use spaces between words

Some scripts (for example Thai, Lao, Khmer, Myanmar, Tai Tham, New Tai Lue, Chinese and Japanese) do not put spaces between words. PTXprint must know where it may break a line. There are two ways:

* **Mark break points in the text with "/".** For Thai, Lao, Myanmar, Tai Tham (Lanna) and New Tai Lue, when **Text Script** is set to that script, PTXprint turns each `/` in the text into an invisible break point. The `/` itself is not printed.
* **Use a line-break dictionary.** Tick **Specify Line Break Locale** and type a code in the box: `th` (Thai), `km` (Khmer), `my` (Myanmar), `zh` (Chinese), `ja` (Japanese), `ko` (Korean), or `gr` to use the line-breaking rules inside a Graphite font. When you choose a Han, Japanese or Korean script in **Text Script**, PTXprint fills this in for you.

These options are shown in the **Default** and **Full** views.

## Hyphenation

PTXprint can hyphenate words using the hyphenation list from your Paratext project. In Paratext, the Wordlist tool suggests where words can be broken, and you approve the suggestions. PTXprint turns that list into a list it can use.

1. Click **Import List...**. The **Create Hyphenation List** dialog opens.
2. Choose the options (see below) and click **OK**. PTXprint shows a message saying how many words it used.
3. Tick **Hyphenate**.
4. Click **Print**.

You only need to create the list again when the Paratext hyphenation list changes.

When you tick **Hyphenate**, PTXprint unticks **Between Letters** in **Spacing Adjustments**, because letter spacing stops hyphenation from working well. A message in the status bar tells you this.

**Omit '-'Hyphen** – some scripts break long words at the end of a line but do not show a hyphen. Tick this to make the hyphen invisible.

**Make Hyphens Non-Breaking** – PTXprint uses non-breaking hyphens, so a line will not be broken at a hyphen that is already in the text. Create the hyphenation list again after you change this.

### Create Hyphenation List dialog

* **Only Use Approved Hyphenation Words** (ticked by default) – use only the words whose break points you approved in Paratext. Untick it to use all words, including Paratext's unchecked guesses. If the list comes out empty, try unticking this.
* **Limit Hyphenation List to Words Found in** – use only words that appear in the books you are printing. The books are listed beside this option. Use this when the full list is too long. (If the list is longer than the typesetting engine can handle, PTXprint keeps the most frequent words.)
* **Add Syllable-Based Hyphenated Words** – only for scripts where **Syllable line breaking** is ticked in **Additional Script Settings...**. It adds break points for more words using the syllable rules.
* **Advanced** – limits on which words are added: **Minimum affix**, **Minimum length** and **Min non-hyphen**.

## Spacing Adjustments

When text is justified (both edges straight), PTXprint stretches or shrinks the spaces in each line. This area controls how much.

* **Between Words** – the smallest (**Min/Shrink**) and largest (**Max/Stretch**) size of a space between words, as a percentage of a normal space. A lower minimum lets more words fit on a line. A higher maximum lets lines stretch more. Too low makes words hard to separate; too high leaves big gaps ("rivers" of white space).
* **Between Letters** – also lets PTXprint add or remove a very small amount of space between letters. The numbers are a percentage of the font size, so keep them small. Use this only when you really need it: it can make text look uneven and it stops hyphenation from working well.

**Between Letters** is greyed out when **Interlinear & Code** is ticked on the **Advanced** tab. It is also not used when **Contextual Spaces** is ticked for the Regular font, and it is unticked when you tick **Hyphenate**.

These settings are shown in the **Default** and **Full** views.

## Add Tatweel (kashida) Rules dialog

In Arabic script, a *tatweel* (also called *kashida*, the character ـ) is a joining stroke that makes a word longer. It is used to make lines look better or to fill a line. This dialog helps you write a *change rule* that adds tatweels to one word at one verse. The rule goes into the project's changes file (changes.txt), which PTXprint applies every time it prints.

To open the dialog: on the **View+Edit** tab, open the changes file. In the **Code Snippets** area at the side, click **Arabic**, then **Add Tatweels**. (This is advanced.)

1. In Paratext (or anywhere), copy the word or short phrase you want to lengthen (up to 60 characters). The dialog fills in **Word / Phrase** from the clipboard by itself. On Windows, it also fills in **Reference** from the current Paratext reference.
2. Check the **Reference**.
3. Set **Tatweels to insert**.
4. Click in **Word / Phrase** where the tatweels should go, and press **Ctrl+`** (Ctrl and the grave-accent key). Repeat for other places in the word.
5. Check the rule in **The rule to be added to Changes.txt**. It looks like `at REF 'original' > 'new'`.
6. Click **Insert Rule**. The rule is added at the cursor position in the file you have open on the **View+Edit** tab.
7. Save the file and click **Print**.

## Common tasks

### How do I change the main font?

1. On the **Fonts+Script** tab, in **Font Configuration**, click the **Select Font...** button next to **Regular**.
2. Type part of the font name in the search box, then click the font.
3. Click **OK**.
4. Check the **Bold**, **Italic** and **Bold Italic** buttons. If a style is in brackets, it will be faked.
5. Click **Print**.

### How do I get rid of empty boxes (tofu) in the printed text?

1. Make sure all the books are selected on the **Basic** tab.
2. On the **Fonts+Script** tab, tick **Use Fallback Font**.
3. Click **Find Missing Characters**.
4. Click the **Select Font...** button beside the list and choose a font that has these characters. If the label turns red, try another font.
5. Click **Print**.

### How do I print numbers in my own script's digits?

1. On the **Fonts+Script** tab, click the **Script for Numbers** link (or click **Select Font...** for **Regular**).
2. In the **Pick a Font** dialog, choose your script in **Digit mapping**.
3. Click **OK**, then click **Print**.
4. Check that the font has those digits.

### How do I set up a right-to-left script (for example Arabic or Hebrew)?

1. On the **Fonts+Script** tab, choose a font made for your script.
2. In **Writing System**, set **Text Flow Direction** to **Right-to-Left**. **RTL Book Binding** is ticked for you.
3. Set **Text Script** to your script (for example **Arabic** or **Hebrew**).
4. If your font needs Graphite (for example some Nastaliq fonts), open **Select Font...**, tick **Graphite Rendering** and click **OK**.
5. Click **Print**.

### How do I set up a script that has no spaces between words?

1. On the **Fonts+Script** tab, set **Text Script** to your script.
2. If your text marks word breaks with `/` (Thai, Lao, Myanmar, Tai Tham, New Tai Lue), nothing more is needed: the `/` marks become invisible break points.
3. Otherwise, tick **Specify Line Break Locale** and type the code for your language (for example `th`, `km`, `my`, `zh`, `ja` or `ko`).
4. For Myanmar or Indic scripts, click **Additional Script Settings...** and consider **Syllable line breaking**.
5. Click **Print**.

### How do I turn on hyphenation?

1. Make sure hyphenation points have been approved in the Paratext Wordlist.
2. On the **Fonts+Script** tab, in **Hyphenation**, click **Import List...**.
3. Click **OK** in the dialog and read the message.
4. Tick **Hyphenate**.
5. Click **Print**.

### How do I choose a different form of a letter that the font offers?

1. Click **Select Font...** for **Regular**.
2. Click **Select Features...**.
3. Choose your language in **Language** (if it is listed), then tick or choose the feature you want.
4. Click **OK** in both dialogs, then click **Print**. PTXprint copies the Regular font's features to the Bold, Italic and Bold Italic fonts.

### How do I fit more text on each line?

1. On the **Fonts+Script** tab, in **Spacing Adjustments**, make **Min/Shrink** (Between Words) a little smaller.
2. Or, in the **Pick a Font** dialog, set **Stretch** to a value slightly below 1.00 (for example 0.97).
3. Click **Print** and check that the text is still easy to read.

## Common problems

### The whole Fonts+Script tab is greyed out

**Cause:** **Lock UI Layout Settings** is ticked on the **Advanced** tab.

**What to do:** Change to the **Full** view. On the **Advanced** tab, **Main** tab, **General** area, untick **Lock UI Layout Settings**.

### Some characters print as empty boxes

**Cause:** The Regular font does not contain those characters.

**What to do:** Use **Use Fallback Font** and **Find Missing Characters** (see Common tasks), or choose a Regular font that supports your whole character set.

### My font is not in the list

**Cause:** The font is not installed, or was installed only for one user, or PTXprint has not refreshed its list.

**What to do:** Install the font for all users, then click **Refresh Font List** on the **Fonts+Script** tab.

### Bold or italic looks thick, blurred or slanted wrongly

**Cause:** The font has no real bold or italic, so PTXprint fakes it. The style is shown in brackets on the button.

**What to do:** Choose a font family that has real bold and italic typefaces, or change **Embolden** and **Slant** in the **Pick a Font** dialog.

### Letters do not join, or marks are in the wrong place

**Cause:** The **Text Script** may be wrong, or the font needs Graphite rendering.

**What to do:** Set **Text Script** to your script. If the font is a Graphite font, tick **Graphite Rendering** in the **Pick a Font** dialog.

### Additional Script Settings... is greyed out

**Cause:** The script chosen in **Text Script** has no extra options.

### Long lines do not break in Thai, Khmer, Myanmar, Chinese and similar scripts

**Cause:** PTXprint does not know where it may break the line.

**What to do:** Set **Text Script**, and either mark breaks with `/` in the text (for Thai, Lao, Myanmar, Tai Tham, New Tai Lue) or tick **Specify Line Break Locale** and type the language code.

### Hyphenation does not work

**Possible causes and what to do:**

* No list was created. Click **Import List...** first.
* The list is empty because no words are approved in Paratext. Untick **Only Use Approved Hyphenation Words** and create the list again, or approve words in Paratext.
* **Between Letters** is ticked. Untick it.
* **Hyphenate** is not ticked.

### Between Letters is greyed out

**Cause:** **Interlinear & Code** is ticked on the **Advanced** tab. These two settings cannot be used together.

### Font features I set have disappeared

**Cause:** Choosing another font in the list, or ticking or unticking **Graphite Rendering**, clears the features.

**What to do:** Set the features again after choosing the font and the Graphite option.

### Numbers print as boxes after choosing a digit mapping

**Cause:** The font does not have the digits for that script.

**What to do:** Choose a font that has these digits, or set **Digit mapping** back to **Default**.

### Text is printed in black even though styles have colours

**Cause:** **Enable Colored Text (as Specified in Stylesheet)** is not ticked.

## Settings reference: Fonts+Script tab

Every control in this part of PTXprint is listed below, grouped by where it appears.

### Create Hyphenation List (dialog)

#### OK

- **Where:** Create Hyphenation List (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Creates the hyphenation list with the chosen options and shows a message with the number of words used. Read the message: it tells you if the list was empty or had to be shortened.

*(Internal ID: `btn_gnr8pl_ok1`)*

#### Cancel

- **Where:** Create Hyphenation List (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without creating a list.

*(Internal ID: `btn_gnr8pl_cancel1`)*

### Create Hyphenation List (dialog) › When Creating Hyphenation List

#### Add Syllable-Based Hyphenated Words

- **Where:** Create Hyphenation List (dialog) › When Creating Hyphenation List
- **Type:** Checkbox (not ticked by default)
- **Description:** Append syllable-based hyphenated words to hyphen list
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> This advanced hybrid option is only available if Syllable Line Breaking has been enabled under Additional Script Settings for Complex Scripts.
>
> If enabled, it will use Syllable Line Breaking to hyphenate words from the books selected so that a combination of manually-marked hyphenation along with automated hyphenation is possible.

**Explanation:**

Adds more words to the list, broken at syllable boundaries using PTXprint's syllable rules for your script. It is greyed out unless **Syllable line breaking** is ticked in **Additional Script Settings...** (Myanmar and some Indic scripts). Use it when Paratext's list covers only some words.

*(Internal ID: `c_addSyllableBasedHyphens` · Config key: `paragraph/ifsylhyphens`)*

#### Limit Hyphenation List to Words Found in

- **Where:** Create Hyphenation List (dialog) › When Creating Hyphenation List
- **Type:** Checkbox (not ticked by default)
- **Description:** Limit hyphenation list to only include words in active books
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Normally ALL hyphenated words from ALL books are included in PTXprint's hyphenated wordlist.
>
> However, if the list of hyphenated words is too long (greater than 63929 words) then you can prioritize which words to include by enabling this option to only use words from the books being printed.
>
> Note that if there are too many words in the Paratext hyphenation file, PTXprint will automatically prioritize the list created for XeTeX based on frequency.

**Explanation:**

Keeps only the words that appear in the books you are printing (listed beside this option). Use it when the full Paratext list is very long. If the list is still too long for the typesetting engine, PTXprint keeps the words that appear most often.

*(Internal ID: `c_hyphenLimitBooks` · Config key: `paragraph/ifhyphlimitbks`)*

#### Only Use Approved Hyphenation Words

- **Where:** Create Hyphenation List (dialog) › When Creating Hyphenation List
- **Type:** Checkbox (ticked by default)
- **Description:** Only use words where hyphenation points have been approved in Paratext
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The Paratext WordList tool guesses hyphenation points based on syllable structure and patterns in the language.
>
> However, it expects the user to (i) check and, if appropriate, (ii) approve the suggested hyphenation points (by clicking the check mark making it appear green).
>
> Normally only the approved hyphenated words will be used when creating the hyphenation list for PTXprint/TeX to use.
>
> However, if you wish to include ALL words (regardless of their approval status) then disable this option.

**Explanation:**

When ticked, only words whose break points you approved in the Paratext Wordlist are used. This is the safe choice. Untick it to include Paratext's unchecked guesses too; check the printed result carefully if you do.

*(Internal ID: `c_hyphenApprovedWords` · Config key: `paragraph/ifhyphapproved`)*

### Create Hyphenation List (dialog) › When Creating Hyphenation List › Advanced

#### Minimum affix

- **Where:** Create Hyphenation List (dialog) › When Creating Hyphenation List › Advanced
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 10, default 3

**Tooltip (the text shown when you hover the mouse over it):**

> Do not add any words to the hyphenation list that include an optional hyphen less than this number of characters at the beginning or end of the word.

**Explanation:**

Leaves out words that have a break point too close to the start of the word (fewer than this many characters). This stops very short pieces such as one or two letters being left at the end of a line. The default of 3 is usually good.

*(Internal ID: `s_hyphMinprefix`)*

#### Minimum length

- **Where:** Create Hyphenation List (dialog) › When Creating Hyphenation List › Advanced
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 3 to 50, default 7

**Tooltip (the text shown when you hover the mouse over it):**

> The minimum word length (including optional hyphens) that will be added to the hyphenation list.

**Explanation:**

Leaves out short words. Only words longer than this number of characters are added to the list. Short words rarely need to be broken.

*(Internal ID: `s_hyphMinWord`)*

#### Min non-hyphen

- **Where:** Create Hyphenation List (dialog) › When Creating Hyphenation List › Advanced
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** from 1 to 50, default 9

**Tooltip (the text shown when you hover the mouse over it):**

> Minimum word length for a word to block hyphenation.

**Explanation:**

Intended for long words that have no break points in the Paratext list. In current versions it does not appear to change the list that is created, so you can leave it at the default.

*(Internal ID: `s_hyphMinBlock`)*

### Add Tatweel (kashida) Rules (dialog)

#### Insert Rule

- **Where:** Add Tatweel (kashida) Rules (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Adds the rule shown at the bottom of the dialog at the cursor position in the file open on the **View+Edit** tab. Make sure the changes file is the file that is open. Save the file afterwards.

*(Internal ID: `btn_tatweel_insertRule`)*

#### Close

- **Where:** Add Tatweel (kashida) Rules (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog. It also stops the dialog from watching the clipboard.

*(Internal ID: `btn_tatweel_close`)*

#### Reference

- **Where:** Add Tatweel (kashida) Rules (dialog)
- **Type:** Text box
- **Description:** Tatweel Dialog: Enter reference
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enter the verse reference where the word is located.
>
> (Note that the reference is automatically updated from the current Paratext reference.)

**Explanation:**

The verse reference (for example `GEN 1:1`) where the word is. On Windows it is filled from the current Paratext reference each time you copy a new word. The rule only changes the word at this reference.

*(Internal ID: `t_tatweelRef`)*

#### Word / Phrase

- **Where:** Add Tatweel (kashida) Rules (dialog)
- **Type:** Text box
- **Description:** Tatweel Dialog: Enter word or phrase to be lengthened
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Enter the word to be lengthened and place the cursor at the location and use shortcut Ctrl-` (Ctrl-grave) to insert Tatweels. Repeat at other words and/or locations.
>
> (Note that this box is automatically updated from the clipboard if the word/phrase is 60 characters or less).

**Explanation:**

The word or phrase to lengthen. It is filled in automatically when you copy text of 60 characters or less. Click where the tatweels should go and press **Ctrl+`** to insert them. The "before" part of the rule is the text you copied, so copy the exact word from the text; do not just type it here.

*(Internal ID: `t_tatweelText`)*

#### Tatweels to insert

- **Where:** Add Tatweel (kashida) Rules (dialog)
- **Type:** Number box
- **Description:** Tatweel Dialog: Number of Tatweels to insert
- **View level:** Default and Full views
- **Values:** from 1 to 20

**Tooltip (the text shown when you hover the mouse over it):**

> How many Tatweels should be inserted at the current cursor location?

**Explanation:**

How many tatweel characters are inserted each time you press **Ctrl+`**. Start with 1 or 2 and check the printed result.

*(Internal ID: `s_tatweelLength`)*

#### The rule to be added to Changes.txt

- **Where:** Add Tatweel (kashida) Rules (dialog)
- **Type:** Text box
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> The rule to be added to Changes.txt

**Explanation:**

The finished rule, in the form `at REF 'original' > 'new'`. Check it before you click **Insert Rule**.

*(Internal ID: `t_tatweelPreview`)*

### Pick a Font (and Typeface) (dialog)

#### OK

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Uses the selected font, typeface and options for the button you clicked.

*(Internal ID: `btn_font_ok`)*

#### Cancel

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing the font.

*(Internal ID: `btn_font_cancel`)*

#### Choose a font from the installed fonts. Fonts shown in BOLD ...

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Table
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Choose a font from the installed fonts. Fonts shown in BOLD have all 4 typefaces.
>
> If you cannot locate the desired font in this list, then it is quite likely that it has not been installed "For all Users" in the Windows system.

**Explanation:**

The list of installed fonts. Click a font to select it. Fonts in **bold** have all four typefaces (Regular, Bold, Italic, Bold Italic). Choosing a different font clears the font features.

*(Internal ID: `tv_fontFamily`)*

#### Typeface

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Drop-down list
- **Description:** Font Selection Dialog: Typeface
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Choices:** Regular; Bold; Italic; Bold Italic

**Tooltip (the text shown when you hover the mouse over it):**

> Fonts which have all 4 typefaces (regular, bold, italic, and bold-italic) are shown in BOLD in the list above.
>
> If you cannot locate the desired font in this list, then it is quite likely that it has not been installed "For all Users" in the Windows system.

**Explanation:**

The typeface of the selected font to use. Normally choose **Regular** for the Regular button, **Bold** for the Bold button, and so on. Fonts may offer other faces too, such as Light or Semibold.

*(Internal ID: `fcb_fontFaces`)*

#### Font Selection Dialog: Find a font

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Search box
- **View level:** All view levels (Mini, Basic, Default, Full)

**Tooltip (the text shown when you hover the mouse over it):**

> Type the start of a font name to jump to it in the list.

**Explanation:**

Type part of a font name to jump to it in the list.

*(Internal ID: `t_fontSearch`)*

#### Fake Bold/Italic

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Font Selection Dialog: Fake bold or italic typeface
- **View level:** Basic, Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If the font you are using doesn't have multiple typefaces (such as Bold, Italic and Bold-Italic) then you can "fake" these by adding boldness and/or slant to the regular typeface.

**Explanation:**

Tick this to make a bold and/or italic look from the regular typeface, using **Embolden** and **Slant**. Use it only when the font has no real bold or italic. PTXprint also fakes styles automatically when it cannot find them; the font button then shows the style in brackets.

*(Internal ID: `c_fontFake`)*

#### Stretch

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Number box
- **Description:** Font Selection Dialog: Stretch (or shrink) font setting
- **View level:** Default and Full views
- **Values:** from 0.5 to 2, default 1

**Tooltip (the text shown when you hover the mouse over it):**

> The shapes of the characters can be stretched (larger) or condensed (smaller) to occupy more horizontal space, or less (shrink text).  
> 1.00 = 100% = normal  
> 0.95 =   95% = shrink text  
> 1.05 = 105% = expand text

**Explanation:**

Makes letters wider (above 1.00) or narrower (below 1.00). Small changes such as 0.95–1.05 can help fit text, but large changes distort the letter shapes. When you set it for the Regular font, PTXprint copies it to the Bold, Italic and Bold Italic fonts.

*(Internal ID: `s_fontExtend`)*

#### Font Selection Dialog: Selected font features

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Text box
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> You can enable/disable any font features for the selected font. For example:  
> smcp=1, cv12=2 Use 'Select Features...' to choose them from a list.

**Explanation:**

The font features in use, written as a list such as `smcp=1, cv12=2` (and sometimes `language=xx`). The easy way to fill it is the **Select Features...** button. It is cleared when you choose a different font or change **Graphite Rendering**.

*(Internal ID: `t_fontFeatures`)*

#### Contextual Spaces

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Font Selection Dialog: Use contextual spaces
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Set this option if the font changes the width of spaces depending on the text around them.

**Explanation:**

Tick only if the font's documentation says that it changes the width of spaces depending on the text around them. When this is ticked for the Regular font, PTXprint switches off **Between Letters** spacing.

*(Internal ID: `c_fontCtxtSpaces`)*

#### Graphite Rendering

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Checkbox (not ticked by default)
- **Description:** Font Selection Dialog: Use Graphite rendering
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> If you require this font to use SIL's Graphite Rendering technology, then enable this.
>
> Changing this clears the font features.

**Explanation:**

Uses SIL's Graphite rendering for this font instead of the normal (OpenType) rendering. Some fonts for complex scripts work best, or only, with Graphite. When ticked, **Select Features...** shows the font's Graphite features. Ticking or unticking it clears the font features.

*(Internal ID: `c_fontGraphite`)*

#### Select Features...

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Button
- **Description:** Font Selection Dialog: Select font features
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Choose font features (and the language) from a list of those this font supports.

**Explanation:**

Opens the **Select Font Features** dialog for the font selected in the list. It shows Graphite features if **Graphite Rendering** is ticked, otherwise OpenType features.

*(Internal ID: `btn_fontFeatures`)*

#### Digit mapping

- **Where:** Pick a Font (and Typeface) (dialog)
- **Type:** Drop-down list
- **Description:** Font Selection Dialog: Digit (number) script mapping
- **View level:** Default and Full views
- **Choices:** Default; Arabic-Hindi; Arabic-Farsi; Burmese

**Tooltip (the text shown when you hover the mouse over it):**

> All known unicode-encoded number/digit systems are catered for. So if you don't want to use the Latin/Arabic numbers [0-9], you can pick the appropriate script here. (Make sure the font you are using supports these digits too.)

**Explanation:**

Prints numbers using the digits of another script, for example Arabic-Indic, Devanagari, Myanmar or Thai. Use it when the text contains 0–9 but the publication should show your script's digits. Make sure the font has those digits. Leave it on **Default** if the text already contains the right digits. The list holds many more scripts than the four shown in the generated list above.

*(Internal ID: `fcb_fontdigits`)*

### Pick a Font (and Typeface) (dialog) › Fake Bold/Italic

#### Embolden

- **Where:** Pick a Font (and Typeface) (dialog) › Fake Bold/Italic
- **Type:** Number box
- **Description:** Font Selection Dialog: Fake bold setting
- **View level:** Basic, Default and Full views
- **Values:** default 1.6
- **Only available when:** “Fake Bold/Italic” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If the required font doesn't have a BOLD typeface, you can use this setting to create the BOLD effect. (For example, setting Embolden to 1.6 would thicken the Regular typeface making it appear as bold.)

**Explanation:**

How much thicker the letters become for faked bold. Larger numbers give thicker letters. It is only active when **Fake Bold/Italic** is ticked. Check the result in print, because too much makes letters fill in.

*(Internal ID: `s_fontBold`)*

#### Slant

- **Where:** Pick a Font (and Typeface) (dialog) › Fake Bold/Italic
- **Type:** Number box
- **Description:** Font Selection Dialog: Fake italic setting
- **View level:** Basic, Default and Full views
- **Values:** from -1 to 1, default 0.15
- **Only available when:** “Fake Bold/Italic” is selected

**Tooltip (the text shown when you hover the mouse over it):**

> If the required font does not have an ITALIC typeface, you can use this setting to create the ITALIC effect. (For example, setting Slant to 0.15 would slant the Regular typeface by 15% making it appear as italic.)

**Explanation:**

How much the letters lean for faked italic. 0.15 is a normal italic slant. A negative value leans the letters the other way. 0 means no slant. It is only active when **Fake Bold/Italic** is ticked.

*(Internal ID: `s_fontItalic`)*

### Select Font Features... (dialog)

#### OK

- **Where:** Select Font Features... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Writes the features you changed into the font features box of the **Pick a Font** dialog. Only features that differ from the default are written.

*(Internal ID: `btn_feats_ok`)*

#### Cancel

- **Where:** Select Font Features... (dialog)
- **Type:** Button
- **View level:** Default and Full views

**Explanation:**

Closes the dialog without changing the features.

*(Internal ID: `btn_feats_cancel`)*

#### Language

- **Where:** Select Font Features... (dialog)
- **Type:** Drop-down list
- **View level:** Default and Full views

**Tooltip (the text shown when you hover the mouse over it):**

> Choose the language the font should use. Some fonts change letter shapes for particular languages.

**Explanation:**

Chooses the language the font should use. Some fonts change letter shapes for different languages. Choosing a language also changes the feature settings to that language's defaults.

*(Internal ID: `fcb_featsLangs`)*

### Fonts+Script tab › Font Configuration

#### Select Font...

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Button
- **Description:** Select Regular font
- **View level:** All view levels (Mini, Basic, Default, Full)
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select the main font for the publication. Note that the font chooser dialog also has a number of other options for setting advanced font features and, if needed, Graphite rendering.

**Explanation:**

The main font for the text. Choose it first: PTXprint then fills in the Bold, Italic and Bold Italic fonts from the same family, with the same features. This happens each time you click **OK** for the Regular font, so any bold or italic font you chose by hand is replaced. All styles that do not name their own font use this font. If your Paratext language settings list features for this font, they are used too.

*(Internal ID: `bl_fontR` · Config key: `document/fontregular`)*

#### Select Font...

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Button
- **Description:** Select Bold font
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you see the style in parentheses (bold) this indicates that PTXprint could not locate the bold style and will fake the style.

**Explanation:**

The bold font. It is filled in automatically when you choose the Regular font. If it shows *(bold)* in brackets, there is no real bold and PTXprint will fake it.

*(Internal ID: `bl_fontB` · Config key: `document/fontbold`)*

#### Select Font...

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Button
- **Description:** Select Italic font
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you see the style in parentheses (italic) this indicates that PTXprint could not locate the italic style and will fake the style.

**Explanation:**

The italic font. It is filled in automatically when you choose the Regular font. If it shows *(italic)* in brackets, there is no real italic and PTXprint will fake it.

*(Internal ID: `bl_fontI` · Config key: `document/fontitalic`)*

#### Select Font...

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Button
- **Description:** Select Bold Italic font
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If you see either of the styles in parentheses (bold) or (italic) this indicates that PTXprint could not locate the style and will fake the bold-italic style.

**Explanation:**

The bold-italic font. It is filled in automatically when you choose the Regular font. Brackets around a style mean that style will be faked.

*(Internal ID: `bl_fontBI` · Config key: `document/fontbolditalic`)*

#### Refresh Font List button

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Button
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Refresh Font List:  
> If you have recently installed a font but it doesn't show in the font list, then try clicking this button to refresh the list.
>
> If it still doesn't show up, then try re-installing the font (in Windows, locate the font file, then right-click on it and select "Install For All Users").
>
> And remember to Refresh the Font List again.

**Explanation:**

Reloads the list of fonts from the computer. Click it after installing a new font. If the font still does not appear, it may need to be installed for all users.

*(Internal ID: `btn_refreshFonts`)*

#### Enable Colored Text (as Specified in Stylesheet)

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The marker specifications in stylesheets also include the \Color parameter. If this option is checked, then these settings will be used to produce colored text output. For example the \wj Words of Jesus\wj* marker might specify \Color Red which will only take effect if this option is also enabled - otherwise all text will appear in black.

**Explanation:**

Prints colours that are set in the styles, for example red letters for the words of Jesus, or coloured headings. When it is not ticked, all text is black. Check with your printer whether colour printing is possible and what it costs.

*(Internal ID: `c_colorfonts` · Config key: `document/ifcolorfonts`)*

#### Script for Numbers

- **Where:** Fonts+Script tab › Font Configuration
- **Type:** Link
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> To change the script for numbers, click here to locate the Digit Mapping setting at the end of the Font selection dialog.

**Explanation:**

A shortcut. It opens the **Pick a Font** dialog for the Regular font and highlights **Digit mapping**.

*(Internal ID: `lb_NumberScript`)*

### Fonts+Script tab › Use Fallback Font

#### Find Missing Characters

- **Where:** Fonts+Script tab › Use Fallback Font
- **Type:** Button
- **Description:** Find Missing Characters button
- **View level:** Default and Full views
- **Only available when:** “Use Fallback Font” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> If the primary font is missing any characters (special punctuation, quotes or glossary markers), then these can be listed here, and handled using the Font specified below.
>
> It is recommended that you select as many scripture books as available before using this tool to find missing characters.
>
> Note that the following characters are reserved and are ignored by the Fallback font functionality:  
>            \u2018 \u2019 \u201c \u201d * # %

**Explanation:**

Checks all the characters in the selected books against the Regular font and lists any that are missing. Digits and markers are not checked. If characters are missing, **Use Fallback Font** is ticked; if not, PTXprint tells you a fallback font is not needed and unticks it. Hover over the list afterwards to see the character codes.

*(Internal ID: `btn_findMissingChars`)*

#### Select Font...

- **Where:** Fonts+Script tab › Use Fallback Font
- **Type:** Button
- **Description:** Select font to display missing characters
- **View level:** Default and Full views
- **Only available when:** “Use Fallback Font” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click to select a font to be used as a substitute or "fallback" for the characters listed above which are not in the Regular font.
>
> Select a font to be used as a substitute or "fallback" for the characters listed above which are not in the Regular font.
>
> Note that if the label text is RED, it means that the font currently selected doesn't have all the missing characters either, so it is wise to choose another font.

**Explanation:**

The fallback font, used only for the characters in the list. Choose a font that contains all of them. If the label is red, it does not contain them all. It must be a different font from the Regular font.

*(Internal ID: `bl_fontExtraR` · Config key: `document/fontextraregular`)*

#### Missing Characters

- **Where:** Fonts+Script tab › Use Fallback Font
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Use Fallback Font” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> First use the button (on the left) to find any characters missing from the primary font. You may add to this list if needed. Use spaces between items. Note that you can also use \u0ABC codes to enter hard-to-type characters.

**Explanation:**

The characters to print with the fallback font, separated by spaces. You can add characters by hand, or type codes such as `⸤`. Quotation marks (‘ ’ “ ”) and `*`, `#`, `%` are ignored.

*(Internal ID: `t_missingChars` · Config key: `paragraph/missingchars`)*

### Fonts+Script tab

#### Use Fallback Font

- **Where:** Fonts+Script tab
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> This setting is used to prevent "tofu" boxes [] in the printed text. If the primary font is missing any special characters (for example curly quotes), then an alternative "fallback" font can be used to ensure that they are displayed properly.

**Explanation:**

Turns the fallback font on. Then use **Find Missing Characters** and choose a fallback font. It is ticked or unticked automatically by **Find Missing Characters**.

*(Internal ID: `c_useFallbackFont` · Config key: `paragraph/ifusefallback`)*

### Fonts+Script tab › Hyphenation

#### Hyphenate

- **Where:** Fonts+Script tab › Hyphenation
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> To hyphenate properly you need to first create a Hyphenation List using the 'Import List...' button. This will create a XeTeX hyphenation list from the hyphenation list in Paratext.
>
> Note that for Hyphenation to work properly, the Spacing Adjustments 'Between Letters' option needs to be disabled.

**Explanation:**

Turns hyphenation on, using the list created with **Import List...** (create the list first). Ticking it unticks **Between Letters** spacing. When it is not ticked, PTXprint does not hyphenate at all.

*(Internal ID: `c_hyphenate` · Config key: `paragraph/ifhyphenate`, `paragraph/ifnothyphenate`)*

#### Import List...

- **Where:** Fonts+Script tab › Hyphenation
- **Type:** Button
- **Description:** Create Hyphenation List
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Click this button to generate a hyphenation list that can be used by XeTeX to optimize hyphenation. This will read Paratext's HyphenatedWords.txt list and create a TeX hyphen list for this language.

**Explanation:**

Opens the **Create Hyphenation List** dialog. PTXprint reads the hyphenation list of your Paratext project and makes its own list from it. Do this again when the Paratext list changes.

*(Internal ID: `btn_generateHyphenationList`)*

#### Omit '-'Hyphen

- **Where:** Fonts+Script tab › Hyphenation
- **Type:** Checkbox (not ticked by default)
- **Description:** Omit hyphen from hyphenated words
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Some scripts use hyphenation to break long words onto the next line, BUT don't need to display the actual '-' character. If this option is checked, then "hyphens" will be invisible.

**Explanation:**

Makes the hyphen at a line break invisible. Use it for scripts that break words across lines without showing a hyphen.

*(Internal ID: `c_omitHyphen` · Config key: `paragraph/ifomithyphen`)*

#### Make Hyphens Non-Breaking

- **Where:** Fonts+Script tab › Hyphenation
- **Type:** Checkbox (not ticked by default)
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Enable this option to ensure that word-medial hyphens within the text never break across two lines.
>
> By default, lines may break at word-medial hyphens.
>
> If enabled, lines will not break at these hyphens.

**Explanation:**

Uses non-breaking hyphens, so that lines are not broken at hyphens that are already in the text. Create the hyphenation list again after changing this, because the list is made with the chosen kind of hyphen.

*(Internal ID: `c_nonBreakingHyphens` · Config key: `paragraph/ifnbhyphens`)*

### Fonts+Script tab › Spacing Adjustments

#### Between Words

- **Where:** Fonts+Script tab › Spacing Adjustments
- **Type:** Checkbox (ticked by default)
- **Description:** Spacing Between Words
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> The horizontal distance that the space character can use between words is adjustable - and allows a greater degree of flexibility when trying to shrink or grow paragrahs when balancing pages.

**Explanation:**

Lets PTXprint use the **Min/Shrink** and **Max/Stretch** values for the spaces between words. When unticked, standard values are used.

*(Internal ID: `c_spacing` · Config key: `document/ifspacing`)*

#### Between Letters

- **Where:** Fonts+Script tab › Spacing Adjustments
- **Type:** Checkbox (ticked by default)
- **Description:** Spacing Between Letters
- **View level:** Default and Full views
- **Greyed out when:** “Interlinear  &  Code”, “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Enabling letter spacing allows the spaces between characters to be adjusted (usually by a very small percentage). This might help alleviate space problems. Values are in percentage of the text point size and get used everywhere.
>
> Warning: Only use this if really needed! In some cases, enabling this setting will prevent hyphenation from working at all. In other cases it can make the text look very ugly.
>
> Note that if this option is disabled, then it is due to the Interlinear option being set on the Advanced page. These two settings are mutually exclusive.
>
> Letter spacing is also not used if 'Contextual Spaces' is set for the Regular font.

**Explanation:**

Lets PTXprint add or remove a tiny amount of space between letters to help justify lines. Use it only when needed. It stops hyphenation from working well, so PTXprint unticks it when you tick **Hyphenate**. It is greyed out when **Interlinear & Code** is ticked on the **Advanced** tab.

*(Internal ID: `c_letterSpacing` · Config key: `document/ifletter`, `document/letterspace`)*

#### Min/Shrink

- **Where:** Fonts+Script tab › Spacing Adjustments
- **Type:** Number box
- **Description:** Spacing Between Words (Min/Shrink)
- **View level:** Default and Full views
- **Values:** from 10 to 200, default 50
- **Only available when:** “Between Words” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> When justifying paragraphs, and especially when trying to shrink or grow a paragraph to take fewer or more lines, the horizontal distance that a space uses can be adjusted - allowing the text to shrink or grow. Lower values will enable a 'tighter' text and make it more flexible, but keep the readers in mind - and their need to distinguish word-breaks with ease. This value is a % percentage of a normal space width. TeX's default value is 66%.
>
> Minimum size % that a space can shrink to when necessary.

**Explanation:**

The smallest a space between words may become, as a percentage of a normal space. Lower values let more text fit on a line, but words may become hard to tell apart. Values of about 50–80 are common.

*(Internal ID: `s_minSpace` · Config key: `document/spaceshrink`)*

#### Max/Stretch

- **Where:** Fonts+Script tab › Spacing Adjustments
- **Type:** Number box
- **Description:** Spacing Between Words (Max/Stretch)
- **View level:** Default and Full views
- **Values:** from 50 to 999, default 200
- **Only available when:** “Between Words” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> When justifying paragraphs, and especially when trying to shrink or grow a paragraph to take fewer or more lines, the horizontal distance that a space uses can be adjusted - allowing the text to shrink or grow. Larger values will enable a 'looser' text and make it more flexible to grow, but be careful to avoid 'rivers' or white space in paragraphs. This value is a % percentage of a normal space width. TeX's default value is 150%.
>
> Maximum size % that a space can grow to when necessary.

**Explanation:**

The largest a space between words may become, as a percentage of a normal space. Higher values let lines stretch more, but can leave big gaps. Values of about 150–200 are common.

*(Internal ID: `s_maxSpace` · Config key: `document/spacestretch`)*

#### Spacing Between Letters (Min/Shrink)

- **Where:** Fonts+Script tab › Spacing Adjustments
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** default 2
- **Only available when:** “Between Letters” is selected
- **Greyed out when:** “Interlinear  &  Code”, “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Values are in percentage of the text point size.

**Explanation:**

How much the space between letters may shrink, as a percentage of the font size. Keep it small (a few percent at most). Only active when **Between Letters** is ticked.

*(Internal ID: `s_letterShrink` · Config key: `document/lettershrink`)*

#### Spacing Between Letters (Max/Stretch)

- **Where:** Fonts+Script tab › Spacing Adjustments
- **Type:** Number box
- **View level:** Default and Full views
- **Values:** default 0.5
- **Only available when:** “Between Letters” is selected
- **Greyed out when:** “Interlinear  &  Code”, “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Values are in percentage of the text point size.

**Explanation:**

How much the space between letters may grow, as a percentage of the font size. Keep it small. Only active when **Between Letters** is ticked.

*(Internal ID: `s_letterStretch` · Config key: `document/letterstretch`)*

### Fonts+Script tab › Writing System

#### Text Flow Direction

- **Where:** Fonts+Script tab › Writing System
- **Type:** Drop-down list
- **Description:** Text direction (Right-to-left RTL etc)
- **View level:** Basic, Default and Full views
- **Choices:** Left-to-Right; Right-to-Left; Top-to-Bottom (and Left-to-Right)
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Select the direction for the text to flow. Note that the option for "Top to Bottom" lays out the vertical lines left to right.

**Explanation:**

The direction of the text. Choose **Right-to-Left** for Arabic, Hebrew and similar scripts; this also ticks **RTL Book Binding**. **Top-to-Bottom** is for vertical text. Changing this changes the whole layout.

*(Internal ID: `fcb_textDirection` · Config key: `document/ifrtl`, `document/toptobottom`)*

#### Text Script

- **Where:** Fonts+Script tab › Writing System
- **Type:** Drop-down list
- **View level:** Basic, Default and Full views
- **Choices:** Latn
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Choose the script of the text. It is used for font shaping, and PTXprint provides additional typesetting functionality for some scripts:  
> Arabic, Myanmar, Thai, Lao, Tai Tham, New Tai Lue, Bengali, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, and Chinese (Han).
>
> If set to "Default", PTXprint tries to detect the script when the project is opened.

**Explanation:**

The script (writing system) of the text. It tells the font which shaping rules to use and switches on PTXprint's extra processing for some scripts (for example `/` as a word-break mark in Thai, Lao, Myanmar, Tai Tham and New Tai Lue). If it is **Default** when a project is opened, PTXprint tries to detect the script. Changing it may also change **Digit mapping** and **Specify Line Break Locale**.

*(Internal ID: `fcb_script` · Config key: `document/script`)*

#### Additional Script Settings...

- **Where:** Fonts+Script tab › Writing System
- **Type:** Button
- **View level:** Basic, Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> A small number of complex scripts (such as Myanmar, Indic, Arabic & Han) have additional options which can be set individually.

**Explanation:**

Opens extra options for the chosen script. It is only active for scripts that have options: Myanmar, Malayalam, Tamil, Sinhala, Telugu, Kannada, Oriya, Arabic, and Han (Simplified and Traditional).

*(Internal ID: `btn_scrsettings`)*

#### Specify Line Break Locale

- **Where:** Fonts+Script tab › Writing System
- **Type:** Checkbox (not ticked by default)
- **Description:** Enable Line Break Locale
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Some languages that use complex scripts need dictionary support for line breaking. Note that the dictionary used will be LWC-specific. For example, zh for Chinese, ko for Korean, etc. Note that Graphite fonts can also have line breaking rules which can be enabled by using the gr locale.

**Explanation:**

Tick this for scripts that do not put spaces between words, so PTXprint can use a dictionary to find where lines may break. Then type the code in the box. It is ticked automatically when you choose a Han, Japanese or Korean script.

*(Internal ID: `c_linebreakon` · Config key: `document/iflinebreakon`)*

#### Set Line Break Locale

- **Where:** Fonts+Script tab › Writing System
- **Type:** Text box
- **View level:** Default and Full views
- **Only available when:** “Specify Line Break Locale” is selected
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Language code for dictionary-based line breaking (for scripts without spaces between words):  
> ja = Japanese km = Khmer ko = Korean my = Myanmar th = Thai zh = Chinese  
>    OR gr = Graphite

**Explanation:**

The code of the line-break dictionary to use: `th`, `km`, `my`, `zh`, `ja` or `ko`, or `gr` to use the line-breaking rules built into a Graphite font. It is greyed out until **Specify Line Break Locale** is ticked.

*(Internal ID: `t_linebreaklocale` · Config key: `document/linebreaklocale`)*

#### RTL Book Binding

- **Where:** Fonts+Script tab › Writing System
- **Type:** Checkbox (not ticked by default)
- **Description:** Set the binding to Right (for RTL publications)
- **View level:** Default and Full views
- **Greyed out when:** “Lock UI Layout Settings” is ticked

**Tooltip (the text shown when you hover the mouse over it):**

> Enable this for Right-to-Left publications (so that the book is bound on the right hand side).

**Explanation:**

Makes the book bind on the right, as right-to-left books do. This affects where the binding gutter goes, how PDF viewers show the pages, and the cover. It is ticked automatically when you choose **Right-to-Left** text direction.

*(Internal ID: `c_RTLbookBinding` · Config key: `cover/rtlbookbinding`)*
