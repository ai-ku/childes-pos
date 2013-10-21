### 1.1 BIN INSTALLATION
# build only the scripts

bin:
	cd ../bin; make eval.pl

export PATH := ../bin:.:${PATH}
PLOT_DIR=figures/
### 2 Plots
WSUB_PLOT=../run/
PLOT_DATA=figure_data/

all: substitute.pdf ngram.pdf perplexity.pdf inputlayer.pdf

substitute.pdf: 
	ls ${PLOT_DATA}*wsub.plot | subsplot.py 
	mv $@ ${PLOT_DIR}$@
	
ngram.pdf:
	ls ${PLOT_DATA}fixwsub*gram | ngramplot.py 
	mv $@ ${PLOT_DIR}$@
	
perplexity.pdf:
	ls ${PLOT_DATA}mintz03.*.plot | perplexityplot.py 
	mv $@ ${PLOT_DIR}$@
	
inputlayer.pdf:
	inputplot.py
	mv $@ ${PLOT_DIR}$@
