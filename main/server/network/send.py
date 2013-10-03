'''
Created on 29.09.2013

@author: Solonarv
'''
from struct import Struct
from util.structhelper import ushort, ulonglong

struct_CellBase = Struct('>QHHfc')
# A struct composed of:
#  - unsigned long long (cell's uid)
#  - unsigned short (cell's x position)
#  - unsigned short (cell's y position)
#  - float (cell's energy)
#  - char  (cell's type
# All in big-endian (network byte order)

struct_BoardDims = Struct('>HH')

def encodechanges(board, recorder):
    
    # Append board dimensions
    data = bytearray(struct_BoardDims.pack(board.w, board.h))
    
    for cell in board.cells.values():
        data.extend(struct_CellBase.pack(cell.uid, cell.pos[0], cell.pos[1], cell.energy, cell.tpid))
    
    data.extend(len(recorder.changelog))
    for change in recorder.changelog:
        data.extend(change.pack())