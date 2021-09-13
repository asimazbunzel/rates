SHELL=/bin/bash
CONDA_ROOT=$(HOME)/.local/bin/conda

install:
	source $(CONDA_ROOT)/bin/activate && conda activate bin2dco-3.9 && python setup.py install

