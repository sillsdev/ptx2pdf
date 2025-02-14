# zcolsync
## Summary
A manual synchronisation point for diglots / polyglots synchronsied with the 'scores' method.
## Examples
```
\zcolsync|id\* % This position should be synchronised with id on the other column(s)
\zcolsync|v23a\* % This position should be synchronised as if it were verse 23a.
\zcolsync|p3\* % This position should synchronised as if it were paragraph 3.

```
## Description
This milestone produces no output, but as it has a textproperty of `diglotsync` the attribute is interpreted by the diglot / polyglot merging 
code, to override the current position.

## See also
* [Diglot documentation](../documentation/diglot.md)


