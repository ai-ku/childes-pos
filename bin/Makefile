all: mike_childes fastsubs eval.pl wkmeans scode

## FASTSUBS
FASTSUBS_GIT_REPO=git://github.com/ai-ku/fastsubs.git
FASTSUBS_GIT_TAG=
####
## WKMEANS
WKMEANS_GIT_REPO=git://github.com/ai-ku/wkmeans.git
WKMEANS_GIT_TAG=
## SCODE
SCODE_GIT_REPO=git://github.com/ai-ku/scode.git
SCODE_GIT_TAG=
###

eval.pl: check
	test -e $@ || ln -s ../src/scripts/* .

mike_childes: check
	cd ../src/mikenet8/childes; make
	test -e $@ || ln -s ../src/mikenet8/childes/mike_childes .

scode: check
	test -e ../src/scode || (cd ../src/ ; git clone ${SCODE_GIT_REPO} ; git checkout ${SCODE_GIT_TAG}) 
	cd ../src/scode; make
	test -e $@ || ln -s ../src/scode/scode .

wkmeans: check
	test -e ../src/wkmeans || (cd ../src/ ; git clone ${WKMEANS_GIT_REPO} ; git checkout ${WKMEANS_GIT_TAG}) 
	cd ../src/wkmeans; make
	test -e $@ || ln -s ../src/wkmeans/wkmeans .

fastsubs: check
	test -e ../src/fastbust || (cd ../src/ ; git clone ${FASTSUBS_GIT_REPO} ; git checkout ${FASTSUBS_GIT_TAG}) 
	cd ../src/fastsubs; make
	test -e $@ || ln -s ../src/fastsubs/fastsubs .
	test -e wordsub || ln -s ../src/fastsubs/wordsub .

check:
	true

clean:
	-rm *~ mike_childes wordsub fastsubs *.pl *.py