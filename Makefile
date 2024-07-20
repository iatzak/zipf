.PHONY : all results clean help settings

include config.mk

DATA=$(wildcard data/*.txt)
RESULTS=$(patsubst data/%.txt,results/%.csv,$(DATA))

## all : Regenerate all results
all : results/collated.png

## results/collated.png : Plot the collated results
results/collated.png : results/collated.csv bin/plotparams.yml
	python3 $(PLOT) $< --outfile $@ --plotparams $(word 2,$^)

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

## help : Show all commands
help :
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' \
		| column -t -s ':'
