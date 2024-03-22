from enum import IntEnum
from enum import Enum, unique
brightness = 0
contrast = 0
saturation = 0
backlight = 100
cell_count = 1
warning_cell_voltage = 28

nIndex = 0
PAGE_SIZE = 256
HEAD_SIZE = 4


class ch341_status(Enum):
    IDLE = 0
    VTX_NOTCONNECTED = 1
    VTX_CONNECTED = 2
    VTX_UPDATE = 3
    VTX_UPDATEDONE = 4

    HYBRIDVIEW_CHECK_ALIVE = 11
    HYBRIDVIEW_CONNECTED = 12
    HYBRIDVIEW_GET_FW = 13
    HYBRIDVIEW_UPDATE = 14
    HYBRIDVIEW_UPDATEDONE = 15

    EVENTVRX_NOTCONNECTED = 21
    EVENTVRX_CONNECTED = 22
    EVENTVRX_GET_FW = 23
    EVENTVRX_UPDATE = 24
    EVENTVRX_UPDATEDONE = 25

    STATUS_EXIT = 255


class download_status(Enum):
    IDLE = -2
    FILE_PARSE = -1
    DOWNLOAD_VTX_FW = 1
    DOWNLOAD_VTX_FW_DONE = 2
    DOWNLOAD_HYBRID_VIEW_FW = 3
    DOWNLOAD_HYBRID_VIEW_FW_DONE = 4
    DOWNLOAD_EVENT_VRX_FW = 5
    DOWNLOAD_EVENT_VRX_FW_DONE = 6
    DOWNLOAD_EXIT = 255
