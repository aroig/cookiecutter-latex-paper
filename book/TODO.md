TODO
====

* compile one chapter at a time and merge them afterwards. It would lead to a more
  efficient compilation.

        pdflatex -jobname=chapter-foo "\\includeonly{foo}\\input{master.tex}"
