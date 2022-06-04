# xlum-python
Python importer for https://github.com/R-Lum/xlum_specification

## Requirements

- lxml https://pypi.org/project/lxml/
- pytest https://pypi.org/project/pytest/
  
## Setting Up Conda

```console
$ conda env create --prefix ./env --file environment.yml; conda activate ./env
```

## Usage
 ```python
 import xlum

 meta_obj = xlum.importer.from_xlum(file_name="<Path to Xlum>")
  ```

## Citing
```
<Comming Soon>
```