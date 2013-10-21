### 1. GENERAL SETUP

### 1.1 BIN INSTALLATION

bin:
	cd ../bin; make

RESULTS_PATH=results/
MINTZ_DATA_PATH=../data/childes/mintz03xml/
TRAIN_DATA_PATH=../data/childes/data-xml
NCPU=10
SEED=0

all: mintz03 clair10pr clair10ps
data: anne.data.gz aran.data.gz eve.data.gz naomi.data.gz nina.data.gz peter.data.gz

mintz03: anne.fre.eval aran.fre.eval eve.fre.eval naomi.fre.eval nina.fre.eval peter.fre.eval
clair10pr: anne.prbi.eval aran.prbi.eval eve.prbi.eval naomi.prbi.eval nina.prbi.eval peter.prbi.eval
clair10ps: anne.psbi.eval aran.psbi.eval eve.psbi.eval naomi.psbi.eval nina.psbi.eval peter.psbi.eval
yatbaz12: anne.wsub.plot aran.wsub.plot eve.wsub.plot naomi.wsub.plot nina.wsub.plot peter.wsub.plot 

yatbaz12_nohup: train.tok.gz
	nohup make anne.wsub.plot > anne.out 2> anne.err &
	nohup make aran.wsub.plot > aran.out 2> aran.err &
	nohup make eve.wsub.plot > eve.out 2> eve.err &
	nohup make naomi.wsub.plot > naomi.out 2> naomi.err &
	nohup make nina.wsub.plot > nina.out 2> nina.err &
	nohup make peter.wsub.plot > peter.out 2> peter.err &

%.data.gz:
	ls ${MINTZ_DATA_PATH}$*/*.xml | childes.pl 2> $*.err | gzip > $@ 

## SRILM Language Model
SRILM_PATH=/opt/srilm/bin/i686-m64
LM_VOCAB=2
LM_NGRAM=4
LM_DISCOUNT=-kndiscount
export PATH := ../bin:.:${SRILM_PATH}:${PATH}

train.tok.gz:
	find ${TRAIN_DATA_PATH} -type f | childes.pl -w 2> train.tok.err | gzip > $@

# test data extractor
%.tok.gz:
	ls ${MINTZ_DATA_PATH}$*/*.xml | childes.pl -w 2> $*.err | gzip > $@ 

%.vocab.gz: train.tok.gz ## LM_VOCAB=2: time=1m16s, wc=78498   78498  672284
	zcat $< | ngram-count -write-order 1 -text - -write - | \
	perl -lane 'print $$F[0] if $$F[1] >= ${LM_VOCAB}' | gzip > $@

%.lm.gz: %.vocab.gz train.tok.gz ## LM_NGRAM=4, LM_VOCAB=20: time=6m10s, wc=27427373 118077512 847912087
	zcat train.tok.gz | ngram-count -order ${LM_NGRAM} ${LM_DISCOUNT} -interpolate -unk -vocab $< -text - -lm $@

%.ppl.gz: %.data.gz train.lm.gz 
	zcat $< | extractText.py | \
	ngram -order ${LM_NGRAM} -unk -lm train.lm.gz -ppl - -debug 2 | gzip > $@

mintz03.ppl.plot: anne.ppl.gz aran.ppl.gz eve.ppl.gz naomi.ppl.gz nina.ppl.gz peter.ppl.gz 
	-rm $@
	for label in anne aran eve naomi nina peter; do\
		echo "$$label n-gram: ${LM_NGRAM}" >> $@; \
		zcat $$label.ppl.gz | tail -1 >> $@;\
	done

### FASTSUBS options:
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

%.sub.gz: %.fre.gz train.lm.gz  ## FS_NSUB=100 FS_PSUB=1: time=4h47m, wc=1222974 245817774 2350067125
	zcat $< | cut -f 2 | fastsubs ${FS_OPTIONS} train.lm.gz | grep -P '^X' | gzip > $@

### WORDSUB options:
WORDSUB=16
%.pairs.gz: %.sub.gz	## WORDSUB=12: time=6m33s wc=14085192 28170384 151744889
	zcat $< | awk '{for (i=0;i< ${WORDSUB};i++) print $$0}' |\
	wordsub -s ${SEED}  | perl -lane '@a = split; $$c++; $$subs .= $$a[1] . " ";if ($$c == ${WORDSUB}){print "$$subs"; $$c =0; $$subs = "";}' | gzip > $@

### SCODE (simple) experiments
SCODE_CLUSTER=40
SCODE_ITER=$(shell echo 1 + 100 / ${WORDSUB} | bc)

WSC_OPTIONS=-r 1 -i ${SCODE_ITER} -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v -a

%.wpairs.gz: %.pairs.gz %.word.gz ## WS_NSUB=64: time=20m55s wc=75121024 150242048 809663253
	zcat $*.pairs.gz > $@.tmp
	zcat $*.word.gz | paste - $@.tmp | perl -lane 'print "$$F[0]\t$$_" foreach(@F[1..$$#F]);' | gzip > $@
	-rm $@.tmp

%.scode.gz: %.wpairs.gz 
	zcat $< | scode ${WSC_OPTIONS} | gzip > $@

KM_OPTIONS=-k ${SCODE_CLUSTER} -r 128 -l -w  -s ${SEED}
%.kmeans.gz: %.scode.gz
	zcat $< | perl -ne 'print if s/^0://' | wkmeans ${KM_OPTIONS} | gzip > $@

%.eval: %.kmeans.gz %.pos.gz %.word.gz
	zcat $*.kmeans.gz | wkmeans2eval.pl -t $*.word.gz|  eval.pl -m -v -g $*.pos.gz

%.anl.gz: %.kmeans.gz %.word.gz
	zcat $< | wkmeans2eval.pl -t $*.word.gz | analyze_cluster.py $*.word.gz | gzip > $@

# (word TAB pos TAB subsitutes(space seperated))
%.wsub.gz: %.pairs.gz %.fre.gz
	zcat $< > $@.tmp
	zcat $*.fre.gz | cut -f1,3,4 | paste - $@.tmp | gzip > $@
	-rm $@.tmp

### TRAIN-TEST SPLIT WITH CROSS VALIDATION
CROSSVAL=10
TARGET_FOLD=0
ITER=20000
VERBOSE=-v

%.split.fre.gz: %.fre.gz
	crossval.py -v -seed ${SEED} -tarFold ${TARGET_FOLD} -foldNum ${CROSSVAL} -d $< 2> $*.split.fre.err | gzip > $@  

### FLEXIBLE FRAMES Train-Test

%.fle.runmk: %.fre.gz
	-rm $*.tefle.runmk.gz
	crossval.py -seed ${SEED} -tarFold ${TARGET_FOLD} -foldNum ${CROSSVAL} -d $< | \
		tomikesparse.py fle 2> $@.info | \
		split.py  2> $*.tefle.runmk | gzip > $*.trfle.runmk.gz
	runmike.py ${VERBOSE} -info $@.info -i ${ITER} -te $*.tefle.runmk -tr $*.trfle.runmk.gz -seed ${SEED}

### FIXED FRAMES Train-Test
%.fre.runmk: %.fre.gz
	-rm $*.tefre.runmk.gz
	crossval.py -seed ${SEED} -tarFold ${TARGET_FOLD} -foldNum ${CROSSVAL} -d $< | \
		tomikesparse.py fre 2> $@.info | \
		split.py  2> $*.tefre.runmk | gzip > $*.trfre.runmk.gz
	runmike.py ${VERBOSE} -info $@.info -i ${ITER} -te $*.tefre.runmk -tr $*.trfre.runmk.gz -seed ${SEED}

### Wordsub Train-Test
%.wsub.runmk: %.wsub.gz 
	-rm $*.tewsub.runmk.gz
	crossval.py -seed ${SEED} -tarFold ${TARGET_FOLD} -foldNum ${CROSSVAL} -d $< | \
		sub2mikeSimple.py 2> $@.info | \
		split.py  2> $*.tewsub.runmk | gzip > $*.trwsub.runmk.gz
	runmike.py ${VERBOSE} -info $@.info -i ${ITER} -te $*.tewsub.runmk -tr $*.trwsub.runmk.gz -seed ${SEED}

## ALL-Data Split Train-Test
EXP_CROSSVAL=10
EXP_ITER=100000
ARGS_FRAME=7

### FRAME EXPERIMENTS
split.frame.out: anne.fre.gz aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz 
	splitframe-args.py ${EXP_ITER} ${EXP_CROSSVAL} ${SEED} all | xargs -n${ARGS_FRAME} -P${NCPU} splitframerun.pl > $@

%.frame.out: %.fre.gz
	-rm $*.*.fold*.out
	splitframe-args.py ${EXP_ITER} ${EXP_CROSSVAL} ${SEED} $* | xargs -n${ARGS_FRAME} -P${NCPU} splitframerun.pl > $@
	ls $*.fle.fold*.out | analyzetags.py > $*.fle.${EXP_ITER}.anl
	ls $*.fre.fold*.out | analyzetags.py > $*.fre.${EXP_ITER}.anl
	ls $*.pr.fold*.out | analyzetags.py > $*.pr.${EXP_ITER}.anl
	ls $*.ps.fold*.out | analyzetags.py > $*.ps.${EXP_ITER}.anl
	-mkdir -p ${RESULTS_PATH}${EXP_ITER}
	mv $*.*.fold*.out ${RESULTS_PATH}${EXP_ITER}
	cp $@ ${RESULTS_PATH}${EXP_ITER}

split.frame.plot: split.frame.out
	-rm $@
	for label in anne aran eve naomi nina peter; do\
		echo "$$label scores" >> $@; \
		cat $< | plotdata.pl 3=$$label 4=x 5=y >> $@ ;\
	done

%.frame.plot: %.frame.out
	cat $< | plotdata.pl 3=$* 4=x 5=y > $@ 

### WORDSUB EXPERIMENTS
ARGS_WSUB=7

split.wsub.out: anne.sub.gz aran.sub.gz eve.sub.gz naomi.sub.gz nina.sub.gz peter.sub.gz anne.fre.gz	 aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	splitwordsub-args.py ${EXP_ITER} ${EXP_CROSSVAL} ${SEED} all | xargs -n${ARGS_WSUB} -P${NCPU} splitwordsubrun.pl > $@

%.wsub.out: %.sub.gz %.fre.gz
	splitwordsub-args.py ${EXP_ITER} ${EXP_CROSSVAL} ${SEED} $* | xargs -n${ARGS_WSUB} -P${NCPU} splitwordsubrun.pl > $@
#	ls $*.wsub.fold*.out | analyzetags.py > $*.fixwsub${EXP_ITER}.anl
	-mkdir -p ${RESULTS_PATH}${EXP_ITER}
	mv $*.wsub*.fold*.out ${RESULTS_PATH}${EXP_ITER}
	cp $@ ${RESULTS_PATH}${EXP_ITER}

split.wsub.plot: split.wsub.out
	-rm $@
	for label in anne aran eve naomi nina peter; do\
		echo "$$label scores" >> $@; \
		cat $< | plotdata.pl 4=$$label 3=x 5=y >> $@ ;\
	done

%.wsub.plot: %.wsub.out
	cat $< | plotdata.pl 4=$* 3=x 5=y > $@

### FIX WORDSUB EXPERIMENTS
## This experiments assumes fixed number of substitutes
## Run the previous experiments to determine the best number of subsititutes.

FSUB_EXP_CROSSVAL=10
FSUB_EXP_ITER=10
FSUB_ARGS_WSUB=7
FSUB_SUBS=16

split.fixwsub.out: anne.sub.gz aran.sub.gz eve.sub.gz naomi.sub.gz nina.sub.gz peter.sub.gz anne.fre.gz	 aran.fre.gz eve.fre.gz naomi.fre.gz nina.fre.gz peter.fre.gz
	splitwordsub-args.py ${FSUB_EXP_ITER} ${FSUB_EXP_CROSSVAL} ${SEED} all | perl -lane 'print if $$F[3] == ${FSUB_SUBS}' | xargs -n${FSUB_ARGS_WSUB} -P${NCPU} splitwordsubrun.pl > $@

%.fixwsub.out: %.sub.gz %.fre.gz
	splitwordsub-args.py ${FSUB_EXP_ITER} ${FSUB_EXP_CROSSVAL} ${SEED} $* |perl -lane 'print if $$F[3] == ${FSUB_SUBS}'| xargs -n${FSUB_ARGS_WSUB} -P${NCPU} splitwordsubrun.pl > $@			
	ls $*.wsub${FSUB_SUBS}.fold*.out | analyzetags.py > $*.fixwsub${FSUB_EXP_ITER}.anl
	-mkdir -p ${RESULTS_PATH}${FSUB_EXP_ITER}
	mv $*.wsub*.fold*.out ${RESULTS_PATH}${FSUB_EXP_ITER}
	cp $@ ${RESULTS_PATH}${FSUB_EXP_ITER}

split.fixwsub.plot: split.fixwsub.out
	-rm $@
	for label in anne aran eve naomi nina peter; do\
		echo "$$label scores" >> $@; \
		cat $< | plotdata.pl 4=$$label 3=x 5=y >> $@ ;\
	done

%.fixwsub.plot: %.fixwsub.out
	cat $< | plotdata.pl 4=$* 3=x 5=y > $@

### DATA Statistics

DATA_NUMSUB=16
DATA_WSUBFEAT=9
wsub.stat:	anne.wsub.out aran.wsub.out eve.wsub.out naomi.wsub.out nina.wsub.out peter.wsub.out 
	-rm $@
	for label in anne aran eve naomi nina peter; do\
		echo "$$label" >> $@; \
		cat $$label.wsub.out | perl -lane 'if ($$F[3] == ${DATA_NUMSUB}) {$$c+=1; $$t += $$F[${DATA_WSUBFEAT}]; $$t2 += $$F[${DATA_WSUBFEAT}]**2;} END{print $$t/$$c . " ". ($$t2/$$c - ($$t/$$c)**2)**.5 }' >> $@;\
	done

DATA_FRAME=4
DATA_FRAMEFEAT=9
frame.stat: anne.frame.out aran.frame.out eve.frame.out naomi.frame.out nina.frame.out peter.frame.out 
	-rm $@
	for label in anne aran eve naomi nina peter; do\
		echo "$$label" >> $@; \
		cat $$label.frame.out | perl -lane '$$t->{$$F[${DATA_FRAME}]}{_C_} += $$F[${DATA_FRAMEFEAT}]; $$t->{$$F[${DATA_FRAME}]}{_A_} += 1; END{foreach (keys %$$t) {print "$$_ ". $$t->{$$_}{_C_} / $$t->{$$_}{_A_};}}' >> $@;\
	done


### FREQUENT (AXB), FLEXIBLE(AX + XB) and BIGRAM FRAMES (AX and XB)
FRAME_THR=0
MINTZ03_OPTIONS=-t ${FRAME_THR} -u 

#also equivalent to FLEXIBLE
%.fre.gz: %.data.gz
	zcat $< | frame.py  -n ${LM_NGRAM} ${MINTZ03_OPTIONS} 2> $*.fre.stat |gzip > $@ 

%.prbi.gz: %.data.gz
	zcat $< | frame.py  -f prbi ${MINTZ03_OPTIONS} 2> $*.prbi.stat |gzip > $@ 

%.psbi.gz: %.data.gz
	zcat $< | frame.py  -f psbi ${MINTZ03_OPTIONS} 2> $*.psbi.stat |gzip > $@ 

%.word.gz: %.fre.gz
	zcat $< | cut -f 3 | gzip > $@

%.pos.gz: %.fre.gz
	zcat $< | cut -f 4 | gzip > $*.pos.gz

%.gold.gz: %.fre.gz
	zcat $< | cut -f 2 | gzip > $*.gold.gz

#%.eval: %.pos.gz %.gold.gz
#	zcat $< | eval.pl -c -m -v -g $*.gold.gz 2> $@

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


%.runmk: %.mike.gz
	runmike.py $<.info ${ITER}

## EXPERIMENTS

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

.PRECIOUS: train.lm.gz train.vocab.gz %.fre.gz %.prbi.gz %.psbi.gz %.word.gz %.pos.gz %.gold.gz %.data.gz %.fle.nn %.psbi.nn %.prbi.nn %.fre.nn %.psbi.mike.gz %.prbi.mike.gz %.apsbi.mike.gz %.aprbi.mike.gz %.fre.mike.gz %.fle.mike.gz %.runmk %.sub.gz %.wordsub.mike.gz %.pairs.gz %.wordsub.out %.trws.fre.stat %.trws.mike.gz %.split.fre.stat %.trfle.mike.gz %.trfre.mike.gz %.scode.gz %.kmeans.gz %.wpairs.gz

clean:
	-rm *.fre.* *.prbi.* *.psbi.*

clean.all:
	-rm *data.gz 
	-rm *.err
	-rm *.fre* *.prbi* *.psbi*
