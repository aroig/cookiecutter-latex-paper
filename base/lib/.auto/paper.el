(TeX-add-style-hook
 "paper"
 (lambda ()
   (TeX-run-style-hooks
    "scrartcl"
    "scrartcl10"
    "abdokoma")
   (TeX-add-symbols
    "documentclassname")))

