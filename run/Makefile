### 1. GENERAL SETUP

### 1.1 BIN INSTALLATION

bin:
	cd ../bin; make

MINTZ_DATA_PATH=../data/childes/mintz03xml/
TRAIN_DATA_PATH=../data/childes/data-xml

SEED=0
all: mintz03 clair10pr clair10ps
data: anne.data.gz aran.data.gz eve.data.gz naomi.data.gz nina.data.gz peter.data.gz

mintz03: anne.fre.eval aran.fre.eval eve.fre.eval naomi.fre.eval nina.fre.eval peter.fre.eval
clair10pr: anne.prbi.eval aran.prbi.eval eve.prbi.eval naomi.prbi.eval nina.prbi.eval peter.prbi.eval
clair10ps: anne.psbi.eval aran.psbi.eval eve.psbi.eval naomi.psbi.eval nina.psbi.eval peter.psbi.eval

%.data.gz:
	ls ${MINTZ_DATA_PATH}$*/*.xml | childes.pl 2> $*.err | gzip > $@ &

## SRILM Language Model
SRILM_PATH=/opt/srilm/bin/i686-m64
LM_VOCAB=2
LM_NGRAM=4
LM_DISCOUNT=-kndiscount
export PATH := ../bin:.:${SRILM_PATH}:${PATH}

train.tok.gz:
	find ${TRAIN_DATA_PATH} -type f | ${SRC_PATH}childes.pl -w 2> train.tok.err | gzip > $@

%.vocab.gz: train.tok.gz ## LM_VOCAB=2: time=1m16s, wc=78498   78498  672284
	zcat $< | ngram-count -write-order 1 -text - -write - | \
	perl -lane 'print $$F[0] if $$F[1] >= ${LM_VOCAB}' | gzip > $@

%.lm.gz: %.vocab.gz train.tok.gz ## LM_NGRAM=4, LM_VOCAB=20: time=6m10s, wc=27427373 118077512 847912087
	zcat train.tok.gz | ngram-count -order ${LM_NGRAM} ${LM_DISCOUNT} -interpolate -unk -vocab $< -text - -lm $@

### FASTSUBS options:
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

%.sub.gz: %.fre.gz train.lm.gz  ## FS_NSUB=100 FS_PSUB=1: time=4h47m, wc=1222974 245817774 2350067125
	cat $*.fre.stat | fastsubs ${FS_OPTIONS} train.lm.gz | grep -P '^X' | gzip > $@

### WORDSUB options:
WORDSUB=3

%.pairs.gz: %.sub.gz	## WORDSUB=12: time=6m33s wc=14085192 28170384 151744889
	zcat $< | awk '{for (i=0;i< ${WORDSUB};i++) print $$0}' |\
	wordsub -s 0  | perl -lane '@a = split; $$c++; $$subs .= $$a[1] . " ";if ($$c == ${WORDSUB}){print "$$a[0] $$subs"; $$c =0; $$subs = "";}' | gzip > $@

%.wordsub.mike.gz: %.pairs.gz %.fre.gz
	sub2mike.py "./" $* 2> $*.wordsub.mike.gz.info | gzip > $@ 

### TRAIN-TEST SPLIT
SPLIT_RATIO=.30

%.split.fre.gz: %.fre.gz
	rsplit.py ${SEED} $*.fre.stat  $< ${SPLIT_RATIO} 2> $*.split.fre.stat | gzip > $@  

### Train-Test SPLIT

### FLEXIBLE FRAMES Train-Test
%.trfle.mike.gz: %.split.fre.rm
	-gz $*.tefle.mike.gz
	tomikesparse.py fle $< 2> $@.info | \
		 split.py  2> $*.tefle.mike | gzip > $@
	gzip $*.tefle.mike

%.trfle.runmk: %.trfle.mike.gz
	runmike.py $<.info ${ITER} $*.tefle.mike.gz

### FIXED FRAMES Train-Test
%.trfre.mike.gz: %.split.fre.gz
	-rm $*.tefre.mike.gz
	tomikesparse.py fre $< 2> $@.info | \
		 split.py  2> $*.tefre.mike | gzip > $@
	gzip $*.tefre.mike

%.trfre.runmk: %.trfre.mike.gz
	runmike.py $<.info ${ITER} $*.tefre.mike.gz

### Wordsub Train-Test
%.trws.mike.gz: %.pairs.gz %.split.fre.gz
	-rm $*.trws.pairs.gz $*.tews.mike.gz $*.trws.fre.stat
	ln -s $*.split.fre.stat $*.trws.fre.stat
	ln -s $*.pairs.gz $*.trws.pairs.gz
	sub2mike.py "./" $*.trws 2> $*.trws.mike.gz.info | \
		 split.py  2> $*.tews.mike | gzip > $@
	gzip $*.tews.mike	

%.trws.runmk: %.trws.mike.gz
	runmike.py $<.info ${ITER} $*.tews.mike.gz

## ALL-Data Split Train-Test
split.frame.out: anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz 
	splitframe-args.py ${EXP_ITER} ${SPLIT_RATIO} | xargs -n5 -P${NCPU} splitframerun.pl > $@

split.wsub.out: anne.sub.gz aran.sub.gz eve.sub.gz naomi.sub.gz nina.sub.gz peter.sub.gz anne.fre.gz	 aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	splitwordsub-args.pl ${EXP_ITER} ${SPLIT_RATIO} | xargs -n5 -P${NCPU} splitwordsubrun.pl > $@

split.frame.plot: split.frame.out
	for label in anne aran eve naomi nina peter; do\
		echo "$$label scores" >> $@; \
		cat $< | plotdata.pl 2=$$label 3=x 4=y >> $@ ;\
	done

split.wsub.plot: split.wsub.out
	for label in anne aran eve naomi nina peter; do\
		echo "$$label scores" >> $@; \
		cat $< | plotdata.pl 3=$$label 2=x 4=y >> $@ ;\
	done

### FREQUENT (AXB), FLEXIBLE(AX + XB) and BIGRAM FRAMES (AX and XB)
FRAME_THR=0
MINTZ03_OPTIONS=-t ${FRAME_THR} -u 

#also equivalent to FLEXIBLE
%.fre.gz: %.data.gz
	zcat $< | frame.py  ${MINTZ03_OPTIONS} 2> $*.fre.stat |gzip > $@ 

%.prbi.gz: %.data.gz
	zcat $< | frame.py  -f prbi ${MINTZ03_OPTIONS} 2> $*.prbi.stat |gzip > $@ 

%.psbi.gz: %.data.gz
	zcat $< | frame.py  -f psbi ${MINTZ03_OPTIONS} 2> $*.psbi.stat |gzip > $@ 

%.word.gz: %.gz
	zcat $< | cut -f 1 | gzip > $@

%.pos.gz: %.gz
	zcat $< | cut -f 3 | gzip > $*.pos.gz

%.gold.gz: %.gz
	zcat $< | cut -f 2 | gzip > $*.gold.gz

%.eval: %.pos.gz %.gold.gz
	zcat $< | eval.pl -c -m -v -g $*.gold.gz 2> $@

%.dist: %.gz
	zcat $< | perl -lane '$$h{$$F[1]}++;END{print "$$_ $$h{$$_}" foreach keys(%h)}'

## MIKENET Neural Network
mikenet.data:	anne.mikenet aran.mikenet eve.mikenet naomi.mikenet nina.mikenet peter.mikenet

%.mikenet: %.fre.runmk %.psbi.runmk %.prbi.runmk %.fle.runmk %.apsbi.runmk %.aprbi.runmk
	echo $@

%.fre.mike.gz: %.fre.gz
	tomike.py fre $<  2> $@.info | gzip > $@ 

%.fle.mike.gz: %.fre.gz
	tomike.py fle $<  2> $@.info | gzip > $@

%.psbi.mike.gz: %.fre.gz
	tomike.py ps $<  2> $@.info | gzip > $@ 

%.apsbi.mike.gz: %.psbi.gz
	tomike.py ps $<  2> $@.info | gzip > $@

%.prbi.mike.gz: %.fre.gz
	tomike.py pr $<  2> $@.info | gzip > $@ 

%.aprbi.mike.gz: %.prbi.gz
	tomike.py pr $<  2> $@.info | gzip > $@

all.fre.mike.gz: anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	tomikesparse.py fre anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz \
	2> $@.info | gzip > $@

all.fle.mike.gz: anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	tomikesparse.py fle anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz \
	2> $@.info | gzip > $@

all.pr.mike.gz: anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	tomikesparse.py pr anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz \
	2> $@.info | gzip > $@

all.ps.mike.gz: anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	tomikesparse.py ps anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz \
	2> $@.info | gzip > $@

### Individual Run

ITER=10000
%.runmk: %.mike.gz
	runmike.py $<.info ${ITER}

## EXPERIMENTS

EXP_ITER=10000
NCPU=10
## ALL-Data Experiments
all.%.frame.out: all.%.mike.gz
	allframe-args.py $< ${EXP_ITER} | xargs -n4 -P${NCPU} allframerun.pl > $@

all.wordsub.out: anne.sub.gz aran.sub.gz eve.sub.gz naomi.sub.gz nina.sub.gz peter.sub.gz anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	mikeall-args.py ${EXP_ITER} | xargs -n4 -P${NCPU} mikeallrun.pl

## MIKENET Experiments

%.frame.out: %.fre.gz %.prbi.gz %.psbi.gz
	frame-args.py $* ${EXP_ITER} | xargs -n5 -P1 framerun.pl  > $@

### Wordsub experiments
%.wordsub.out: %.sub.gz %.fre.gz %.pairs.gz
	mikerun-args.py $*.wordsub ${EXP_ITER} | xargs -n6 -P${NCPU} mikerun.pl  > $@

%.plot: %.out
	cat $< | plotdata.pl 2=x 3=y > $@

.PRECIOUS: %.fre.gz %.prbi.gz %.psbi.gz %.word.gz %.pos.gz %.gold.gz %.data.gz %.fle.nn %.psbi.nn %.prbi.nn %.fre.nn %.psbi.mike.gz %.prbi.mike.gz %.apsbi.mike.gz %.aprbi.mike.gz %.fre.mike.gz %.fle.mike.gz %.runmk %.sub.gz %.wordsub.mike.gz %.pairs.gz %.wordsub.out %.trws.fre.stat %.trws.mike.gz %.split.fre.stat %.trfle.mike.gz %.trfre.mike.gz

clean:
	-rm *.fre.* *.prbi.* *.psbi.*

clean.all:
	-rm *data.gz 
	-rm *.err
	-rm *.fre* *.prbi* *.psbi*