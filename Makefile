.PHONY all: log.log

log.log: py.py
	python $< > $@ && tail $(TAIL) $@