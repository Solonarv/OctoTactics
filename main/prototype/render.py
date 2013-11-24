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
        self.focus=(-1,-1,None,False) # x,y,frame,changed
        self.tarlinepool=set()
        self.tarlineschanged=False
    
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
    
    def update_focusframe(self):
        x,y,frame,changed=self.focus
        if not changed: return
        if x!=-1 and y!=-1:
            if frame is None:
                frame=self.canvas.create_oval(x*50+10,y*50+10,x*50+40,y*50+40)
            else:
                self.canvas.coords(frame,x*50+10,y*50+10,x*50+40,y*50+40)
        elif frame is not None:
            self.canvas.coords(frame,-1,-1,-1,-1)
        self.focus=(x,y,frame,False)
    
    def focus_onto(self,x,y):
        _,_,f,_=self.focus
        self.focus=(x,y,f,True)
    
    def update_cellcounters(self):
        for coords,cellcnt in self.cellcounters.items():
            x,y=coords
            cell=self.board.cells[x,y]
            self.canvas.itemconfig(cellcnt,int(cell.energy))
    
    def update_tarlines(self):
        if not self.tarlineschanged: return
        ntarlines_req=3*sum([len(c.targets) for c in self.board.cells.values()])
        ntarlines_act=len(self.tarlinepool)
        if ntarlines_act>ntarlines_req: # remove unneeded lines
            newpool={self.tarlinepool.pop() for i in range(ntarlines_req)}
            for line in self.tarlinepool.difference(newpool):
                self.canvas.delete(line)
            self.tarlinepool=newpool
        elif ntarlines_act!=ntarlines_req: # add more lines if necessary
            self.tarlinepool.update({self.canvas.create_line(-1,-1,-1,-1) for i in range(ntarlines_req-ntarlines_act)})
        # Iterate through cells, assign each 3*n lines if needed