
import sys
import logging
import os
import pandas as pd
from dataclasses import asdict

DIRNAME = os.path.dirname(__file__)
sys.path.append(
    os.path.join(
        DIRNAME,
        '../xlum')
)
from data.classes import XlumMeta, Sample, Record, Sequence, Curve
import importer

def main():
    logging.basicConfig(level=logging.DEBUG)

    obj: XlumMeta = importer.from_xlum(
        os.path.join(
            DIRNAME,
            "../assets/xlum_example.xlum"
        )
        # "/Users/sgrehl/Documents/GIT/xlum/R-package/xlum_v2/inst/extdata/xlum_example.xlum"
        # "/Users/sgrehl/Downloads/BDX16646_OSL_SAR.xlum"
        # "/Users/sgrehl/Downloads/BDX16646_RF70.xlum"
    )
    logging.debug(obj)

    df_xlum: pd.DataFrame = obj.df
    print(obj.__class__.__name__, "DataFrame:\n", df_xlum, "\n-----------")
    for sample in obj.lstSamples:
        sample:Sample
        df_sequences:pd.DataFrame = sample.df
        print(sample.__class__.__name__, "DataFrame:\n", df_sequences, "\n-----------")
        for sequence in sample.lstSequences:
            sequence:Sequence
            df_records:pd.DataFrame = sequence.df
            print(sequence.__class__.__name__, "DataFrame:\n", df_records, "\n-----------")
            for record in sequence.lstRecords:
                record:Record
                df_curves:pd.DataFrame = record.df
                print(record.__class__.__name__, "DataFrame:\n", df_curves, "\n-----------")
                for curve in record.lstCurves:
                    curve:Curve
                    df_values:pd.DataFrame = curve.df
                    print(curve.__class__.__name__, "DataFrame:\n", df_values, "\n-----------")


if __name__ == '__main__':
    main()
