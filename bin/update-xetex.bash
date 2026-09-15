#!/bin/bash

# Update the bundled Windows XeTeX tree from a portable TeX Live installation.
#
# Obtain the TeX Live tree with the regular TeX Live installer, not w32tex:
# choose Install, not Unpack only
# choose a mirror if needed
# unselect Install TeXworks front end
# click Advanced
# Portable setup: Yes
# Scheme: small scheme (basic + xetex, metapost, a few languages)
# N. of collections: 1/41 [uncheck everything except the collection XeTeX and packages]
#
# Equivalently, for an unattended install, pass install-tl a profile
# containing at least:
#     selected_scheme scheme-custom
#     collection-basic 1
#     collection-xetex 1
#     instopt_portable 1
#     tlpdbopt_create_formats 1
#     tlpdbopt_install_docfiles 0
#     tlpdbopt_install_srcfiles 0
#
# Usage: bin/update-xetex.bash <portable-texlive-dir>
# Run from the root of the repository.
#
# Only files this repository already tracks are refreshed; the bundled tree is
# a deliberately trimmed subset of TeX Live and this script does not grow it.
# Adding a file that a new TeX Live release needs is a manual decision.

set -u

tmpdir=$1
if [ -z "$tmpdir" ]
then
    echo "Need to specify the portable TeX Live installed folder"
    exit 1
fi

if [ ! -e "$tmpdir" ]
then
    echo "$tmpdir does not exist"
    exit 1
fi

if [ ! -d "$tmpdir" ]
then
    echo "$tmpdir is not a directory"
    exit 1
fi

if [ ! -d xetex ]
then
    echo "No xetex directory here; run this from the root of the repository"
    exit 1
fi

tmpdir=$(cd "$tmpdir" && pwd)
repo=$PWD/xetex

# TeX Live keeps the Windows binaries in bin/windows; this repository keeps
# them in bin/win32_x86_64, matching the bindir that runner.py computes from
# sys.platform and platform.machine().
tlbin=bin/windows
repobin=bin/win32_x86_64

# Versioned files embed a version number in the name (icudt72.dll became
# icudt78.dll between TeX Live 2023 and 2026), so the old one has to be
# removed and the new one added rather than overwritten in place.
versioned_files="icudt*.dll msvcr*.dll"   # kpathsea*.dll

# Map a path relative to xetex/ onto its source path relative to the TeX Live
# tree. Everything under texmf-dist/ matches one-for-one; the binaries are
# relocated, and the format file is moved next to the binaries so that kpathsea
# finds it via the $SELFAUTOLOC/web2c{/$engine,} element of TEXFORMATS.
map_source() {
    case "$1" in
        "$repobin"/web2c/xetex/xetex.fmt) echo "texmf-var/web2c/xetex/xetex.fmt" ;;
        "$repobin"/*)                     echo "$tlbin/${1#"$repobin"/}" ;;
        *)                                echo "$1" ;;
    esac
}

# Drop the versioned files first so that stale ones do not survive the update.
( cd "$repo/$repobin" && git rm --quiet --ignore-unmatch $versioned_files )

# Refresh every file the repository already tracks under the Windows bin
# directory and the shared texmf tree. Other platforms' bin directories are
# deliberately left alone: they come from a TeX Live build for that platform.
missing=0
for f in $( cd "$repo" && find "$repobin" texmf-dist -type f ! -name '*.log' | sort )
do
    src="$tmpdir/$(map_source "$f")"
    if [ -f "$src" ]
    then
        cp -p "$src" "$repo/$f"
    else
        echo "WARNING: no TeX Live source for xetex/$f"
        missing=$((missing + 1))
    fi
done

# Add the new versioned files.
for pattern in $versioned_files
do
    found=$(cd "$tmpdir/$tlbin" && ls $pattern 2>/dev/null)
    if [ -z "$found" ]
    then
        echo "WARNING: no TeX Live file matching $pattern"
        missing=$((missing + 1))
        continue
    fi
    for f in $found
    do
        cp -p "$tmpdir/$tlbin/$f" "$repo/$repobin/$f"
    done
done

( cd "$repo/$repobin" && git add $versioned_files && chmod 700 *.exe )

echo
if [ "$missing" -gt 0 ]
then
    echo "$missing file(s) had no source in the TeX Live tree - check the"
    echo "warnings above before committing. A renamed or dropped file may"
    echo "need the same treatment as the versioned files."
    echo
fi
echo "Review changes and commit"
echo
