import enum


class CurveType(enum.Enum):
    NA=-2
    UNKNOWN=-1
    MEASURED=0
    PREDEFINED=1


class RecordType(enum.Enum):
    NA=-2
    UNKNOWN=-1

    PAUSE = 0
    BLEACHING=1
    IRRADIATION=2
    ATMOSPHEREEXCHANGE=3
    HEATING=4

    SPECTROMETER=50
    CAMERA=60
    PREHEAT_TL=90
    TL=100
    ITL=120
    TM_OSL=140
    RF=200
    UV_RF=220
    IR_RF=240
    IR_PL=300
    OSL=500
    GSL=510
    VSL=520
    YSL=530
    IRSL=540
    POSL=550
    NORM_IRRAD=600
    USER =1000
    CUSTOM=1100


class State(enum.Enum):
    NA=-2
    UNKNOWN=-1
    PLANNED=0
    STARTED=1
    FINISHED=2


class SampleCondition(enum.Enum):
    NA=-2
    UNKNOWN=-1
    NATURAL=0
    NATURAL_DOSE=1
    BLEACH=10
    BLEACH_DOSE=11
    NATBLEACH=12
    NAT_DOSEBLEACH=13
    DOSE=20
    BACKGROUND=30
