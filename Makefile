.PHONY : all clean help  settings

COUNT=bin/countwords.py
DATA=$(wildcard data/*.txt)
RESULTS=$(patsubst data/%.txt,results/%.csv,$(DATA))
COLLATE=bin/collate.py

## all :  Regenerate all results
all : results/collated.csv

## results/collate.csv : Collate all results
results/collated.csv : $(RESULTS) $(COLLATE)
	mkdir -p results
	python3 $(COLLATE) $(RESULTS) > $@

## results/%.csv : Regenerate results for any book
results/%.csv : data/%.txt $(COUNT)
	python3 $(COUNT) $< > $@

## clean : Remove all generated files
clean :
	rm -f results/*.csv

## settings : Show variable's values
settings :
	@echo COUNT: $(COUNT)
	@echo DATA: $(DATA)
	@echo RESULTS: $(RESULTS)
	@echo COLLATE: $(COLLATE)

## help : show this message
help :
	@grep '^##' ./Makefile
