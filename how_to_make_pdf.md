## Call sphinx

```
make latexpdf
```

## Open `_build/latex/Pythonista.tex`
remove \PYGZbs{} from the file

if using bash,
grep -l '\\PYGZbs{}' Pythonistas.tex | xargs sed -i.bak -e 's/\\PYGZbs{}//g'

## compile
```
platex Pythonistas.tex
dvipdfmx Pythonistas.dvi
```
