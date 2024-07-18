.PHONY : all results clean help settings

COUNT=bin/countwords.py
DATA=$(wildcard data/*.txt)
RESULTS=$(patsubst data/%.txt,results/%.csv,$(DATA))
COLLATE=bin/collate.py
PLOT=bin/plotcounts.py
SUMMARY=bin/book_summary.sh

## all :  Regenerate all results
all : results/collated.png

## results/collated.png : Plot the collated results
results/collated.png : results/collated.csv
	python3 $(PLOT) $< --outfile $@

## results/collated.csv : Collate all results
results/collated.csv : $(RESULTS) $(COLLATE)
	mkdir -p results
	python3 $(COLLATE) $(RESULTS) > $@

## results/%.csv : Regenerate results for any book
results/%.csv : data/%.txt $(COUNT)
	@$(SUMMARY) $< 'Title'
	@$(SUMMARY) $< 'Author'
	python3 $(COUNT) $< > $@

## results : Regenerate results for all books
results : $(RESULTS)

## clean : Remove all generated files
clean :
	rm $(RESULTS) results/collated.csv results/collated.png

## settings : Show variable's values
settings :
	@echo COUNT: $(COUNT)
	@echo DATA: $(DATA)
	@echo RESULTS: $(RESULTS)
	@echo COLLATE: $(COLLATE)
	@echo PLOT: $(PLOT)
	@echo SUMMARY: $(SUMMARY)

## help : Show this message
help :
	@grep '^##' ./Makefile
