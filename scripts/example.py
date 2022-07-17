import os
import pandas as pd
import urllib

from xlum.data.classes import XlumMeta, Sample, Record, Sequence, Curve
import xlum.importer


def main():

    # Download example file
    url = 'https://raw.githubusercontent.com/R-Lum/xlum_specification/master/examples/xlum_example.xlum'
    local_dir = os.path.join(os.getcwd(), "tmp")
    local_path = os.path.join(local_dir, "example.xlum")
    os.mkdir(local_dir)
    urllib.request.urlretrieve(url, local_path)

    obj: XlumMeta = xlum.importer.from_xlum(local_path)

    os.remove(local_path)
    os.rmdir(local_dir)

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
