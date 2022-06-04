# xlum-python
Python importer for https://github.com/R-Lum/xlum_specification

## Requirements

- lxml https://pypi.org/project/lxml/
- pytest https://pypi.org/project/pytest/
  
## Setting Up Conda

```
conda create --name xlum lxml pytest; conda activate xlum
```

## Usage
 ```
 import xlum

 meta_obj = xlum.importer.from_xlum(file_name="<Path to Xlum>")
  ```

## Citing
```
<Comming Soon>
```