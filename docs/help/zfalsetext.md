# zfalsetext

## Summary
Content to use if a test was negative
## Examples
```tex

\zifvarset|var="recording"\*
\zfalsetext
\is2 Audio recording website
\ip No audio recording exists at the time of publication but
 keep checking on https://our.web.site for news.
\zfalsetext*

```
## Description
This appears like a character style, but in fact it can swallow entire paragraphs or sidebars. All content inside vanishes if the test results in a true value. Nesting is not possible.

## See also

* Documentation on [Conditional text](conditional.md)
* [zifvarset](zifvarset.md)
* [zifhook](zifhook.md)
