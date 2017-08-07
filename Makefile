NEO_VER = 3.2.3
NCL_VER = 1.9.5

.PHONY: all neo

all: neo log.log

log.log: src.src py.py
	python py.py $< > $@ && tail $(TAIL) $@
	
NEO = neo4j-community-$(NEO_VER)
NEO_GZ = $(NEO)-unix.tar.gz
NCL = neoclipse-$(NCL_VER)
NCL_GZ = $(NCL)-linux.gtk.x86_64.tar.gz

neo: $(NEO)/README.txt $(NCL)/README.txt

$(NEO)/README.txt: gz/$(NEO_GZ)
	tar zx < $< && touch $@
$(NCL)/README.txt: gz/$(NCL_GZ)
	tar zx < $< && touch $@

WGET = wget -c
gz/$(NEO_GZ):
	$(WGET) -O $@ https://neo4j.com/artifact.php?name=$(NEW_GZ)
gz/$(NCL_GZ):
	$(WGET) -O $@ http://dist.neo4j.org/neoclipse/$(NCL)-linux.gtk.x86_64.tar.gz