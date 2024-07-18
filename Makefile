.PHONY : all clean help  settings

COUNT=bin/countwords.py
DATA=$(wildcard data/*.txt)
RESULTS=$(patsubst data/%.txt,results/%.csv,$(DATA))

## all :  Regenerate all results
all : $(RESULTS)

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

## help : show this message
help :
	@grep '^##' ./Makefile
