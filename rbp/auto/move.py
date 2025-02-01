#on veut aller de x,y à z,w 
#(0,0) en bas a gauche 
c = controller.Controller()
def move (from, to):
    x,y = from
    x1,y1 = to 
    dx  = x1-x
    dy = y1-y
    #on va a gauche
    if dx<0:
    #aller a gacuhe de |dx| cases
        turn_left(c,90)
        dx= -dx
        forward(c,50*dx,speed) 
    elif: 
    #aller a droite de dx cases
        turn_right(c,90)
        forward(c,50*dx,speed) 
    if dy < 0:
    # aller en bas
    elif:
    # aller en haut de dy cases
        forward(c,dy*50)


