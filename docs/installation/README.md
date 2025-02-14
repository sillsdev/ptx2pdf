### Installation

# Installation in a Ubuntu environment (container or virtual machine)

```
sudo apt install libgirepository1.0-dev libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 texlive-xetex python3-setuptools gir1.2-poppler-0.18 gir1.2-gtksource-3.0 python3-numpy python3-gi gobject-introspection gir1.2-gtk-3.0 libgtk-3-0 gir1.2-gtksource-3.0 python3-cairo python3-regex python3-pil python3-venv fonts-sil-charis

git clone --depth=1 https://github.com/sillsdev/ptx2pdf.git
cd ptx2pdf
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel build
pip install .
```

## configuration files 

Config files (like the default path to the translation project files) are stored in ~/.config/ptxprint/


# Installation in Windows

Install using the exe made with pyinstaller. 


