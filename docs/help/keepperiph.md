# KeepPeriph
## Summary
Remember the contents of the named periphery 
## Examples
```
\KeepPeriph{logobit}
```
## Description
Normally, stored pheriphery materials are single-use. I.e. once used they are discarded. This setting (for use in `ptxprint-mods.tex`, etc) sets a flag that instructs the code to not discard the content of the named periphery, so it can be reused.

If the content of the periphery contains one of the low-level command `\keeptriggerfalse` or `\keeptriggertrue`, then these take priority over this setting.

## See also
* [Peripheral matter](../documentation/README.md)