parse:
	poetry run run

build:
	poetry run cc
	llc out.ll -o out.s

