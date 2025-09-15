python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip3 install -e .
pip3 install pyinstaller
pyinstaller ptxprint.spec -y

