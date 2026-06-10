# Results of timing tests
## Motivation
There are some things that we might consider optimisations which actually,  in
the world of TeX, are counter-productive. 
This document is an attempt to get some real results and see how much the affect things.

## Max of 2 or 3 numbers

* This test avoids assigning to any variable, at the cost of more \dimexprs:
\def\max#1#2{\ifdim\dimexpr #1 \relax>\dimexpr #2\relax \dimexpr #1\relax \else \dimexpr #2\relax; \fi}

* maxb uses 2 temporary vars to avoid repeating \dimexpr
\def\maxb#1#2#3{\dimen1=\dimexpr #2 \relax \dimen2=\dimexpr #3\relax #1=\ifdim\dimen1>\dimen2 \dimen1 \else \dimen2 \fi}

* maxc does a 3 way max, using 3 temporary variables.
\def\maxc#1#2#3#4{\dimen1=\dimexpr #2 \relax \dimen2=\dimexpr #3\relax \dimen3=\dimexpr #4\relax #1=\ifdim\dimen1>\dimen2 \dimen1 \else \dimen2 \fi\ifdim #1<\dimen3 #1=\dimen3\fi}

* maxd uses a more complex if structure to avoid assigning to the variable twice.
\def\maxd#1#2#3#4{\dimen1=\dimexpr #2 \relax \dimen2=\dimexpr #3\relax \dimen3=\dimexpr #4\relax #1=\ifdim\dimen1>\dimen2 \ifdim \dimen3>\dimen1 \dimen3 \else \dimen1 \fi \else \ifdim \dimen3>\dimen2 \dimen3 \else\dimen2\fi\fi}

After (column) runs, each with 30000 loops, these results were obtained for the different tests.
XeTeX:
maxa 61 148.305ms
maxb 61 122.123ms
maxc 21 151.03ms
maxd 21 154.049ms
maxe 40 149.188ms
maxf 40 141.495ms


It can be seen that the multiple `\dimexpr` calls of maxa are not efficient, and surprisingly, the cost of parsing the if structure of maxd outweighs the re-assignment and re-testing in maxc.
This led to the ideas tested in \maxe: is it easier for TeX to cope with the pragma `\dimen0 = \if TEST result \fi`  or is the (easier to read as a human) `\if TEST \dimen0= result\fi`

\def\maxe#1#2#3#4{\dimen1=\dimexpr #2 \relax \dimen2=\dimexpr #3\relax \dimen3=\dimexpr #4\relax \ifdim\dimen1>\dimen2 #1=\dimen1 \else #1=\dimen2 \fi\ifdim #1<\dimen3 #1=\dimen3\fi}

Another question that arose was  how hard TeX found it to parse if...else..fi  rather than simple if statements with repeated assignments:

\def\maxf#1#2#3#4{#1=\dimexpr #2 \relax \dimen2=\dimexpr #3\relax \dimen3=\dimexpr #4\relax \ifdim #1<\dimen2 #1=\dimen2 \fi\ifdim #1<\dimen3 #1=\dimen3 \fi}
This result was entirely surprising to me. It can be seen, comparing `\maxf` and `\maxc  that the extra `\ifdim ... #1=\dimen2\fi` costs about 20ms / 30000. Other tests indicate the following 
time-costs, relative to the above baselines:

\def\a{B} 4ms more than \dimen1=\dimen2
\ifx\a\relax ... \fi 7ms more than \ifdim\dimen1>\dimen2
\ifdim\dimen1=10pt ... \fi 24ms  more than \ifdim\dimen1>\dimen2, maybe due to the need to interpret the string? The result seems strange, anyway.


## Is that just XeTeX?

Results of this simple case with luaTeX are as follows:

maxa 40 154.318ms
maxb 40 126.26ms
maxc 20 163.528ms
maxd 20 168.237ms
maxe 20 156.676ms
maxf 20 149.505ms

## col@do or crafted expression?
When calculating the height of a block with multiple columns, we have the
general-purpose \each@col tool. How does using that to determine the max of A,
L and R, compared to generating an explicit  customised macro with \each@col
once and using that? 

```
\def\functionB#1#2\E{\tmpdim=\dimexpr \ht\csname #1box\endcsname \let\col@do\@functionB \x@\each@col#2\E}
\def\@functionB#1{\dimen0=\dimexpr \ht\csname #1box\endcsname+\dp\csname #1box\endcsname\relax\ifdim\dimen0>\tmpdim \tmpdim=\dimen0 \fi}

\def\genfunction#1#2\E{
  \edef\tmp{\tmpdim=\dimexpr \ht\csname #1box\endcsname+\dp\csname #1box\endcsname\relax}%
  \x@\fntoks\x@{\tmp}%
  \let\col@do\@genfunction
  \x@\each@col#2\E
  \x@\def\x@\function\x@{\the\fntoks}%
}

\def\@genfunction#1{%
  \edef\tmp{\dimen0=\dimexpr \ht\csname #1box\endcsname+\dp\csname #1box\endcsname\relax}%
  \x@\x@\x@\fntoks\x@\x@\x@{\x@\the\x@\fntoks\tmp \ifdim\dimen0>\tmpdim \tmpdim=\dimen0 \fi}%
}
```
The \edef expands the `#1` macro and generates the \csnames, reducing execution
time. However, earlier versions of the above showed that (obviously, in
retrospect) an `\if` cannot be included in `\edef`ed macro, or that is also expanded.

Results are as below (for 5000 loops):

col@do 20 18.309ms
generating 20 32.6347ms
explicit 20 9.20563ms

In formulating the  
Clearly, the cost of generating the custom macro, and the potential for error if the 
function is not generated properly means that extra testing is needed and it should not be
used for every operation, but for the type of repeated calculations
used in itterative optimisation suggest the approach shows it has the potential of doubling speed.
For the case here, the benefit starts to occur after N times where 9.2N+32.6<18.3N  -> N>32.6/(18.3-9.2) = 3.4 - i.e. only 4 iterations.





