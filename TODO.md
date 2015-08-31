TODO
====

* track dependencies of `.aux` and `.toc` files.

* simplify scripts to create `preamble.tex`. I'd like to get rid of the python
  script. Extend to handle journal styles.

* Add build target to update templates via cookiecutter.

* Use template name as document subtype. There is no way to get the template name right
  now.

* Fix troubles with bibliography

* Make loud error messages when tex dependencies do not exist. I should proably
  instantiate rules explicitly instead of relying on complex pattern rules.

* move gitref stuff from `draftools.lua` to the Makefile. Want to general gitref.tex with
  the corresponding tex code for the header.


## paper


## book

* compile one chapter at a time and merge them afterwards. It would lead to a more
  efficient compilation.

        pdflatex -jobname=chapter-foo "\\includeonly{foo}\\input{master.tex}"
