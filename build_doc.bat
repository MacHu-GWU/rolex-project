pushd "%~dp0"
cd rolex
python zzz_manual_install.py
cd ..
python create_doctree.py
make html