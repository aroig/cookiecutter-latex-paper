# Copyright (c) {{ cookiecutter.date.split('-')[0] }}, {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>
# All rights reserved.


#----------------------------------#
# Variables                        #
#----------------------------------#

# Software
LATEX      := lualatex
DIFFLATEX  := difflatex
BIBTEX     := biber

# Latexdiff config
LATEXDIFF_IGNORE   := picture tikzpicture tikzcd DIFnomarkup
LATEXDIFF_PACKAGES := amsmath hyperref

# Execution flags
LATEX_FLAGS     := --shell-escape --halt-on-error --interaction=nonstopmode --synctex=1
LATEXDIFF_FLAGS := --packages=$(subst ' ',',',$(LATEXDIFF_PACKAGES)) \
                   --config "PICTUREENV=(?:$(subst ' ',|,$(LATEXDIFF_IGNORE)))[\w\d*@]*"


#----------------------------------#
# Directories                      #
#----------------------------------#

BLDDIR     := ./build
FIGDIR     := ./figs
LIBDIR     := ./lib
TEXDIR     := ./tex
BINDIR     := ./bin
REFDIR     := ./ref
FLATDIR    := ./build/flat
DIFFDIR    := ./build/diff


#----------------------------------#
# Source Files                     #
#----------------------------------#

METADATA   := metadata.bib
DOCTYPE    := {{cookiecutter.project_type}}
DOCID      := $(shell perl -ne '/\@article[a-zA-Z{]*:(.*),/ && print "$$1\n"' $(METADATA))
REF        := HEAD

MKPREAMBLE := bin/mkpreamble.py
PREAMBLE   := preamble.tex
GITREF     := gitref

FIGFILES   := $(sort $(wildcard $(FIGDIR)/*.png) $(wildcard $(FIGDIR)/*.pdf))
LIBFILES   := $(sort $(wildcard *.sty) $(wildcard $(LIBDIR)/*))
BIBFILES   := $(sort $(wildcard *.bib))
TEXFILES   := $(sort $(wildcard *.tex) $(wildcard $(TEXDIR)/*.tex) $(PREAMBLE))
AUXFILES   := $(patsubst %.tex,$(notdir %.aux),$(TEXFILES))
TOCFILES   := $(DOCID).toc

BLDFILES   := Makefile .gitignore README.md $(METADATA) $(MKPREAMBLE)
BLDFILES   := $(foreach f,$(BLDFILES),$(wildcard $(f)))


#----------------------------------#
# Functions                        #
#----------------------------------#

# setup environment for some commands
latex-environment  = TEXINPUTS="$1:$(LIBDIR):$(TEXDIR):$(FIGDIR):" LUAINPUTS="$1:$(LIBDIR):"
lua-environment    = LUA_PATH="$(LIBDIR)/?.lua"

# extract tex file dependencies
latex-dependencies = $1.tex $(foreach p,\
	$(shell perl -ne '/^\s*\\(input|include)\{(.*?)(.tex)?\}/ && print "$$2.tex "' $1.tex),\
	$(dir $1)$(p)\
)

# bibliography files
doc-dependencies = $(call latex-dependencies,$1) $(BLDDIR)/$1.bbl $(PREAMBLE) $(LIBFILES) $(FIGFILES)

# write string $2 to file $1 only if it is different from its contents.
write-if-changed-cmd = if [ ! -f "$2" ] || [ ! "$1" = "`cat $2 2> /dev/null`" ]; then echo "$1" > "$2"; fi


#----------------------------------#
# Abstract rules                   #
#----------------------------------#

# set vpath so make finds the source files
VPATH       := $(LIBDIR):$(TEXDIR):$(FIGDIR)

# shell settings
SHELL       := /usr/bin/bash
.SHELLFLAGS := -e -u -c

.ONESHELL:

# So we can use $$(variable) on the prerequisites, that expand at matching time
.SECONDEXPANSION:

# never handle as intermediate targets but never delete them
.SECONDARY:

# always trigger rebuilds on those
.PHONY: update pdf 2in1 src flat flatsrc diff figs clean slideshow view ref bib test

all: pdf

pdf: $(DOCID).pdf $(DOCID).synctex.gz

2in1: $(DOCID).2in1.pdf

src: $(DOCID).tar.gz

flat: $(FLATDIR)/$(DOCID).pdf

flatsrc: $(FLATDIR)/$(DOCID).tar.gz

diff: $(DIFFDIR)/$(DOCID).pdf

figs: $(FIGFILES)

clean:
	rm -Rf $(BLDDIR) $(FLATDIR) $(DIFFDIR)
	rm -Rf *.pdf *.tar.gz *.synctex.gz


#----------------------------------#
# Generic file rules               #
#----------------------------------#

# add dependency to force always rebuild but still checking the file timestamps.
FORCE:

# create file with a hash, used to track modifications to the original file
$(BLDDIR)/%.sha: $(BLDDIR)/%
	@mkdir -p $(dir $@)
	SHA="`sha256sum '$<'`"; $(call write-if-changed-cmd,$$SHA,$@)

# convert pdf to ps
$(BLDDIR)/%.ps: $(BLDDIR)/%.pdf
	pdftops -paper A4 $< $@

# make a 2in1 ps
$(BLDDIR)/%.ps.imposed: $(BLDDIR)/%.ps
	cd $(dir $<); impose $(notdir $<)

# make a 2in1 pdf
%.2in1.pdf: $(BLDDIR)/%.ps.imposed
	ps2pdf -sPAPERSIZE=a4 $< $@

# copy files from the build directory
%.pdf: $(BLDDIR)/%.pdf
	cp $< $@

%.synctex.gz: $(BLDDIR)/%.pdf
	cp "$(BLDDIR)/$*.synctex.gz" "$@"

%.tar.gz: $(BLDDIR)/%.tar.gz
	cp $< $@


#----------------------------------#
# Git rules                        #
#----------------------------------#

$(BLDDIR)/$(GITREF): FORCE
	@mkdir -p $(dir $@)
	$(call write-if-changed-cmd,$(shell git describe --always --tags --dirty=+),$@)

$(DIFFDIR)/$(GITREF): FORCE
	@mkdir -p $(dir $@)
	$(call write-if-changed-cmd,$(shell git describe --always --tags $(REF)),$@)

$(DIFFDIR)/old/%.tex: $(DIFFDIR)/$(GITREF)
	@mkdir -p $(dir $@)
	git show $(shell cat $<):$*.tex > $@


#----------------------------------#
# Preamble and bibliography        #
#----------------------------------#

# create a preamble tex file
$(PREAMBLE): $(MKPREAMBLE) $(METADATA)
	@python $^ > $@

# precompile headers
$(BLDDIR)/preamble.fmt: $(PREAMBLE)
	@mkdir -p $(dir $@)
	$(call latex-environment,$(dir $<)) $(LATEX) $(LATEX_FLAGS) -ini -job-name="preamble" "&lualatex $<\dump" --output-directory=$(dir $@) $<

# compile document to produce the bcf file. we do not want to rebuild on every tex file change.
$(BLDDIR)/%.bcf: | $$(call latex-dependencies,%)
	@mkdir -p $(dir $@)
	$(call latex-environment,$(dir $<)) $(LATEX) $(LATEX_FLAGS) --draftmode --output-directory=$(dir $@) $*.tex

# prepare bibliography when bibliography file changes. Do not rebuild when bcf file changes.
$(BLDDIR)/%.bbl: $(BIBFILES) | $(BLDDIR)/%.bcf
	@mkdir -p $(dir $@)
	$(BIBTEX) --input-directory=$(dir $@) --output-directory=$(dir $@) $*.bcf


#----------------------------------#
# Document                         #
#----------------------------------#

# compile pdf with up to date bibliography
$(BLDDIR)/%.pdf: %.tex $$(call doc-dependencies,%) | $(BLDDIR)/$(GITREF)
	@mkdir -p $(dir $@)
	$(call latex-environment,$(dir $<)) $(LATEX) $(LATEX_FLAGS) --output-directory=$(dir $@) $<

# compile one chapter alone
$(BLDDIR)/chapter-%.pdf: $(TEXDIR)/%.tex $(PREAMBLE) $(FIGFILES) | $(BLDDIR)/$(GITREF)
	@mkdir -p $(dir $@)
	$(call latex-environment,$(dir $<)) $(LATEX) $(LATEX_FLAGS) --output-directory=$(dir $@) \
		-jobname=chapter-$* "\\includeonly{$<}\\input{$(DOCID).tex}"

# make a tar.gz package of the sources
$(BLDDIR)/%.tar.gz: %.tex $$(call doc-dependencies) $(BIBFILES) $(BLDFILES)
	@mkdir -p $(dir $@)
	tar -cz -f $@ $(patsubst ./%,%,$^)

# make a tikz figure
$(FIGDIR)/%.pdf: $(FIGDIR)/%.tex
	@( cd $(FIGDIR); $(LATEX) --jobname=$* --output-directory=$(BLDDIR) $(notdir $<) )
	cp $(BLDDIR)/$*.pdf $@


#----------------------------------#
# Make diff and flat               #
#----------------------------------#

# flatten sources
$(FLATDIR)/%.tex: %.tex
	@mkdir -p $(dir $@)
	latexpand -o $@ $<

$(DIFFDIR)/%.tex: $(DIFFDIR)/old/%.tex %.tex
	@mkdir -p $(dir $@)
	latexdiff $(LATEXDIFF_FLAGS) $^ > $@


#----------------------------------#
# Miscelania rules                 #
#----------------------------------#

# Update cookiecutter template for the project and merge it with current branch
TEMPLATE_URL_paper  := latex:paper
TEMPLATE_URL_book   := latex:paper
TEMPLATE_URL_notes  := latex:paper
TEMPLATE_URL_slides := latex:slides
TEMPLATE_URL_poster := latex:slides

update-template:
	@python make/cookiecutter-update.py "$(TEMPLATE_URL_$(DOCTYPE))" template

# prepare a tree of symlinks to the bibliography
ref-tree:
	rm -Rf $(REFDIR)
	cali lktree --classifier=flat "tag:paper:$(DOCID)" $(REFDIR)

# autogenerate bibliography from citation keys
auto-bib:
	cali find --fmt=bib "tag:paper:$(DOCID)" > $(DOCID).auto.bib

# view pdf
view:
	xdg-open $(DOCID).pdf &

# make a slideshow
slideshow:
	pdfpc $(DOCID).pdf &

test:
