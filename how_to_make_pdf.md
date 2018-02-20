## Call sphinx

```
make latexpdf
```

## Open `_build/latex/Pythonista.tex`
remove \PYGZbs{} from the file

## compile
platex Pythonistas.tex
dvipdfmx Pythonistas.dvi


# Command
```
make latexpdf
cd _build/latex
grep -l '\\PYGZbs{}' Pythonistas.tex | xargs sed -i.bak -e 's/\\PYGZbs{}//g'
platex Pythonistas.tex
dvipdfmx Pythonistas.dvi
cd ../..
```
