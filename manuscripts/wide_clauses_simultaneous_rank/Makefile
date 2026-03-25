PDF=wide_clauses_simultaneous_rank.pdf
TEX=wide_clauses_simultaneous_rank.tex

all:
	latexmk -pdf -interaction=nonstopmode $(TEX)

clean:
	latexmk -C
	rm -f *.bbl *.blg *.out *.toc *.aux *.log
