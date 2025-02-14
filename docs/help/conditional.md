# Conditional content

There are (so far) two tests which set up the pseudo-character styles
`\ztruetext ...\ztruetext*`  and `\falsetext...\zfalsetext*`
Note that these are **not** true character styles, and they cannot be nested.
All content (including paragraph markers, sidebars, etc) within them is
swallowed as a TeX parameter and if the result of the test was true or false
(as appropriate) it is re-read and re-processed.
Because of how they operate, no attempt should be made to use them inside hooks
or other macros.

#### Tests for conditional text.
`\zifhooks|marker` Sets up the conditional text code depending if there have
been hooks set up for a given marker. This can be useful if markers for `\add`
or `\sls` are inserting code via hooks.

`\zifvarset|var="varname"\*`   Sets up the conditional text code depending if the zvar  
`varname` has been set. The optional parameter `emptyok="T"` determines whether
an empty variable should be treated as unset (the default, if emptyok is not
specified) or as set (any value for emptyok except "F"). i.e., an empty variable will 
give the following results:
* `\zifvarset|var="varname"\*`   -> false
* `\zifvarset|var="varname" emptyok="F"\*`   -> false
* `\zifvarset|var="varname" emptyok="t"\*`   -> true
* `\zifvarset|var="varname" emptyok=""\*`   -> true
* `\zifvarset|var="varname" emptyok="rabbit"\*`   -> true

