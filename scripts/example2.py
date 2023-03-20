import xlum

try:
    import matplotlib
    from matplotlib import pyplot as plt
except ModuleNotFoundError:
    import pip
    pip.main(["install", "--user", "matplotlib"])
finally:
    import matplotlib
    from matplotlib import pyplot as plt
try:
    import tkinter
except ModuleNotFoundError:
    import pip
    pip.main(["install", "--user", "tkinter"])
finally:
    from tkinter.filedialog import askopenfilename


def main ():
    filename = askopenfilename()
    obj = xlum.from_xlum(filename)

    for sample in obj.lstSamples:
        for idx_s, sequence in enumerate(sample.lstSequences):
            for idx_r, record in enumerate(sequence.lstRecords):
                plt.figure(idx_s*100+idx_r)
                for curve in record.lstCurves:
                    plt.plot(curve.lstValues, "o-", label=f"{curve.component} - {curve.vLabel} in [{curve.vUnit}] '{curve.curveType.name.lower()}'")
                    plt.xlabel(f"{curve.tLabel} in [{curve.tUnit}]")
                    if curve.yLabel != "NA":
                        plt.ylabel(f"{curve.yLabel} in [{curve.yUnit}]")
                plt.title(
                    f"""
                    {obj.author}
                    {sample.name}: {sample.mineral} from ({sample.longitude:.2f}, {sample.latitude:.2f}, {sample.altitude:.2f})
                    {sequence.fileName} by {sequence.software}
                    {record.recordType.name}{' - '+ record._meta.comment if record._meta.comment != "NA" else ""}
                    """
                    )
                plt.legend()
    plt.show()

if __name__ == "__main__":
    main()