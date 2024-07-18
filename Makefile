.PHONY : all clean settings

COUNT=bin/countwords.py
DATA=$(wildcard data/*.txt)
RESULTS=$(patsubst data/%.txt,results/%.csv,$(DATA))

# Regenerate all results
all : $(RESULTS)

# Regenerate results for any book
results/%.csv : data/%.txt $(COUNT)
	python3 $(COUNT) $< > $@

# Remove all generated files
clean :
	rm -f results/*.csv

# Show variable's values
settings :
	@echo COUNT: $(COUNT)
	@echo DATA: $(DATA)
	@echo RESULTS: $(RESULTS)
