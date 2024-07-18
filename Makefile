.PHONY : all clean

COUNT=bin/countwords.py
RUN_COUNT=python3 $(COUNT)

# Regenerate all results
all : results/moby_dick.csv results/jane_eyre.csv results/time_machine.csv

# Regenerate results for any book
results/%.csv : data/%.txt $(COUNT)
	$(RUN_COUNT) $< > $@

# Regenerate results for "Jane Eyre°
results/jane_eyre.csv : data/jane_eyre.txt $(COUNT)
	$(RUN_COUNT) $< > $@

# Remove all generated files
clean :
	rm -f results/*.csv
