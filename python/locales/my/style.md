Audience: Bible translators and typesetters in Myanmar who already know common English computing words (font, margin, PDF, file). The Burmese is there to help them read the screen faster, not to be a literary translation.

- Language: standard modern Burmese in Unicode (never Zawgyi), as used in current Burmese software and websites. Simple, clear wording; avoid literary or archaic forms.
- Keep English computing words that Burmese users actually say, written in Burmese script where that is usual: ဖောင့် (font), ဖိုင် (file), ဖိုင်တွဲ (folder), တက်ဘ် (tab). Use a Burmese word where it is the normal one (ဆက်တင်များ for settings, ရွေးချယ်ပါ for select).
- Register: polite. Instructions end with ပါ (ရွေးချယ်ပါ, ထည့်သွင်းပါ, နှိပ်ပါ). Labels and buttons: short noun or verb phrases without sentence-final particles. Tooltips and messages: complete, natural sentences ending with ။ where a full stop belongs.
- Translate the meaning, never word by word (see the term notes); if a literal rendering reads as nonsense, rethink it.
- Numbers stay in the digits of the English (do not convert them to Burmese digits), so that values and placeholders keep working.
- Do not translate product and technical names: Paratext, PTXprint, USFM, FRT, XeTeX, ptx2pdf, and any code such as \k or \w. Keep PDF and similar acronyms in Latin script. Strong's stays a name (keep "Strong's").
- Bible terms follow the Judson Burmese Bible: သမ္မာကျမ်းစာ (Bible), ကျမ်း (book), အခန်းကြီး (chapter), အခန်းငယ် (verse), အောက်ခြေမှတ်စု (footnote), ကိုးကားချက် (cross-reference).
- Typesetting terms: စာမျက်နှာ (page), အနားသတ် / မာဂျင် (margin), ဘောင် (border), ခေါင်းစီး (header), အောက်ခြေစာ (footer), ကော်လံ (column), စာအုပ်ကျော (spine), မ / စုံ စာမျက်နှာ (odd/even pages).
- Strings containing markup such as <span ...> or <b>: translate only the visible words; leave the tags and attributes exactly as they are.
- Every translation must keep each placeholder ({}, %s, %(name)s), tag and blank-line paragraph break exactly as in the English. Never merge two paragraphs into one.
