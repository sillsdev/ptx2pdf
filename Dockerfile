# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm
WORKDIR /app
#    apt-get install --no-install-recommends -y texlive-xetex fontconfig
RUN <<EOF
    apt-get update 
    apt install --no-install-recommends -y tex-common teckit texlive-base texlive-binaries texlive-latex-base fontconfig
    apt download texlive-xetex
    dpkg --install --force-depends texlive-xetex_*_all.deb
    rm texlive-xetex_*_all.deb
    apt-get clean
    rm -fr /usr/share/texlive/texmf-dist/tex /usr/share/texlive/texmf-dist/fonts
EOF
COPY python/ python/
COPY xetex/ xetex/
COPY src/ src/
COPY fonts/ fonts/
COPY pyproject.toml MANIFEST.in ./
RUN <<EOF
    pip install --no-cache-dir .
    rm -fr build
EOF
ENTRYPOINT ["ptxprint"]
