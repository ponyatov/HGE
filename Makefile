NEO_VER = 3.2.3
NEO = neo4j-community-$(NEO_VER)-unix
NEO_GZ = $(NEO).tar.gz

WGET = wget -c
gz/$(NEO_GZ):
	$(WGET) -O $@ https://neo4j.com/artifact.php?name=neo4j-community-3.2.3-unix.tar.gz

.PHONY all: log.log

log.log: py.py
	python $< > $@ && tail $(TAIL) $@