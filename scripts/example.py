import logging
import os
import pandas as pd
from dataclasses import asdict

DIRNAME = os.path.dirname(__file__)
import sys
sys.path.append(
    os.path.join(
        DIRNAME,
        '../xlum')
)
import importer
from data.classes import XlumMeta, Sample, Record, Sequence, Curve

def main():
    logging.basicConfig(level=logging.DEBUG)

    obj:XlumMeta = importer.from_xlum(
        # os.path.join(
        #     DIRNAME, 
        #     "../assets/xlum_example.xlum"
        # )
        # "/Users/sgrehl/Documents/GIT/xlum/R-package/xlum_v2/inst/extdata/xlum_example.xlum"
        "/Users/sgrehl/Downloads/BDX16646_OSL_SAR.xlum"
        # "/Users/sgrehl/Downloads/BDX16646_RF70.xlum"
    )
    logging.debug(obj)

    df_xlum:pd.DataFrame = obj.df
    # df_samples:pd.DataFrame = obj.df
    # for sample in obj.lstSamples:
    #     sample:Sample
    #     df_sequences:pd.DataFrame = pd.json_normalize(asdict(sequence) for sequence in sample.lstSequences).drop(labels="lstRecords", axis="columns")
    #     for sequence in sample.lstSequences:
    #         sequence:Sequence
    #         df_records:pd.DataFrame = pd.json_normalize(asdict(record) for record in sequence.lstRecords).drop(labels="lstCurves", axis="columns")
    #         for record in sequence.lstRecords:
    #             record:Record
    #             df_curves:pd.DataFrame = pd.json_normalize(asdict(curve) for curve in record.lstCurves).drop(labels="lstValues", axis="columns")
    #             for curve in record.lstCurves:
    #                 curve:Curve
    #                 df_values:pd.DataFrame = pd.json_normalize(asdict(value) for value in curve.lstValues)


if __name__ == '__main__':
    main()