
# Instructions for the creation of AI based PRs

Congratulations, you found a bug and wish to submit a PR to fix it. Of course
you have tested your fix to ensure it does fix the issue and are therefore ready
to submit. Please remember the following.

1. All PRs should be associated with an existing issue. This means you do not
need to explain the issue again. If you cannot get your explanation down to 1-2
paragraphs, you are over thinking it.

2. You are fixing a bug, not writing a huge new feature. Therefore the value of
your patch is inversely proportional to its size. A typical bug fix should be <
10 lines of additional code.

3. Once your bug is gone it should remain gone. We don't need a slew of tests to
prove your solution. That's what human code review is for. Do not include tests
in your submission.

4. Remember you are fixing a bug (or cluster of bugs) not writing a full
application or a new feature. We typically do not accept AI written features via
issues.

Using AI to help with coding is valuable and a modern large LLM can often find
bugs we don't spot and fix them. This document is not saying we don't accept AI
generated solutions, just that the solutions should be targetted for quick human
review with minimised code change and short explanations.
