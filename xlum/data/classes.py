import base64
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List
import re
from lxml import etree
import pandas as pd
from functools import cached_property

from xlum.data.enumerations import CurveType, RecordType, State, SampleCondition


class Xlum_DataFrame_Support(object):
    def __init__(self) -> None:
        """derault construktor - NOT IMPLEMENTED

        Raises:
            NotImplementedError: not intended to instantiate
        """
        raise NotImplementedError(
            "This class cannot be instantiated, please implement your own class that inherit its functionalities."
        )

    @cached_property
    def df(self) -> pd.DataFrame:
        """dataclass as dataframe, with nested datapoints as rows
        Returns:
            pd.DataFrame: data frame
        """
        # Find class attribute with nested list, eg records within a sequence
        for k in self.__dict__:
            k: str
            if len(k) > 3 and k[:3] == "lst":
                strLabel = k
        # Create data frame with all class-attributes, including and renaming _meta (if available)
        df = pd.DataFrame([self]).drop(columns=[strLabel], axis="columns")
        df.rename(
            columns={k: self.__class__.__name__ + "." + k for k in df.columns},
            inplace=True,
        )
        lstDataFrames = [df]
        if "_meta" in self.__dict__:
            lstDataFrames[0].drop(
                columns=self.__class__.__name__ + "." + "_meta",
                axis="columns",
                inplace=True,
            )
            lstDataFrames.append(
                pd.DataFrame([self._meta]).rename(
                    columns={
                        c: self.__class__.__name__ + "." + c
                        for c in self._meta.__dict__
                    }
                )
            )

        # Add nested list as rows, records in a sequence
        df_lst: pd.DataFrame = pd.json_normalize(
            asdict(entry) for entry in eval(f"self.{strLabel}")
        )
        # Remove deeper nested informations, eg curves since lists in data frames are not best-practice - merge data frames if informations should be combined
        nestedLists: List = []
        metaInformation: List = []
        for c in df_lst:
            c: str
            if len(c) > 3 and c[:3] == "lst":
                nestedLists.append(c)
            if len(c) > 5 and c[:5] == "_meta":
                metaInformation.append(c)
        df_lst.drop(labels=nestedLists, axis="columns", inplace=True)
        # Rename '_meta' information in self.lst...
        lstDataFrames.append(
            df_lst.rename(
                columns={
                    k: strLabel[3:] + "." + k.replace("_meta.", "")
                    for k in df_lst.columns
                }
            )
        )
        # Merge class information and nested list information, sequence and its records
        return pd.concat(lstDataFrames, axis="columns")


@dataclass
class XLum_Meta(object):
    comment: str = "empty"
    state: State = State.UNKNOWN
    parentID: str = "NA"

    @classmethod
    def from_attributes(cls, dct: Dict) -> "XLum_Meta":
        """extract meta informatino from xml attributes

        Args:
            dct (Dict): attributes dictionary

        Returns:
            XLum_Meta: structured data
        """
        attr = dict()
        for k in ["comment", "state", "parentID"]:
            if k in dct:
                attr[k] = dct["comment"]
            else:
                attr[k] = "NA"
        try:
            if attr["state"] == "NA":
                attr["state"] = State.UNKNOWN
            else:
                attr["state"] = State[dct["state"].upper()]
        except Exception as ex:
            print(ex)
            attr["state"] = dct["state"]

        return XLum_Meta(**attr)


@dataclass
class Curve(Xlum_DataFrame_Support):

    lstValues: List = lambda: []  # internal list in the curve node

    component: str = "NA"
    startDate: datetime = datetime(2013, 1, 1, 3, 42, 42, 42)
    curveType: CurveType = CurveType.UNKNOWN
    duration: float = 0.0
    offset: float = 0.0
    xValues: List[
        int
    ] = lambda: []  # see: https://stackoverflow.com/questions/52063759/passing-default-list-argument-to-dataclasses
    yValues: List[int] = lambda: []
    tValues: List[int] = lambda: []
    xLabel: str = "NA"
    yLabel: str = "NA"
    tLabel: str = "NA"
    vLabel: str = "NA"
    xUnit: str = "NA"
    yUnit: str = "NA"
    tUnit: str = "NA"
    vUnit: str = "NA"
    detectionWindow: str = "NA"
    filter: str = "NA"
    _meta: XLum_Meta = XLum_Meta(comment="empty curve")

    @classmethod
    def from_element(cls, element: etree.Element) -> "Curve":
        """extract Curve information from tree element

        Args:
            element (etree.Element): xml tree element with 'curve' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "curve", f"{element.tag=} expected 'curve'"

        attr = dict()
        # strings
        for k in [
            "component",
            "xLabel",
            "yLabel",
            "tLabel",
            "vLabel",
            "xUnit",
            "yUnit",
            "tUnit",
            "vUnit",
            "filter",
            "detectionWindow",
        ]:
            if k in element.attrib:
                attr[k] = element.attrib[k]
                if k == "component":
                    print(element.attrib[k])
            else:
                attr[k] = "NA"
        # floats
        for k in [
            "duration",
            "offset",
        ]:
            if k in attr:
                attr[k] = float(element.attrib[k])
            else:
                attr[k] = 0.0
        # list[int]
        for k in ["xValues", "yValues", "tValues"]:
            if k in attr:
                attr[k] = list(map(int, element.attrib[k].split()))
            else:
                attr[k] = []
        # check if values are base64 encoded
        strValues = element.text
        b64_pattern = re.compile('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
        if re.fullmatch(b64_pattern, strValues):
            strValues = base64.b64decode(strValues)
        lstStrValues = re.findall(r"[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+", strValues)
        attr["lstValues"] = list(map(float, lstStrValues))

        if "startDate" not in element.attrib:
            date = datetime(2013, 1, 1, 3, 42, 42, 42)
        else:
            # Milliseconds are optional
            datetime_format = "%Y-%m-%dT%H:%M:%SZ"
            if "." in element.attrib["startDate"]:
                datetime_format = datetime_format.replace("Z", ".%fZ")
            if "Z" not in element.attrib["startDate"]:
                datetime_format = datetime_format.replace("Z", "")
            date = datetime.strptime(element.attrib["startDate"], datetime_format)

        return Curve(
            startDate=date,
            curveType=CurveType[element.attrib["curveType"].upper().replace("-", "_")]
            if "curveType" in element.attrib
            else CurveType.UNKNOWN,
            _meta=XLum_Meta.from_attributes(element.attrib),
            **attr,
        )

    @cached_property
    def df(self) -> pd.DataFrame:
        """overloaded data frame generation

        Returns:
            pd.DataFrame: data frame
        """
        df: pd.DataFrame = pd.DataFrame([self]).drop(columns="_meta", axis="columns")
        df_meta: pd.DataFrame = pd.DataFrame([self._meta]).rename(
            columns={c: self.__class__.__name__ + "." + c for c in self._meta.__dict__}
        )
        metaInformation: List = []
        lstSeriesColumns = []
        for c in df:
            c: str
            if len(c) > 5 and c[:5] == "_meta":
                metaInformation.append(c)
            if "Values" in c:
                lstSeriesColumns.append(c)
        df = df.rename(columns={"lstValues": "curve"})
        return pd.concat([df, df_meta], axis="columns")


@dataclass
class Record(Xlum_DataFrame_Support):

    lstCurves: List[Curve] = lambda: []

    recordType: RecordType = RecordType.UNKNOWN
    sequenceStepNumber: int = 0
    sampleCondition: SampleCondition = SampleCondition.UNKNOWN

    _meta: XLum_Meta = XLum_Meta(comment="empty record")

    @classmethod
    def from_element(cls, element: etree.Element) -> "Record":
        """extract Record information from tree element

        Args:
            element (etree.Element): xml tree element with 'record' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "record", f"{element.tag=} expected 'record'"

        meta = XLum_Meta.from_attributes(element.attrib)
        return Record(
            lstCurves=[
                Curve.from_element(e)
                for e in element.getchildren()
                if e.tag.lower() == "curve"
            ],
            _meta=meta,
            recordType=RecordType[
                element.attrib["recordType"].upper().replace("-", "_")
            ]
            if "recordType" in element.attrib
            else RecordType.UNKNOWN,
            sequenceStepNumber=int(element.attrib["sequenceStepNumber"])
            if "sequenceStepNumber" in element.attrib
            else 0,
            sampleCondition=SampleCondition[
                element.attrib["sampleCondition"]
                .upper()
                .replace("+", "_")
                .translate({ord(c): None for c in "()."})
            ]
            if "sampleCondition" in element.attrib
            else SampleCondition.UNKNOWN,
        )


@dataclass
class Sequence(Xlum_DataFrame_Support):

    lstRecords: List[Record] = lambda: []

    fileName: str = "NA"
    software: str = "NA"
    readerName: str = "NA"
    readerSN: str = "NA"
    readerFW: str = "NA"

    _meta: XLum_Meta = XLum_Meta(comment="empty sequence")

    @classmethod
    def from_element(cls, element: etree.Element) -> "Sequence":
        """extract Sequence information from tree element

        Args:
            element (etree.Element): xml tree element with 'sequence' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "sequence", f"{element.tag=} expected 'sequence'"

        meta = XLum_Meta.from_attributes(element.attrib)

        attr = {}
        # strings
        for k in ["fileName", "software", "readerName", "readerSN", "readerFW"]:
            if k in element.attrib:
                attr[k] = element.attrib[k]

        return Sequence(
            lstRecords=[
                Record.from_element(e)
                for e in element.getchildren()
                if e.tag.lower() == "record"
            ],
            _meta=meta,
            **attr,
        )


@dataclass
class Sample(Xlum_DataFrame_Support):

    lstSequences: List[Sequence] = lambda: []

    name: str = "NA"
    mineral: str = "NA"
    latitude: float = -1000.0
    longitude: float = -1000.0
    altitude: float = -1000.0
    doi: str = "NA"

    _meta: XLum_Meta = XLum_Meta(comment="empty sample")

    @classmethod
    def from_element(cls, element: etree.Element) -> "Sample":
        """extract Sample informatin from tree element

        Args:
            element (etree.Element): xml tree element with 'sample' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "sample", f"{element.tag=} expected 'sample'"

        meta = XLum_Meta.from_attributes(element.attrib)

        attr = {}
        # strings
        for k in ["name", "mineral", "doi"]:
            if k in element.attrib:
                attr[k] = element.attrib[k]

        # float
        for k in ["latitude", "longitude", "altitude"]:
            if k in element.attrib:
                attr[k] = float(element.attrib[k])

        return Sample(
            lstSequences=[
                Sequence.from_element(e)
                for e in element.getchildren()
                if e.tag.lower() == "sequence"
            ],
            _meta=meta,
            **attr,
        )


@dataclass
class XlumMeta(Xlum_DataFrame_Support):

    lstSamples: List[Sample] = lambda: []

    formatVersion: str = "NA"
    author: str = "NA"
    lang: str = "NA"
    license: str = "NA"

    @classmethod
    def from_element_tree(cls, tree: etree.ElementTree) -> "XlumMeta":
        """extract XLum meta data from an imported element tree

        Args:
            tree (etree.ElementTree): xlum file as element tree

        Returns:
            XlumMeta: parsed data
        """
        root: etree.Element = tree.getroot()
        assert root.tag.lower() == "xlum", f"{root.tag=} expected 'xlum'"
        for e in root.getchildren():
            print(e.tag)

        attr = {}
        # strings
        for k in ["formatVersion", "author", "lang", "license"]:
            if k in root.attrib:
                attr[k] = root.attrib[k]
        return cls(
            lstSamples=[
                Sample.from_element(e)
                for e in root.getchildren()
                if e.tag.lower() == "sample"
            ],
            **attr,
        )
