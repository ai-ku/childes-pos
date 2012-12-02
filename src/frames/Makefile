all: mintz03 clair10pr clair10ps

DATAPATH=../

mintz03: anne.fre45.eval aran.fre45.eval eve.fre45.eval naomi.fre45.eval nina.fre45.eval peter.fre45.eval
clair10pr: anne.prbi45.eval aran.prbi45.eval eve.prbi45.eval naomi.prbi45.eval nina.prbi45.eval peter.prbi45.eval
clair10ps: anne.psbi45.eval aran.psbi45.eval eve.psbi45.eval naomi.psbi45.eval nina.psbi45.eval peter.psbi45.eval


# Constructs anwer files of the top 45 frames
FRAME_THR=45
MINTZ03_OPTIONS=-t ${FRAME_THR} -g -u 
%.fre45.gz: ${DATAPATH}%.data.gz
	zcat $< | ./frame.py  ${MINTZ03_OPTIONS} 2> $*.fre45.stat |gzip > $@ 

%.prbi45.gz: ${DATAPATH}%.data.gz
	zcat $< | ./frame.py  -f prbi ${MINTZ03_OPTIONS} 2> $*.prbi45.stat |gzip > $@ 

%.psbi45.gz: ${DATAPATH}%.data.gz
	zcat $< | ./frame.py  -f psbi ${MINTZ03_OPTIONS} 2> $*.psbi45.stat |gzip > $@ 

%.word.gz: %.gz
	zcat $< | cut -f 1 | gzip > $@

%.pos.gz: %.gz
	zcat $< | cut -f 3 | gzip > $*.pos.gz

%.gold.gz: %.gz
	zcat $< | cut -f 2 | gzip > $*.gold.gz


%.eval: %.pos.gz %.gold.gz
	zcat $< | ../eval.pl -c -m -v -g $*.gold.gz 2> $@

%.dist: %.gz
	zcat $< | perl -lane '$$h{$$F[1]}++;END{print "$$_ $$h{$$_}" foreach keys(%h)}'

clean:
	-rm *.fre45.* *.prbi45.* *.psbi45.*

.PRECIOUS: %.fre45.gz %.prbi45.gz %.psbi45.gz %.word.gz %.pos.gz %.gold.gz 