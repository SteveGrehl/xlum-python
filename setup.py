from distutils.core import setup
# see: https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application
setup(
    name="xlum-python",
    packages=["xlum", "xlum/data", "xlum/test"],
    version="0.0",  # Ideally should be same as your GitHub release tag version
    description="python importer for the XLUM data exchange and archive format",
    author="Grehl, Steve",
    author_email="research@steve-grehl.eu",
    url="https://github.com/SteveGrehl/xlum-python",
    download_url="https://github.com/SteveGrehl/xlum-python/archive/refs/heads/main.zip",
    keywords=[],
    classifiers=[],
)
