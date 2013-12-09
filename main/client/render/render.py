'''
Created on 22.11.2013

@author: Solonarv
'''

import tkinter

class RenderBoard(object):
    def __init__(self, board, canv):
        self.board=board
        self.canvas=canv
        self.cellpolys={(x,y): self.cellpoly(x,y) for x,y in board.cells}
        self.cellcounters={(x,y): self.cellcounter(x,y) for x,y in board.cells}
        self.focus=(-1,-1,None,False) # x,y,frame,changed
        self.tarlineschanged=False
        canv.bind('<Button-1>',self.onCanvasClicked)
        canv.bind('<Button-3>',self.onCanvasRClicked)
    
    def update(self):
        self.update_cellcounters()
        self.update_focusframe()
        self.update_tarlines()
    
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
                                              cx*50-10,cy*50+10, # Pretty cool, huh? Math!
                                              fill="white",
                                              outline="black",
                                              tag="cell")
        else:
            return self.canvas.create_rectangle(cx*50+10,cy*50+10,
                                                cx*50+40,cy*50+40,
                                                fill="white",
                                                outline="black",
                                                tag="cell")
    
    def cellcounter(self,cx,cy):
        return self.canvas.create_text(cx*50+25,cy*50+25,text=int(self.board.cells[cx,cy].energy),anchor="center")
    
    def update_focusframe(self): # redraw / create focus frame if necessary
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
    
    def update_cellcounters(self): # update each cell's energy counter
        for coords,cellcnt in self.cellcounters.items():
            cell=self.board.cells[coords]
            self.canvas.itemconfig(cellcnt,text=int(cell.energy))
    
    def update_tarlines(self):
        if not self.tarlineschanged: return
        self.canvas.delete("tarline")
        for coords,cell in self.board.cells.items():
            x,y=coords
            for tar in cell.targets:
                self.canvas.create_line(x*50+25,y*50+25,tar.x*50+25,tar.y*50+25, arrow=tkinter.LAST, tag="tarline")
    
    def onCanvasClicked(self, event):
        #TODO clicking near the border of an oct cell registers the click at a nearby square cell
        cx=self.canvas.canvasx(event.x, 1)//50
        cy=self.canvas.canvasy(event.y, 1)//50
        
        cell=self.board.cells[cx,cy]
        fx,fy,_,_=self.focus
        if (fx==-1 and fy==-1) or (cx-fx)**2+(cy-fy)**2>self.board.cells[fx,fy].rangeSq:
            self.focus_onto(cx, cy)
            print("Set focus to %i,%i" % (cx,cy))
            return
        fcell=self.board.cells[fx,fy]
        if cx==fx and cy==fy:
            cell.targets=[]
            print("Cell at %i,%i no longer targeting anything" % (cx,cy))
        elif cell in fcell.targets:
            fcell.targets.remove(cell)
            print("Cell at %i,%i no longer targeting cell at %i,%i" % (fx,fy,cx,cy))
        elif len(fcell.targets)<fcell.maxTargets:
            fcell.targets.append(cell)
            print("Cell at %i,%i now targeting cell at %i,%i" % (fx,fy,cx,cy))
        else: return
        self.tarlineschanged=True
        self.focus_onto(-1, -1)
    
    def onCanvasRClicked(self,event):
        #TODO clicking near the border of an oct cell registers the click at a nearby square cell
        cx=self.canvas.canvasx(event.x, 1)//50
        cy=self.canvas.canvasy(event.y, 1)//50
        
        cell=self.board.cells[cx,cy]
        
        cell.owner=1-cell.owner
        print("Cell at %i,%i switched owner" % (cx,cy))