README
======

## How to compile
To produce a pdf file:
    
    make pdf
  
To produce a source distribution tarball:

    make src

To open the PDF output in a viewer

    make view

To rebuild everything, from scratch, bibliography pass, etc

    make -B pdf

To get a list of avaliable make targets

    make help


## Dependencies
* Standard linux environment with GNU make, perl, python and bash

* lualatex: distributed with texlive since 2010. http://www.tug.org/texlive/

* biber: to generate bibliographies. http://biblatex-biber.sourceforge.net/

  
Optional dependencies:

* pgf/tikz: For graphics and commutative diagrams.
  http://pgf.sourceforge.net/
  
* impose+: To produce 2-in-1 pdf's.
  
* git: For versioning the code.
  http://git-scm.com/
  
* latexdiff: Used for producing highlighted diff pdfs when under git. latexdiff
  is distributed with texlive, for instance.

 
