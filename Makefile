PY = python3
PYTEST = pytest
DOC = doxygen
DOCCONFIG = docConfig
SRC = matrix_adt_test.py

.PHONY: all test doc clean

test: 
	$(PYTEST) $(SRC)

doc: 
	$(DOC) $(DOCCONFIG)
	cd latex && $(MAKE)

all: test doc

clean:
	rm -rf html
	rm -rf latex
