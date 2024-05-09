import os, re, datetime

categories = {"I": "Info", "W": "Warning", "E": "Error"}

# Note: Multiple response values are possible - with the most likley problem first:
responses = {
    "R": "Rerun and see if that fixes it.",
    "U": "Fix usfm",
    "P": "Fix piclist or relevant figure definition",
    "Q": "In the QR code specification, try removing the vmax parameter,\n   or increase value of vmax until error goes away.",
    "A": "Fix Adjlist",
    "S": "Fix stylesheet",
    "T": "Contact programming team (TeX)",
    "Y": "Contact programming team (python)",
    "E": "Configuration environment (including ptxprint-mods.tex, file locations, etc)"
    # "F": "Use a different font which is not a Variable Font."
}

messages = [
    ("E","S", r"! Cannot redefine reserved marker .*"),
    ("E","U", r"Reached end of book without finding \\esbe\."),
    ("W","RU", r"Unable to find label for .+? Re-run or correct typo at/near .+"),
    ("W","RU", r"Unable to find reference for .+? Re-run or correct typo at/near .+"),
    ("W","T", r"set@ht passed null value"),
    ("W","T", r"dimension .+? does not exist"),
    ("W","T", r"\*\* Probable typo: if.+? does not exist in side-specific switching"),
    ("W","SY", r"\\[a-z1-9]+ unknown style type"),
    ("W","SY", r"unknown style type .+"),
    ("E","SUYT", r"! ERROR! Improper state; '.+?' should be 'L' 'R' or some other defined column\. Maybe there was output before columns were set up?"),
    ("E","EY", r"@pgfornamentDim not defined\. Probably the path from the TEXINPUTS environment variable does not include \\pgfOrnamentsObject"),
    ("E","U", r"Cannot continue"),
    ("E","US", r"Cannot re-use undefined variable .+"),
    ("E","S", r"Invalid key found when parsing .+? OrnamentScaleRef : '.+?' \(given: .+?\)"),
    ("E","UE", r"Pagecount \(\d+\) has exceeded \\MaxPages \(\d+\)\. This probably means something has gone wrong\. \(or you should increase MaxPages or MaxPagesPerChunk \(\d+\) for this job\)"),
    ("W","UP", r'Unknown picture size \".+?\", expected \"col\", \"span\", \"width\", \"page\" or \"full\"'),
    ("E","UY", r"polyglotcolumn must be followed by a sensible argument\. '.+?' Hasn't been specified as a polyglot column \(with newPolyglotCol\), before any USFM files are read\."),
    ("E","U", r"zglot must be followed by a sensible argument\. '.+?' Hasn't been specified"),
    ("I","U", r"Table column overflow, reducing resolution"),
    ("W","S", r"\*\* .+? specification of .+? \(at \d+:\d+\) leaves .+? for text\. That's probably not enough\."),
    ("W","UP", r"Did not use all pictures in list\. Waiting for .+"),
    ("W","E", r'Paratext stylesheet \".+?\" not found'),
    ("W","UT", r"Abandoning ship with nothing on the page"),
    ("E","UY", r"\*\*\* .+?text called from inside footnote?!?"),
    ("W","S", r"Warning! periph is set nonpublishable \(hidden\) in general\. This may be a mistake!"),
    ("E","T", r"INTERNAL ERROR! Foonotes/figures shouldn't be held, or they'll get lost!"),
    ("W","S", r"Warning: Using xy or XY as part of a 2 part .+? OrnamentScaleRef makes no sense \(given: .+?\)"),
    # Quieten this noisy message as it always shows up!
    ("I","R", r"\*\*\* Figures have changed\. It may be necessary to re-run the job"),
    ("E","P", r"Placement for image .+? \(at .+?\) could not be understood\. Image Lost!"),
    ("W","P", r"Warning: No copyright statement found for: .+? on pages .+? "),
    ("E","T", r"Number of bits does not correspond to the computed value"),
    ("I","ST", r"Image crop not supported"),
    ("W","P", r"Expected rotate=.+? or similar in definition of picture .+"),
    ("W","T", r"Eh? .+? called for .+? and empty parameter"),
    ("WS","EU", r'Thumb tab contents \".+?\" too wide \(.+?\) for tab height \(.+?\)'),
    ("WS","EU", r'Thumb tab contents \".+?\" too wide for tab width'),
    ("E","S", r"Error in stylesheet: Stylesheet changed category from '.+?' to '.+?\'\. Resetting to '.+?'"),
    ("E","UY", r"polyglotcolumn may not be called with an empty argument"),
    ("W","S", r"No side defined for foreground image in sidebar class '.+?\. Assuming outer\."),
    ("E","S", r"Invalid syntax parsing .+? \(given: .+?\)"),
    ("I","", r"n\.b\. You can load optional plugins with \(some of\) .+? or .+?"),
    ("I","", r"Setting drop-cap size to .+"),
    ("W","S", r"! Cover sidebar '.+?' is currently '.+?\. It must be Fcf or similar"),
    ("E","Q", r'! No room for data in QRcode versions.+?'),
    ("W","S", r'! Parent style \".+?\" referenced for borders by \".+?  does not exist!'),
    ("W","S", r"! Unknown borderstyle '.+?\. Known styles: .+?"),
    ("E","U", r'! zornament milestone must have a valid pattern=\"\.\.\.\" set'),
    ("W","US", r"!! Unknown cutout position .+?, picture misplaced"),
    ("E","T", r"!!! EEK\. Internal error detected\. .+? met during trial, somewhere near .+?"),
    ("E","EY", r".+? is already a diglot column\. You can only define it as one once!"),
    ("W","T", r"\*\*  WARNING: something has changed the text width in the sidebar to be larger than the value calculated earlier"),
    ("I","PU", r"\*\* Only .+? pictures were used out of .+? defined\. Piclist may have errors or perhaps contain references for other books\. Unused references: .+"),
    ("W","PU", r"\*\*\* Figure .+? on page .+?, but previously seen on .+?\. Work-around is to move the anchor to a different verse or alter the size/placement\."),
    ("W","P", r"\*\*\* Picture .+? wide in .+? space\.\s+Did you mean to use col, instead of span?"),
    ("W","U", r"\*\*\* WARNING: Sidebar or colophon might not print on page \d+\. \(.+? high, and  page is .+?\)\."),
    ("E","ET", r"\+\+\+RARE CONDITION MET\. Maybe doing wrong thing on page \d+, debug posn .+?\. Toggle with NoMergeReflow.+"),
    ("W","T", r"\+\+\+Uh oh\. Didn't expect this\. Now what? Discards .+? > topskip .+"),
    ("W","ES", r"Cannot define zero-size ornament .+? properly"),
    ("I","", r"Column deltas for book: .+"),
    ("E","S", r"Could not interpret position .+? for .+?:.+"),
    ("E","SU", r"Could not parse Border .+"),
    ("E","ST", r"Could not understand / interpret position .+? for .+?:.+"),
    ("I","", r"Defining .+? as an additional polyglot column\."),
    ("I","", r"Double underline  for .+"),
    ("E","T", r"EEK! Still in trial! on page \d+, somewhere near .+?\. Expect synchronisation and text loss"),
    ("W","U", r"End-milestone of class '.+?', id '.+?' partially matched one or"),
    ("I","UP", r"Forcing page break"),
    ("W","PE", r"MISSING IMAGE: .+? ->"),
    ("E","U", r"Malformed input near .+?: periph called while there was a pending chapter number \(.+?\)"),
    ("E","PU", r"No space for text on page!"),
    ("E","P", r"Not a PDF file, page=\.\.\. only supported on PDFs"),
    ("W","SU", r"Ornamental border: unrecognised control char '.+?'"),
    ("I","S", r"Paragraph font for .+? including a verse number claims it is taller \(.+?\) than baseline \(.+?\)"),
    ("I","", r"Polyglot: layout across .+? pages"),
    ("I","", r'Reading Paratext stylesheet \".+?\" \(.+?\)\.\.\.'),
    ("I","", r"Rotating spine\s(anti clockwise|clockwise)"),
    ("I","", r"Setting .+? drop-cap size to .+"),
    ("I","", r"Setting up column-specific values for columns: .+"),
    ("I","", r"SkipMissingFigtrue: Missing figure .+? ignored\."),
    ("I","", r"Special penalty .+? is .+"),
    ("W","S", r"Supplied scale reference for \(.+? esb\) .+? image \('.+?'\)  not recognised!"),
    ("W","PU", r"Trying to continue by breaking rules"),
    ("E","PU", r"UNPRINTABLE PAGE CONTENTS! Image too big? Somewhere near .+"),
    ("W","U", r"Unable to make outline entry for .+?, no link-id field specified"),
    ("W","P", r'Unexpected key .+?=.+?\. Expected key \"rotate\"'),
    ("W","P", r'Unexpected value rotate=.+?\. Expected values \"edge\", \"binding\", \"odd\", or \"even\"'),
    ("W","P", r'Unknown picture location \".+?\"'),
    ("W","ET", r"baseline set to 0pt EEK"),
    ("W","U", r"pages attribute of zfillsignature must be supplied at the moment"),
    ("I","", r"starting table cat:.+? .+"),
    ("W","US", r"unrecognised rule style '.+?' near .+"),
    ("W","U", r"valid options for pagenums attribute of zfillsignature are 'do' and 'no'"),
    ("W","S", r'converted sidebar placement \".+?\" to \".+?\" in single-column layout'),
    ("W","A", r'\*\* WARNING: adjustlist entries should not contain space.+'),
    # ("E","F", r"xdvipdfmx:fatal: Invalid font:"),
    ("W","U", r"WARNING: p\..+?:.+? used in text when .+? is a footnote, not an endnote\.")]

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
message_regex = '|'.join(f'({pattern})' for _,_, pattern in messages)

# Function to summarize issues in a log file
def summarize_log_file(log_file_path):
    # Read the log file
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_contents = log_file.read()
    summarizeTexLog(log_contents)

# Function to summarize issues in the log text
def summarizeTexLog(logText):
    # Create dictionaries to count occurrences of each category
    category_counts = {"I": 0, "W": 0, "E": 0}
    messageSummary = []
    allmsgs = set()

    # Iterate through the messages and check for matches
    for category, response, pattern in messages:
        matches = re.finditer(pattern, logText)
        for i, match in enumerate(matches):
            category_counts[category[0]] += 1
            # print(f"{category}:{pattern}") # good for figuring out which message is causing it to crash!
            if category[0] in ["W", "E"]:
                msg = f"{categories[category[0]]}: {match.group(0)}"
                if msg in allmsgs:
                    continue
                allmsgs.add(msg)
                messageSummary.append(msg)
                if i < 1 or len(category) < 2 or 'S' not in category:
                    for j, r in enumerate(response, start=1):
                        if j == 1:
                            messageSummary.append(f"  To fix it, try:")
                        messageSummary.append(f"  {j}. {responses[r]}")

    # Look for Unbalanced or Unfilled pages (only show up if \tracing{b} is enabled in ptxprint-mods.tex)
    uf_matches = re.findall(r'Underfill\[(A|B)\]: \[(\d+)\]', logText)
    if len(uf_matches):
        # Extract unique page numbers and sort them in ascending order
        unique_page_numbers = sorted(set(int(match[1]) for match in uf_matches), key=int)
        category_counts["W"] += 1
        messageSummary.append(f"{len(unique_page_numbers)} underfilled pages: {shorten_ranges(unique_page_numbers)}")

    if __name__ == "__main__":
        print(category_counts, '\n'.join(messageSummary))
    else:
        return category_counts, messageSummary

def shorten_ranges(numbers):
    ranges = []
    current_range = [numbers[0]]

    for i in range(1, len(numbers)):
        if numbers[i] - numbers[i-1] == 1:
            current_range.append(numbers[i])
        else:
            if len(current_range) > 1:
                ranges.append(f"{current_range[0]}-{current_range[-1]}")
            else:
                ranges.append(str(current_range[0]))
            current_range = [numbers[i]]

    if len(current_range) > 1:
        ranges.append(f"{current_range[0]}-{current_range[-1]}")
    else:
        ranges.append(str(current_range[0]))

    return ", ".join(ranges)

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

# Main program (if run from commandline)
if __name__ == "__main__":
    root_folder = r"C:\My Paratext 9 Projects"
    search_and_summarize_recent_logs(root_folder)
