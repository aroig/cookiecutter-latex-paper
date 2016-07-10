README
======

## How to compile
To produce a pdf file:
    
    make -B pdf
  
To produce a tarred source distribution:

    make -B src



## Compile Dependencies
This code depends on some tools in order to be compiled properly:

* lualatex: distributed with texlive since 2010.
  http://www.tug.org/texlive/


  
Optional dependencies:

* pgf/tikz: For graphics and commutative diagrams.
  http://pgf.sourceforge.net/
  
* impose+: To produce 2-in-1 pdf's.
  
* texa: To manipulate the source tree.
  https://github.com/aroig/texa
  
* git: For versioning the code.
  http://git-scm.com/
  
* latexdiff: Used for producing highlighted diff pdfs when under git. latexdiff
  is distributed with texlive, for instance.

 

Makefile targets
----------------

* clean: Clean output and temporal files.

* diff: Produce a pdf from a diff tex file. Requires texa to generate the diffs and
  latexdiff to compile.

* figs: Compile the figures if they need compiling.

* flat: Produce a pdf from flattened source code.

* flatsrc: Produce flattened source code, with personal commands replaced, so it compiles
  with the minimal requirements possible. Requires texa.
  
* pdf: Produce a pdf.

* 2in1: Produce a 2-in-1 pdf. Requires impose+.

* src: Produce a source tarball.

* view: Open pdf.

      

