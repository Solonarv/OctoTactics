'''
Created on 29.09.2013

@author: Solonarv
'''
from struct import Struct

struct_CellBase = Struct('>QHHfc')
# A struct composed of:
#  - unsigned long long (cell's uid)
#  - unsigned short (cell's x position)
#  - unsigned short (cell's y position)
#  - float (cell's energy)
#  - char  (cell's type
# All in big-endian (network byte order)

short = Struct('>H')
# A struct that holds a single unsigned short

ulonglong = Struct('>Q')

def encodechanges(board, recorder):
    data = bytearray()
    
    # Append board dimensions
    data.extend(short.pack(board.w))
    data.extend(short.pack(board.h))
    
    for cell in board.cells.values():
        if cell is not None:
            data.extend(
             struct_CellBase.pack(cell.uid, cell.pos[0], cell.pos[1], cell.energy, cell.tpid))
            data.extend(short.pack(len(cell.targets)))
            for tar in cell.targets:
                data.extend(ulonglong.pack(tar.uid))
            

