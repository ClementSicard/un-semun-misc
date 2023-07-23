COUNTRIES_FILE_PATH := ./data/countries.xlsx
UN_BODIES_FILE_PATH := ./data/unbodies.csv

.PHONY: all
all: run-countries run-un-bodies

.PHONY: run-countries
run-countries:
	poetry run python src/countries.py -f $(COUNTRIES_FILE_PATH)

.PHONY: run-un-bodies
run-un-bodies:
	poetry run python src/unbodies.py -f $(UN_BODIES_FILE_PATH)
