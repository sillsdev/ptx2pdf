# Box runs
## The primary issue.
Certain styling options (underline, background colour) need the text to *only*
consist of boxes and glue.  Items such as inserts (notes), marks (verse
numbers), or write nodes on will destroy such a run of box-glue-box-glue-etc,
and prevent the styling from functioning correctly.

Therefore *any macro* wanting to insert such interrupting nodes should end the run if one 
is in progress, insert the node, and restart the run of boxes (with appropriate set-up code).

This is easy enough as long as there's no nesting.

## The nesting issue.
Nested char styles  mean that macros that do not themselves require box-run protection may be contained
within box-runs. Also, all char styles start a new group.

* Items starting a group (all char styles!) should (locally) set
 `\box@runfalse` unless they are actually starting a boxrun.
* Items that set box@runtrue must also increment the nesting counter \active@box@runs
* Items setting box@runtrue should set start@box@run toklist which in turn should and end@box@run toklists via a temp toklist
* Other items, such as raise, which are insert-tolerant, may also use start@box@run and end@box@run for consistency.
* To cope with nesting, tear-down code must preserve values of start@box@run
and end@box@run and reapply them.

## Example code that does this.
### Startup:
```
\tmptox := {}
if has underline {\temptrue, addtotmptox{\box@runtrue\addtoendrun{\applyunderline{0}} } }
if has background {\temptrue, addtotmptox{\box@runtrue\addtoendrun{\applybackground{colour}{0}} } }
if has raise (\temptrue,addtotmptox{\addtoendrun{raisebox{distance}{0})
\iftemp 
 \setbox0=\hbox\bgroup
   \boxrunfalse
   \end@box@run := {}
   \start@box@run := {\tmptox}
   \the\start@box@run
   \x@\aftergroup\x@{\the\end@box@run}
   \ifbox@run  increment active@box@runs \fi
```

### At insert, etc.
```
  \global\let\inuse@box@runs\active@box@runs
  \loop\ifnum \active@box@runs >0
    \x@\def\csname start@box@run-\currentgrouplevel\x@\endcsname\x@{\the\start@box@run}
    \egroup % no need to decrement active@box@runs, as grouping handles that.
  \repeat

	[Insert non-box node]
  \loop\ifnum \active@box@runs < \inuse@box@runs
    \setbox0=\hbox\bgroup
      \boxrunfalse
      \end@box@run := {}
      \start@box@run := \x@{\csname start@box@run-\currentgrouplevel ... }
      \the\start@box@run
      \x@\aftergroup\x@{\the\end@box@run}
      \ifbox@run  increment active@box@runs \fi
  \repeat
  (reset font).
```

Potential issues:
  Above forgets about groupings that are not hboxes. 


### Alternative  approach:
 Close items on the style stack until active@box@runs=0. Restore stylestack afterwards.

Potential issues:
 Wastes additional CPU cycles.
 possible undesired side-effects from hook code. (e.g. start/end markers for `\add`)


