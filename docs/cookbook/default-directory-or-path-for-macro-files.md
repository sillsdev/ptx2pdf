#### Navigation

[Home](../home/README.md)  | [Installation](../installation/README.md) | [Quick Start](../quick-start/README.md) | [Documentation](../documentation/README.md) | [Cookbook ](README.md)

[Cookbook >](README.md)

# <span class="entry-title">Default directory or path for macro files</span>


## <a name="TOC-Problem">Problem</a>

<a name="TOC-Problem">

What is the default directory/path for the macro files where they can be found by XeTeX? (so that I don't have to copy them into my working directory for each new project)

</a>

## <a name="TOC-Problem"></a><a name="TOC-Solution">Solution</a>

<a name="TOC-Solution">

*   **For Mac OS X:** Create a directory "texmf" in your Home directory, and within this a subdirectory "tex" and a further subdirectory called "ptx2pdf", or others for other macros you may be using, so you'll have `~/texmf/tex/ptx2pdf/<macro-files>`. (With some TeX distributions on Mac OS X, the "texmf" folder should be placed within your personal Library folder, rather than directly in your home directory. So you may need to try both those possibilities.)

*   **For anyone running TeX Live on Windows:** look for the "texmf-local" folder that should have been created during installation, alongside the main texlive folder, and put macro files inside `texmf-local/tex/<whatever>`

</a>

<a name="TOC-Solution"></a></td>


<small>Updated on <abbr class="updated" title="2012-01-06T15:26:08.702Z">Jan 6, 2012</abbr> by <span class="author"><span class="vcard">Jeff Klassen</span> </span>(Version <span class="sites:revision">6</span>)</small>
