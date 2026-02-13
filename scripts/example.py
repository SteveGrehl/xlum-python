import logging
import os
import requests

import pandas as pd

import xlum.importer
from xlum.data.classes import Curve, Record, Sample, Sequence, XlumMeta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    # Download example file
    url = "https://raw.githubusercontent.com/R-Lum/xlum_specification/master/examples/xlum_example.xlum"
    logger.debug(f"Loading example data from: {url}")
    local_dir = os.path.join(os.getcwd(), "tmp")
    local_path = os.path.join(local_dir, "example.xlum")
    obj = None
    try:
        os.mkdir(local_dir)
        response = requests.get(url)
        with open(local_path, "wb") as file_ptr:
            file_ptr.write(response.content)
        obj: XlumMeta = xlum.importer.from_xlum(local_path)
        os.remove(local_path)
        logger.debug(
            "Imported example data as XlumMeta object. Removing local example data from disk."
        )
    except Exception as ex:
        logger.exception(ex)
    finally:
        os.rmdir(local_dir)
    if obj is None:
        logger.error("No data loaded.")
        return -1

    # Example data was received from the xlum specification repository.

    df_xlum: pd.DataFrame = obj.df
    print(obj.__class__.__name__, "DataFrame:\n", df_xlum, "\n-----------")
    for sample in obj.lstSamples:
        sample: Sample
        df_sequences: pd.DataFrame = sample.df
        print(sample.__class__.__name__, "DataFrame:\n", df_sequences, "\n-----------")
        for sequence in sample.lstSequences:
            sequence: Sequence
            df_records: pd.DataFrame = sequence.df
            print(
                sequence.__class__.__name__, "DataFrame:\n", df_records, "\n-----------"
            )
            for record in sequence.lstRecords:
                record: Record
                df_curves: pd.DataFrame = record.df
                print(
                    record.__class__.__name__,
                    "DataFrame:\n",
                    df_curves,
                    "\n-----------",
                )
                for curve in record.lstCurves:
                    curve: Curve
                    df_values: pd.DataFrame = curve.df
                    print(
                        curve.__class__.__name__,
                        "DataFrame:\n",
                        df_values,
                        "\n-----------",
                    )


if __name__ == "__main__":
    main()
