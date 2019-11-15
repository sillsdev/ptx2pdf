import regex

class FancyIntro():
    _regexbits = [(r'\\io2 ', r'\\io1 \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0'), # Temporary fix so that the special Intro Outline table doesn't break
               (r'(\\iot .+?)\r\n', r'\1\r\n\iotable\r\n\makedigitsother\r\n\catcode`{=1\r\n\catcode`}=2\r\n\makedigitsother\r\n\catcode`{=1\r\n\catcode`}=2'),
               (r'\\io1 ', r'\iotableleader{'),
               (r' \\ior ', r'}{'),
               (r' \\ior\*', r'}'),
               (r'\\c 1\r\n', r'\catcode`{=11 \catcode`}=11\r\n\makedigitsletters\r\n\c 1\r\n')] # Assumed no other markers is between last \io1 line and \c 1
    regexes = [(None, regex.compile(r[0], flags=regex.S), r[1]) for r in _regexbits]

    styleInfo = r"""
\Marker iotable
\Name iotable - Introduction - Outline Table
\Description Introduction outline text in a table format
\OccursUnder id
\Rank 6
\TextType Other
\TextProperties paragraph publishable vernacular level_1
\StyleType paragraph
\FontSize 12
\LeftMargin 0
\FirstLineIndent .125
"""
# 1/8 inch first line indent

    texCode = r"""
% Enable commands with digits in them to be processed
\catcode`@=11
\def\makedigitsother{\m@kedigitsother}
\def\makedigitsletters{\m@kedigitsletters}
\catcode `@=12
% Usage:
% This is the macro to use in the source text for placing
% the introduction text into a table-like format.
%   \iotableleader{First column text}{Second column text}
\def\iotableleader#1#2{#1\leaders\hbox to 0.8em{\hss.\hss}\hfill#2\par}%
"""
