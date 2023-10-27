PACKAGE_NAME = pdf-splitter
BINARY_NAME = $(PACKAGE_NAME)
INSTALL_DIR = $(HOME)/.local/bin
VENV_DIR = venv

all: build

build: venv
	$(VENV_DIR)/bin/pyinstaller --onefile --name $(BINARY_NAME) main.py --hidden-import ui/pdf-splitter.ui
	mv dist/$(BINARY_NAME) .

venv:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/python -m pip install -r requirements.txt

install: build
	install -m 755 $(BINARY_NAME) $(INSTALL_DIR)/$(BINARY_NAME)

uninstall:
	rm -f $(INSTALL_DIR)/$(BINARY_NAME)

clean:
	rm -rf build/ dist/ __pycache__ *.spec $(BINARY_NAME)

.PHONY: all build install uninstall clean
