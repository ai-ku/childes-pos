MINTZ_DATA_PATH=../data/childes/mintz03xml/
SRC_PATH=../src/

all: mintz03 clair10pr clair10ps
data: anne.data.gz aran.data.gz eve.data.gz naomi.data.gz nina.data.gz peter.data.gz

mintz03: anne.fre.eval aran.fre.eval eve.fre.eval naomi.fre.eval nina.fre.eval peter.fre.eval
clair10pr: anne.prbi.eval aran.prbi.eval eve.prbi.eval naomi.prbi.eval nina.prbi.eval peter.prbi.eval
clair10ps: anne.psbi.eval aran.psbi.eval eve.psbi.eval naomi.psbi.eval nina.psbi.eval peter.psbi.eval

%.data.gz:
	ls ${MINTZ_DATA_PATH}$*/*.xml | ${SRC_PATH}childes.pl 2> $*.err | gzip > $@ &


# Constructs answer files of the top  frames
FRAME_THR=0
MINTZ03_OPTIONS=-t ${FRAME_THR} -g -u 
%.fre.gz: %.data.gz
	zcat $< | ${SRC_PATH}frame.py  ${MINTZ03_OPTIONS} 2> $*.fre.stat |gzip > $@ 

%.prbi.gz: %.data.gz
	zcat $< | ${SRC_PATH}frame.py  -f prbi ${MINTZ03_OPTIONS} 2> $*.prbi.stat |gzip > $@ 

%.psbi.gz: %.data.gz
	zcat $< | ${SRC_PATH}frame.py  -f psbi ${MINTZ03_OPTIONS} 2> $*.psbi.stat |gzip > $@ 

%.word.gz: %.gz
	zcat $< | cut -f 1 | gzip > $@

%.pos.gz: %.gz
	zcat $< | cut -f 3 | gzip > $*.pos.gz

%.gold.gz: %.gz
	zcat $< | cut -f 2 | gzip > $*.gold.gz


%.eval: %.pos.gz %.gold.gz
	zcat $< | ${SRC_PATH}eval.pl -c -m -v -g $*.gold.gz 2> $@

%.dist: %.gz
	zcat $< | perl -lane '$$h{$$F[1]}++;END{print "$$_ $$h{$$_}" foreach keys(%h)}'


## FANN Neural Network
neural.data: anne.neural aran.neural eve.neural naomi.neural nina.neural peter.neural

anne.neural: anne.fre.nn anne.psbi.nn anne.prbi.nn
aran.neural: aran.fre.nn aran.psbi.nn aran.prbi.nn
eve.neural: eve.fre.nn eve.psbi.nn eve.prbi.nn
naomi.neural: naomi.fre.nn naomi.psbi.nn naomi.prbi.nn
nina.neural: nina.fre.nn nina.psbi.nn nina.prbi.nn
peter.neural: peter.fre.nn peter.psbi.nn peter.prbi.nn

anne.run:	anne.fre.run anne.fle.run anne.prbi.run anne.psbi.run
aran.run:	aran.fre.run aran.fle.run aran.prbi.run aran.psbi.run
eve.run:	eve.fre.run eve.fle.run eve.prbi.run eve.psbi.run
naomi.run:	naomi.fre.run naomi.fle.run naomi.prbi.run naomi.psbi.run
nina.run:	nina.fre.run nina.fle.run nina.prbi.run nina.psbi.run
peter.run:	peter.fre.run peter.fle.run peter.prbi.run peter.psbi.run

%.fre.nn: %.fre.gz
	../src/tofnn.py $< fre > $@

%.fle.nn: %.fre.gz
	../src/tofnn.py $< fle > $@

%.psbi.nn: %.fre.gz
	../src/tofnn.py $< ps > $@

%.prbi.nn: %.fre.gz
	../src/tofnn.py $< pr > $@

SAMPLE_SIZE=10000

%.fre.run: %.fre.nn
	../src/simple_train $<  ${SAMPLE_SIZE} > $@ 2> $@.err &

%.fle.run: %.fle.nn
	../src/simple_train $< ${SAMPLE_SIZE} > $@ 2> $@.err &

%.psbi.run: %.psbi.nn
	../src/simple_train $<  ${SAMPLE_SIZE} > $@ 2> $@.err &

%.prbi.run: %.prbi.nn
	../src/simple_train $<  ${SAMPLE_SIZE} > $@ 2> $@.err &


## MIKENET Neural Network
mikenet.data:	anne.mikenet aran.mikenet eve.mikenet naomi.mikenet nina.mikenet peter.mikenet

%.mikenet: %.fre.runmk %.psbi.runmk %.prbi.runmk %.fle.runmk %.apsbi.runmk %.aprbi.runmk
	echo $@


%.fre.mike: %.fre.gz
	../src/tomike.py $< fre > $@ 2> $@.info

%.fle.mike: %.fre.gz
	../src/tomike.py $< fle > $@ 2> $@.info

%.psbi.mike: %.fre.gz
	../src/tomike.py $< ps > $@ 2> $@.info

%.apsbi.mike: %.psbi.gz
	../src/tomike.py $< ps > $@ 2> $@.info

%.prbi.mike: %.fre.gz
	../src/tomike.py $< pr > $@ 2> $@.info

%.aprbi.mike: %.prbi.gz
	../src/tomike.py $< pr > $@ 2> $@.info

%.runmk: %.mike
	../src/runmike.py $<.info

.PRECIOUS: %.fre.gz %.prbi.gz %.psbi.gz %.word.gz %.pos.gz %.gold.gz %.data.gz %.fle.nn %.psbi.nn %.prbi.nn %.fre.nn %.psbi.mike %.prbi.mike %.apsbi.mike %.aprbi.mike %.fre.mike %.fle.mike %.runmk


clean:
	-rm *.fre.* *.prbi.* *.psbi.*

clean.all:
	-rm *data.gz 
	-rm *.err
	-rm *.fre* *.prbi* *.psbi*