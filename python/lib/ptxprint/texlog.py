import os, re, datetime

# I = Info/Ignore
# W = Warning
# E = Error
# L --- too long to match (needs to be shortened to match within 80 chars)
# x     The line below each "L" has a shorter version which should match.

messages = [
    ("W", r"Reached end of book without finding \\esbe\."),
    ("W", r"Unable to find label for .+? Re-run or correct typo at/near .+"),
    ("W", r"Unable to find reference for .+? Re-run or correct typo at/near .+"),
    ("W", r"set@ht passed null value"),
    ("W", r"dimension .+? does not exist"),
    ("W", r"\*\* Probable typo: if.+? does not exist in side-specific switching"),
    ("W", r"unknown style type .+"),
  # ("L", r"! ERROR! Impropper state; '.+?' should be 'L' 'R' or some other defined column\. Maybe there was output before columns were set up?"),
    ("E", r"! ERROR! Impropper state; '.+?' should be 'L' 'R' or some other defined column\."),
  # ("L", r"@pgfornamentDim not defined\. Probably the path from the TEXINPUTS environment variable does not include \\pgfOrnamentsObject"),
    ("L", r"@pgfornamentDim not defined\. Probably the path from the TEXINPUTS environment "),
    ("E", r"Cannot continue"),
    ("W", r"Cannot re-use undefined variable .+"),
    ("E", r"Invalid key found when parsing .+? OrnamentScaleRef : '.+?' \(given: .+?\)"),
    ("W", r"No room for data in QRcode versions till .+"),
  # ("L", r"Pagecount \(\d+\) has exceeded \\MaxPages \(\d+\)\. This probably means something has gone wrong\. \(or you should increase MaxPages or MaxPagesPerChunk \(\d+\) for this job\)"),
    ("E", r"Pagecount \(\d+\) has exceeded \\MaxPages \(\d+\)\. This probably means something"),
    ("W", r'Unknown picture size \".+?\", expected \"col\", \"span\", \"width\", \"page\" or \"full\"'),
    ("L", r"polyglotcolumn must be followed by a sensible argument\. '.+?' Hasn't been specified as a polyglot column \(with newPolyglotCol\), before any USFM files are read\."),
  # ("L", r"polyglotcolumn must be followed by a sensible argument\. '.+?' Hasn't been specified as a polyglot column \(with newPolyglotCol\), before any USFM files are read\."),
    ("E", r"zglot must be followed by a sensible argument\. '.+?' Hasn't been specified"),
    ("W", r"Table column overflow, reducing resolution"),
  # ("L", r"\*\* .+? specification of .+? \(at \d+:\d+\) leaves .+? for text\. That's probably not enough\."),
    ("W", r"\*\* .+? specification of .+? \(at \d+:\d+\) leaves .+? for text\."),
    ("W", r"Did not use all pictures in list\. Waiting for .+"),
    ("W", r'Paratext stylesheet \".+?\" not found'),
    ("W", r"Abandoning ship with nothing on the page"),
    ("E", r"\*\*\* .+? text called from inside footnote?!?"),
    ("W", r"Warning! periph is set nonpublishable \(hidden\) in general\. This may be a mistake!"),
    ("E", r"INTERNAL ERROR! Foonotes/figures shouldn't be held, or they'll get lost!"),
  # ("L", r"Warning: Using xy or XY as part of a 2 part .+? OrnamentScaleRef makes no sense \(given: .+?\)"),
    ("W", r"Warning: Using xy or XY as part of a 2 part .+? OrnamentScaleRef makes"),
    ("W", r"\*\*\* Figures have changed\. It may be necessary to re-run the job"),
    ("E", r"Placement for image .+? \(at .+?\) could not be understood\. Image Lost!"),
    ("E", r"Number of bits does not correspond to the computed value"),
    ("W", r"Image crop not supported"),
    ("W", r"Expected rotate=.+? or similar in definition of picture .+"),
    ("W", r"Eh? .+? called for .+? and empty parameter"),
    ("W", r'Thumb tab contents \".+?\" too wide \(.+?\) for tab height \(.+?\)'),
    ("W", r'Thumb tab contents \".+?\" too wide for tab width'),
  # ("L", r"Error in stylsheet: Stylesheet changed category from '.+?' to '.+?\'\. Resetting to '.+?'"),
    ("E", r"Error in stylsheet: Stylesheet changed category from '.+?' to '.+?\'\."),
    ("W", r"polyglotcolumn may not be called with an empty argument"),
    ("E", r"No side defined for foreground image in sidebar class '.+?\. Assuming outer\."),
    ("E", r"Invalid syntax parsing .+? \(given: .+?\)"),
    ("W", r"n\.b\. You can load optional plugins with \(some of\) .+? or .+?"),
    ("W", r"Setting drop-cap size to .+"),
    ("W", r"! Cover sidebar '.+?' is currently '.+?\. It must be Fcf or similar"),
    ("E", r'! Parent style \".+?\" referenced for borders by \".+?  does not exist!'),
    ("W", r"! Unknown borderstyle '.+?\. Known styles: .+?"),
    ("W", r'! zornament milestone must have a valid pattern=\"\.\.\.\" set'),
    ("W", r"!! Unknown cutout position .+?, picture misplaced"),
    ("E", r"!!! EEK\. Internal error detected\. .+? met during trial, somewhere near .+?"),
    ("E", r".+? is already a diglot column\. You can only define it as one once!"),
  # ("L", r"\*\*  WARNING: something has changed the text width in the sidebar to be larger than the value calculated earlier"),
    ("W", r"\*\*  WARNING: something has changed the text width in the sidebar to be larger"),
  # ("L", r"\*\* Only .+? pictures were used out of .+? defined\. Piclist may have errors or perhaps contain references for other books\. Unused references: .+"),
    ("W", r"\*\* Only .+? pictures were used out of .+? defined\. Piclist may have errors"),
  # ("L", r"\*\*\* Figure .+? on page .+?, but previously seen on .+?\. Work-around is to move the anchor to a different verse or alter the size/placement\."),
    ("W", r"\*\*\* Figure .+? on page .+?, but previously seen on .+?\. Work-around is to"),
    ("E", r"\*\*\* Picture .+? wide in .+? space\.\s+Did you mean to use col, instead of span?"),
  # ("L", r"\*\*\* WARNING: Sidebar or colophon might not print on page \d+\. \(.+? high, and  page is .+?\)\."),
    ("W", r"\*\*\* WARNING: Sidebar or colophon might not print on page \d+\. \(.+? high,"),
  # ("L", r"\+\+\+RARE CONDITION MET\. Maybe doing wrong thing on page \d+, debug posn .+?\. Toggle with NoMergeReflow\ifNoMergeReflow (false|true)"),
    ("E", r"\+\+\+RARE CONDITION MET\. Maybe doing wrong thing on page \d+, debug posn .+?\."),
    ("W", r"\+\+\+Uh oh\. Didn't expect this\. Now what? Discards .+? > topskip .+"),
    ("E", r"Cannot define zero-size ornament .+? properly"),
    ("W", r"Column deltas for book: .+"),
    ("E", r"Could not interpret position .+? for .+?:.+"),
    ("E", r"Could not parse Border .+"),
    ("E", r"Could not understand / interpret position .+? for .+?:.+"),
    ("W", r"Defining .+? as an additional polyglot column\."),
    ("E", r"Double underline  for .+"),
  # ("L", r"EEK! Still in trial! on page \d+, somewhere near .+?\. Expect synchronisation and text loss"),
    ("E", r"EEK! Still in trial! on page \d+, somewhere near .+?\. Expect synchronisation"),
    ("W", r"End-milestone of class '.+?', id '.+?' partially matched one or"),
    ("W", r"Forcing page break"),
    ("E", r"MISSING IMAGE: .+? ->"),
  # ("L", r"Malformed input near .+?: periph called while there was a pending chapter number \(.+?\)"),
    ("W", r"Malformed input near .+?: periph called while there was a pending chapter"),
    ("E", r"No space for text on page!"),
    ("E", r"Not a PDF file, page=\.\.\. only supported on PDFs"),
    ("W", r"Ornamental border: unrecognised control char '.+?'"),
  # ("L", r"Paragraph font for .+? including a verse number claims it is taller \(.+?\) than baseline \(.+?\)"),
    ("W", r"Paragraph font for .+? including a verse number claims it is taller"),
    ("W", r"Polyglot: layout across .+? pages"),
    ("W", r'Reading Paratext stylesheet \".+?\" \(.+?\)\.\.\.'),
    ("W", r"Rotating spine\s(anti clockwise|clockwise)"),
    ("W", r"Setting .+? drop-cap size to .+"),
    ("W", r"Setting up column-specific values for columns: .+"),
    ("W", r"SkipMissingFigtrue: Missing figure .+? ignored\."),
    ("I", r"Special penalty .+? is .+"),
    ("W", r"Supplied scale reference for \(.+? esb\) .+? image \('.+?'\)  not recognised!"),
    ("W", r"Trying to continue by breaking rules"),
    ("E", r"UNPRINTABLE PAGE CONTENTS! Image too big? Somewhere near .+"),
    ("W", r"Unable to make outline entry for .+?, no link-id field specified"),
    ("W", r'Unexpected key .+?=.+?\. Expected key \"rotate\"'),
  # ("L", r'Unexpected value rotate=.+?\. Expected values \"edge\", \"binding\", \"odd\", or \"even\"'),
    ("W", r'Unexpected value rotate=.+?\. Expected values .+'),
    ("W", r'Unknown picture location \".+?\"'),
    ("E", r"baseline set to 0pt EEK"),
    ("W", r"pages attribute of zfillsignature must be supplied at the moment"),
    ("W", r"starting table cat:.+? .+"),
    ("W", r"unrecognised rule style '.+?' near .+"),
    ("W", r"valid options for pagenums attribute of zfillsignature are 'do' and 'no'"),
    ("W", r'converted sidebar placement \".+?\" to \".+?\" in single-column layout'),
    ("W", r"WARNING: p\..+?:.+? used in text when .+? is a footnote, not an endnote\.")]

# These (below) have not been added to the list above (yet) as they seems to require some further knowledge as to how to 'fish' for them.

# \QRdata|*MSG:any message be cerefull with spaces and other special chars so QRdata is better method|\!\def\!\QRPmsg\!{\QRcontent}%
# \errmessage{orn@usepath: #1 unrecognised}%
# Current slop: \string\setCutoutSlop{#1}{\the\numexpr -\@djustmin\relax}{\@djustmax}
# First chapter for \id@@@}\op@ninghooks{first}{c}{c+\styst@k
# IF CHECK #1 Failed. Entered at \csname checkif@#1\endcsname \space != exit at \tr@ceiflevel}\fi}
# No cover produced, as periphery missing (state: \ifcsname periphcontents=coverfront\endcsname\else No coverfront (or cover). \fi\ifcsname periphcontents=coverback\endcsname\else, No coverback \fi \ifcsname periphcontents=coverspine\endcsname\else \ifcsname periphcontents=spine\endcsname\else, No coverspine (or spine).\fi\fi)
# Unrecognised control flag '\x@\meaning\t@st' \x@\the\x@\catcode\x@`\t@st  in fontfeature definition #1[#2], processing like '+' (valid: +/-/=)
# \ch@nged\space for label #2 changed. Re-run file.
# \ifpluginjustwarn Stylesheet option '##1' requires missing \else Loading required \fi plugin: #1
# \newch@rstyle ^ found, but CharstyleExtend false. Check usage.
# barcode #1 #2 #3 #4 #5 #6
# barcodeV (\b@rheight) #1 #2 #3 #4 #5 (#6)
# diglot#1true is deprecated. The normal column switching method is to use (no)lefttext / (no)righttext or the new  polyglotcolumn and endcols macros
# lineskiplimit=\the\lineskiplimit
# ptxfile #1 \ifdigl@tinuse \ifdiglot diglot \else monoglot in diglot doc \fi\else monoglot\fi
# Would use RaiseItem if: \string\setCutoutSlop{#1}{\the\numexpr -\@accept@djmin\relax}{\@accept@djmax}

# Compile all message patterns into a single regular expression
message_regex = '|'.join(f'({pattern})' for _, pattern in messages)
# print(message_regex)

# Function to summarize issues in a log file
def summarize_log_file(log_file_path):
    # Create dictionaries to count occurrences of each category
    category_counts = {"I": 0, "W": 0, "E": 0}

    # Read the log file
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_contents = log_file.read()

    # Iterate through the messages and check for matches
    for i, (category, pattern) in enumerate(messages, start=1):
        # print(pattern)
        matches = re.finditer(pattern, log_contents)
        for match in matches:
            category_counts[category] += 1
            # print(f"{i}: Category: {category}, Matched Text: {match.group(0)}")
            if category in ["W", "E"]:
                print(f"{category}: {match.group(0)}")
    if category_counts['W'] + category_counts['E'] > 0:
        # Print the summary line at the end of the log file
        summary_line = f"Summary: I:{category_counts['I']} W:{category_counts['W']} E:{category_counts['E']} | {log_file_path}\n"
        print(summary_line)

# Function to search for and summarize recent *ptxp.log files
def search_and_summarize_recent_logs(root_folder):
    # Calculate the date one week ago from today
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('ptxp.log'):
                log_file_path = os.path.join(foldername, filename)

                # Check the creation date of the file
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(log_file_path))

                # If the file was created within the last week, summarize its issues
                if creation_time >= one_week_ago:
                    # print(f"\n-- {log_file_path}")
                    summarize_log_file(log_file_path)

# Main program
if __name__ == "__main__":
    root_folder = r"C:\My Paratext 9 Projects"
    search_and_summarize_recent_logs(root_folder)
