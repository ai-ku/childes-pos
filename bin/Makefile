all: mike_childes fastsubs eval.pl

eval.pl: check
	test -e $@ || ln -s ../src/scripts/* .

mike_childes: check
	cd ../src/mikenet8/childes; make
	test -e $@ || ln -s ../src/mikenet8/childes/mike_childes .


fastsubs: check
	cd ../src/fastsubs; make
	test -e $@ || ln -s ../src/fastsubs/fastsubs .
	test -e wordsub || ln -s ../src/fastsubs/wordsub .

check:
	true

clean:
	-rm *~ mike_childes wordsub fastsubs *.pl *.py