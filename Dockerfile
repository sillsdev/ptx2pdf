# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm
WORKDIR /app
RUN <<EOF
    apt-get update 
    apt-get install --no-install-recommends -y texlive-xetex fontconfig
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
