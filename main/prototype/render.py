'''
Created on 22.11.2013

@author: Solonarv
'''

class RenderBoard(object):
    def __init__(self, board, canv):
        self.board=board
        self.canvas=canv
        self.cellpolys={(x,y): self.cellpoly(x,y) for x,y in board.cells}
        self.cellcounters={(x,y): self.cellcounter(x,y) for x,y in board.cells}
    
    def cellpoly(self,cx,cy):
        cell=self.board.cells[cx,cy]
        if cell.celltype=="octogon":
            return self.canvas.create_polygon(cx*50+10,cy*50-10, # Almost a perfect regular octogon
                                              cx*50+40,cy*50-10, # Side ratio is off by ~6% only
                                              cx*50+60,cy*50+10, # That's less that 2px
                                              cx*50+60,cy*50+40, # And the fractions are really simple
                                              cx*50+40,cy*50+60, # Each axis-aligned side is 3/7 the
                                              cx*50+10,cy*50+60, # distance between opposing sides
                                              cx*50-10,cy*50+40, # which is 3/5 of the grid spacing(50px)
                                              cx*50-10,cy*50+10) # Pretty cool, huh? Math!
        else:
            return self.canvas.create_rectangle(cx*50+10,cy*50+10,
                                                cx*50+40,cy*50+40)
    
    def cellcounter(self,cx,cy):
        return self.canvas.create_text(cx*50+25,cy*50+25,text=int(self.board.cells[cx,cy].energy),anchor="center")