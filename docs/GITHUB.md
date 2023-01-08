# xlum <img width=120px src="img/xlum-python_logo.png" align="right" />

Python importer for the [XLUM data exchange and archive format](https://github.com/R-Lum/xlum_specification)
You may install `xlum` using pip:
```console
$ pip install xlum
```

## System requirements

- lxml https://pypi.org/project/lxml/
- pandas https://pandas.pydata.org/
- urllib3 https://urllib3.readthedocs.io/en/stable/
- openpyxl https://openpyxl.readthedocs.io/en/stable/
- Access to GitHub for XSD schema validation
  
## Setting up Conda (optional)

[Conda](https://conda.io) is an open-source package and environment management system that runs on Windows, macOS, Linux, and z/OS. Conda quickly installs, runs and updates packages and their dependencies. Conda easily creates, saves, loads and switches between environments on your local computer. It was created for Python programs but can package and distribute software for any language.

Tutorial: https://towardsdatascience.com/how-to-set-up-anaconda-and-jupyter-notebook-the-right-way-de3b7623ea4a

```console
$ conda env create --prefix ./env --file environment.yml; conda activate ./env
```

The installation of Conda is optional, but highly recommended.

### Adding Jupyter support  (optional)

The [Jupyter](https://jupyter.org) Notebook is a web-based interactive computing platform. The notebook combines live code, equations, narrative text, visualizations and many more.
More information can be found on https://jupyter.org/.

```console
$ conda install jupyter notebook ipykernel matplotlib
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

## Funding

The development of the XLUM-format as format basis for reference data was supported by the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No 844457 [CREDit](https://cordis.europa.eu/project/id/844457)).
