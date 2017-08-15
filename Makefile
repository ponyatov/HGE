NEO_VER = 3.2.3
#NCL_VER = 1.9.5
JRE_VER = 8u144
JRE_RELEASE = 1.8.0_144

NEO = neo4j-community-$(NEO_VER)
NEO_GZ = $(NEO)-unix.tar.gz
#NCL = neoclipse-$(NCL_VER)
#NCL_GZ = $(NCL)-linux.gtk.x86_64.tar.gz
JRE = jre$(JRE_RELEASE)
JRE_GZ = jre-$(JRE_VER)-linux-x64.tar.gz

CWD = $(CURDIR)

.PHONY: all neo server doc

all: neo log.log doc
#	JAVA_HOME=$(CURDIR)/$(JRE) env | grep -i java

log.log: src.src py.py
	python py.py $< > $@ && tail $(TAIL) $@
	
neo: $(NEO)/README.txt $(JRE)/Welcome.html
#$(NCL)/README.txt 

$(NEO)/README.txt: gz/$(NEO_GZ)
	tar zx < $< && touch $@
#$(NCL)/README.txt: gz/$(NCL_GZ)
#	tar zx < $< && touch $@
$(JRE)/Welcome.html: gz/$(JRE_GZ)
	tar zx < $< && touch $@

WGET = wget -c
gz/$(NEO_GZ):
	$(WGET) -O $@ https://neo4j.com/artifact.php?name=$(NEW_GZ)
#gz/$(NCL_GZ):
#	$(WGET) -O $@ http://dist.neo4j.org/neoclipse/$(NCL)-linux.gtk.x86_64.tar.gz
gz/$(JRE_GZ):
	$(WGET) -O $@ --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/$(JRE_VER)-b01/090f390dda5b47b9b721c7dfaa008135/$(JRE_GZ)
	
server: neo
	JAVA_HOME=$(CWD)/$(JRE) $(CWD)/$(NEO)/bin/neo4j console 

doc: doc/architecture.png doc/mobile.png

doc/%.svg: doc/%.dot
	dot -T svg -o $@ $<
doc/%.png: doc/%.dot
	dot -T png -o $@ $<