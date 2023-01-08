import pytest
import os
import urllib
from xlum.data.classes import XlumMeta
import xlum.importer as importer


def get_assets_dir() -> os.PathLike:
    """return path to assets folder

    Returns:
        os.PathLike: path to assets folder
    """
    assets_dir = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-1]
    if os.name == "posix":
        assets_dir = os.path.join(os.sep, *assets_dir, "assets")
    elif os.name == "nt":
        assets_dir = os.path.join(assets_dir[0], os.sep,  *assets_dir[1:], "assets")
    else:
        assert False, f"{os.name=} not supported"
    assert os.path.isdir(assets_dir), f"{assets_dir=} not found"
    return assets_dir


@pytest.mark.parametrize("fn", [("xlum_prototype.xlum"), ("xlum_prototype_b64.xlum")])
def test_import(fn: os.PathLike) -> None:
    """test if a file can be imported

    Args:
        fn (str): path to file
    """
    full_path = os.path.join(get_assets_dir(), fn)
    assert os.path.isfile(full_path), f"{full_path=} is not a file"
    assert isinstance(importer.from_xlum(full_path), XlumMeta)


@pytest.mark.parametrize("url", [('https://raw.githubusercontent.com/R-Lum/xlum_specification/master/examples/xlum_example.xlum')])
def test_gh_import(url: str) -> None:
    # Download example file
    local_dir = os.path.join(os.getcwd(), "tmp")
    local_path = os.path.join(local_dir, "example.xlum")
    if not os.path.exists(local_dir):
        os.mkdir(local_dir)
    urllib.request.urlretrieve(url, local_path)

    try:
        assert isinstance(importer.from_xlum(
            local_path
        ), XlumMeta)
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)
        if os.path.exists(local_dir):
            os.rmdir(local_dir)


@pytest.mark.parametrize("fn", [("xlum_invalid.xlum")])
@pytest.mark.xfail
def test_import_fails(fn: os.PathLike) -> None:
    full_path = os.path.join(get_assets_dir(), fn)
    assert os.path.isfile(full_path), f"{full_path=} is not a file"
    importer.from_xlum(full_path)
