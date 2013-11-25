### 1.1 BIN INSTALLATION
# build only the scripts

all: substitute.pdf ngram.pdf perplexity.pdf fletags10K.pdf fletags100K.pdf wsubtags10K.pdf wsubtags100K.pdf inputlayer.pdf 

bin:
	cd ../bin; make eval.pl

export PATH := ../bin:.:${PATH}
PLOT_DIR=figures/
### 2 Plots
WSUB_PLOT=../run/
PLOT_DATA=figure_data/
ALL=".all"

fletags10K.pdf:
	ls ${PLOT_DATA}10000/*${ALL}.fle.anl | tagplot.py $@
	mv $@ ${PLOT_DIR}$@
	
wsubtags10K.pdf:
	ls ${PLOT_DATA}10000/*${ALL}.wsub16.anl | tagplot.py $@
	mv $@ ${PLOT_DIR}$@

fletags100K.pdf:
	ls ${PLOT_DATA}100000/*${ALL}.fle.anl | tagplot.py $@
	mv $@ ${PLOT_DIR}$@
	
wsubtags100K.pdf:
	ls ${PLOT_DATA}100000/*${ALL}.wsub16.anl | tagplot.py $@
	mv $@ ${PLOT_DIR}$@

substitute.pdf: 
	#train test on same child corpus
	ls ${PLOT_DATA}*wsub.plot | subsplot.py 
	mv $@ ${PLOT_DIR}$@

allsubstitute.pdf: 
	#train on all child corpus test on each child corpus
	cat ${PLOT_DATA}split.wsub.plot | allsubsplot.py 
	mv allsubstitute.pdf ${PLOT_DIR}$@

ngram.pdf:
	ls ${PLOT_DATA}fixwsub*gram | ngramplot.py 
	mv $@ ${PLOT_DIR}$@
	
perplexity.pdf:
	ls ${PLOT_DATA}mintz03.*.plot | perplexityplot.py 
	mv $@ ${PLOT_DIR}$@
	
inputlayer.pdf:
	inputplot.py
	mv $@ ${PLOT_DIR}$@
