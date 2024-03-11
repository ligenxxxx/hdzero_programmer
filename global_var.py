brightness = 0
contrast = 0
saturation = 0
backlight = 100
cell_count = 1
warning_cell_voltage = 28

from enum import Enum, unique
from enum import IntEnum

class ch341_status(Enum):
    IDLE = 0
    VTX_NOTCONNECTED = 1
    VTX_CONNECTED = 2
    VTX_UPDATE = 3
    VTX_UPDATEDONE = 4
    
    HYBRIDVIEW_NOTCONNECTED = 21
    HYBRIDVIEW_CONNECTED = 22
    HYBRIDVIEW_GET_FW = 23
    HYBRIDVIEW_UPDATE = 24
    HYBRIDVIEW_UPDATEDONE = 25
    
    STATUS_EXIT = 255
    
class download_status(Enum):
    IDLE = -2
    FILE_PARSE = -1
    DOWNLOAD_VTX_FW = 1
    DOWNLOAD_VTX_FW_DONE = 2
    DOWNLOAD_EXIT = 255


