from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import re
from lxml import etree

from data.enumerations import CurveType, RecordType, State, SampleCondition


@dataclass
class XLum_Meta(object):
    comment:str="empty"
    state:State=State.UNKNOWN
    parentID:str="NA"

    @classmethod
    def from_attributes(cls, dct:Dict) -> 'XLum_Meta':
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

        return XLum_Meta(
            **attr
        )


@dataclass
class Curve(object):
    
    lstValues:List=lambda: []  # internal list in the curve node

    component:str="NA"
    startDate:datetime=datetime(2013, 1, 1, 3, 42, 42, 42)
    curveType:CurveType=CurveType.UNKNOWN
    duration:float=0.0
    offset:float=0.0
    xValues:List[int]=lambda: []  # see: https://stackoverflow.com/questions/52063759/passing-default-list-argument-to-dataclasses
    yValues:List[int]=lambda: []
    tValues:List[int]=lambda: []
    xLabel:str="NA"
    yLabel:str="NA"
    tLabel:str="NA"
    vLabel:str="NA"
    xUnit:str="NA"
    yUnit:str="NA"
    tUnit:str="NA"
    vUnit:str="NA"
    detectionWindow:str="NA"
    filter:str="NA"
    _meta:XLum_Meta=XLum_Meta(
        comment="empty curve"
    )

    @classmethod
    def from_element(cls, element:etree.Element) -> 'Curve':
        """extract Curve information from tree element

        Args:
            element (etree.Element): xml tree element with 'curve' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "curve", f"{element.tag=} expected 'curve'"

        attr = dict()
        # strings
        for k in ["component", "xLabel", "yLabel", "tLabel", "vLabel", "xUnit", "yUnit", "tUnit", "vUnit", "filter", "detectionWindow"]:
            if k in attr:
                attr[k] = element.attrib[k]
            else:
                attr[k] = "NA"
        # floats
        for k in ["duration", "offset",]:
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
            lstValues=re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', element.text),
            startDate=date,
            curveType=CurveType[element.attrib["curveType"].upper().replace("-", "_")] if "curveType" in element.attrib else CurveType.UNKNOWN,
            _meta = XLum_Meta.from_attributes(element.attrib),
            **attr
            )

@dataclass
class Record(object):

    lstCurves:List[Curve]=lambda: []

    recordType:RecordType=RecordType.UNKNOWN
    sequenceStepNumber:int=0
    sampleCondition:SampleCondition=SampleCondition.UNKNOWN

    _meta:XLum_Meta=XLum_Meta(
        comment="empty record"
    )
    
    @classmethod
    def from_element(cls, element:etree.Element) -> 'Record':
        """extract Record information from tree element

        Args:
            element (etree.Element): xml tree element with 'record' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "record", f"{element.tag=} expected 'record'"

        meta = XLum_Meta.from_attributes(element.attrib)
        return Record(
            lstCurves = [Curve.from_element(e) for e in element.getchildren() if e.tag.lower() == 'curve'],
            _meta = meta,
            recordType=RecordType[element.attrib["recordType"].upper().replace("-", "_")] if "recordType" in element.attrib else RecordType.UNKNOWN,
            sequenceStepNumber=int(element.attrib["sequenceStepNumber"]) if "sequenceStepNumber" in element.attrib else 0,
            sampleCondition=SampleCondition[element.attrib["sampleCondition"].upper().replace("+", "_").translate({ord(c):None for c in "()."})] if "sampleCondition" in element.attrib else SampleCondition.UNKNOWN,
        )


@dataclass
class Sequence(object):

    lstRecords:List[Record]=lambda: []

    fileName:str="NA"
    software:str="NA"
    readerName:str="NA"
    readerSN:str="NA"
    readerFW:str="NA"

    _meta:XLum_Meta=XLum_Meta(
        comment="empty sequence"
    )

    @classmethod
    def from_element(cls, element:etree.Element) -> 'Sequence':
        """extract Sequence information from tree element

        Args:
            element (etree.Element): xml tree element with 'sequence' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "sequence", f"{element.tag=} expected 'sequence'"

        meta = XLum_Meta.from_attributes(element.attrib)

        attr = {}
        #strings
        for k in ["fileName", "software", "readerName", "readerSN", "readerFW"]:
            if k in element.attrib:
                attr[k] = element.attrib[k]

        return Sequence(
            lstRecords = [Record.from_element(e) for e in element.getchildren() if e.tag.lower() == 'record'],
            _meta = meta,
            **attr,
        )



@dataclass
class Sample(object):

    lstSequences:List[Sequence]=lambda: []

    name:str="NA"
    mineral:str="NA"
    latitude:float=-1000.0
    longitude:float=-1000.0
    altitude:float=-1000.0
    doi:str="NA"
    
    _meta:XLum_Meta=XLum_Meta(
        comment="empty sample"
    )

    @classmethod
    def from_element(cls, element:etree.Element) -> 'Sample':
        """extract Sample informatin from tree element

        Args:
            element (etree.Element): xml tree element with 'sample' tag

        Returns:
            Sample: structured data
        """
        assert element.tag.lower() == "sample", f"{element.tag=} expected 'sample'"

        meta = XLum_Meta.from_attributes(element.attrib)

        attr = {}
        #strings
        for k in ["name", "mineral", "doi"]:
            if k in element.attrib:
                attr[k] = element.attrib[k]
        
        #float
        for k in ["latitude", "longitude", "altitude"]:
            if k in element.attrib:
                attr[k] = float(element.attrib[k])

        return Sample(
            lstSequences = [Sequence.from_element(e) for e in element.getchildren() if e.tag.lower() == 'sequence'],
            _meta = meta,
            **attr,
        )


@dataclass
class XlumMeta(object):

    lstSamples:List[Sample]=lambda: []

    formatVersion:str="NA"

    @classmethod
    def from_element_tree(cls, tree:etree.ElementTree) -> 'XlumMeta':
        """extract XLum meta data from an imported element tree

        Args:
            tree (etree.ElementTree): xlum file as element tree

        Returns:
            XlumMeta: parsed data
        """
        root:etree.Element = tree.getroot()
        assert root.tag.lower() == "xlum", f"{root.tag=} expected 'xlum'"
        for e in root.getchildren():
            print(e.tag)

        return cls(
            lstSamples = [Sample.from_element(e) for e in root.getchildren() if e.tag.lower() == 'sample'],
            formatVersion=root.attrib['formatVersion']
        )