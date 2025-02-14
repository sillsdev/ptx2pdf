# ztruetext

## Summary
Content to use if a test was positive
## Examples
```tex

\zifvarset|var="recording"\*
\ztruetext
\is2 Audio recordings available!
\ip Audio recordings are available at \zvar|recording\*
\ztruetext*

```
## Description
This appears like a character style, but in fact it can swallow entire paragraphs or sidebars. All content inside vanishes if the test results in a false value. Nesting is not possible.

## See also

* Documentation on [Conditional text](conditional.md)
* [zifvarset](zifvarset.md)
* [zifhook](zifhook.md)

