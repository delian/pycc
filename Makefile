parse:
	poetry run run

build:
	poetry run cc
	llc out.ll -o out.s -march=arm -mcpu=cortex-a53
	llc out.ll -o out.o -march=x86-64 -filetype=obj
	clang out.o -o out	
	opt -S out.ll -passes=dot-callgraph -o out.dot
	dot -Tpng out.dot -o out.png




