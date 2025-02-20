FROM python:3.11
WORKDIR /app
RUN apt-get update
RUN apt-get install -y texlive-xetex
COPY python/ python/
COPY xetex/ xetex/
COPY src/ src/
COPY fonts/ fonts/
COPY pyproject.toml MANIFEST.in ./
RUN pip install --no-cache-dir .

ENTRYPOINT ["ptxprint"]
