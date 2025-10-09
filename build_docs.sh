pip install -r requirements.txt
sphinx-apidoc -o ./sphinx/bdat ./src
make -C ./sphinx html
