# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm
WORKDIR /app
#    apt-get install --no-install-recommends -y texlive-xetex fontconfig. The following is much smaller but complex
RUN <<EOF
    apt-get update 
    apt install --no-install-recommends -y tex-common teckit texlive-base texlive-binaries texlive-latex-base fontconfig
	apt install fonts-sil-ezra fonts-sil-galatia 
	apt install fonts-sil-charis fonts-sil-gentium fonts-sil-andika
	apt install fonts-sil-scheherazade fonts-sil-harmattan fonts-sil-lateef fonts-sil-awami-nastaliq 
	apt install fonts-sil-annapurna 
	apt install fonts-sil-padauk
#	apt install fonts-noto-core fonts-noto-extra
	apt install ttf-mscorefonts-installer
    apt download texlive-xetex
    dpkg --install --force-depends texlive-xetex_*_all.deb
    rm texlive-xetex_*_all.deb
    rm -fr /usr/share/texlive/texmf-dist/tex /usr/share/texlive/texmf-dist/fonts
    apt-get clean
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
