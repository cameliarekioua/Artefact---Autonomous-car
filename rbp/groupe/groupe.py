x = 0
y = 0
curr_x, curr_y = 0, 0

COLS = 6
ROWS = 6

balises = set()

def do_cycle():
    global x, y, balises
    while (y < ROWS):
        y = y+1
        curr_x, curr_y, found_balises = chercher_balise()   # en cherchant les balises, il tourne, donc il triangulise en même temps 
        avancer([curr_x, curr_y], 50*[x, y])
        balises = balises | found_balises
    tourner_droite(90)
    avancer(50*[x, y], 50*[x+1, y])
    x += 1
    tourner_droite(90)
    while y >= -1:
        y = y-1
        curr_x, curr_y, found_balises = chercher_balise()
        avancer([curr_x, curr_y], 50*[x, y])
        balises = balises 
    
def 
