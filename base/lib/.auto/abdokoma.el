(TeX-add-style-hook
 "abdokoma"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("datetime" "nodayofweek") ("csquotes" "autostyle")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "etex"
    "iftex"
    "babel"
    "datetime"
    "geometry"
    "scrpage2"
    "titletoc"
    "csquotes"
    "amsmath"
    "xcolor"
    "graphicx"
    "tikz"
    "abdocolor"
    "abdoalias"
    "abdofonts"
    "abdothms"
    "draftools"
    "url"
    "hyperref")
   (TeX-add-symbols
    '("texorpdf" 2)
    '("setupsectioning" 1)
    "widelinespread"
    "regularlinespread"
    "regularheader"
    "hyperrefhook"
    "headerhook"
    "sectioninghook"
    "setupchapterpart"
    "emphold"
    "unfootnote")
   (LaTeX-add-lengths
    "headerlinethickness")))

