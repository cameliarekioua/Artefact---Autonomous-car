import time
import threading
from .controller import Controller
import math

class CtrlMot():

    ## Constantes ##
    TICK_PER_CM = 120 * 4*8 / (6.75*math.pi)
    TICKS_PER_DEGREE = TICK_PER_CM * (math.pi * 19.5) / 360
    ARRET = 0
    MARCHE = 1
    TOURNE = 2




    ## Initialisation ##
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.etat = self.ARRET
        self.etatFutur = self.ARRET

        self.pos_lock = threading.Lock()      
        self.distance_parcourue = 0
        self.angle_parcouru = 0
        self.last_distance_parcourue = 0
        self.last_angle_parcouru = 0

        self.controller.set_motor_shutdown_timeout(10)


        self.K = 0.005     # Proportionnel
        self.Ki = 0.0005  # Intégral

        self.action_thread = None
        self.action_event = threading.Event()  # Utilisé pour interrompre les actions

    def _move_ticks_turn(self, left_ticks_exp, right_ticks_exp, speed):
            """Fonction pour exécuter les mouvements avec correction PI."""

            print(f"etat : {self.etat} , tick to go : {left_ticks_exp} , {right_ticks_exp}")
            relativeTicks = self.controller.new_relative()
            ticks_left, ticks_right = 0, 0
            integral_error = 0
            base_speed = speed

            self.last_distance_parcourue = 0
            self.last_angle_parcouru = 0

            self.distance_parcourue = 0     
            self.angle_parcouru = 0 


            base_left_speed = base_speed if left_ticks_exp > 0 else -base_speed
            base_right_speed = base_speed if right_ticks_exp > 0 else -base_speed
            self.controller.set_motor_speed(base_left_speed, base_right_speed)

            raw_left_speed = 0
            raw_right_speed = 0


            while not self.action_event.is_set():
                ticks_update = self.controller.get_relative_encoder_ticks(relativeTicks)
                ticks_left += ticks_update[0]
                ticks_right += ticks_update[1]




                #Correction pour avoir des ticks coherents

                if self.etat == self.MARCHE:
                    tick_error = ticks_left - ticks_right
                elif self.etat == self.TOURNE:
                    tick_error = -(ticks_right + ticks_left)

                integral_error += tick_error

                correction = self.K * tick_error + self.Ki * integral_error

                if self.etat == self.MARCHE:
                    base_left_speed = self.arret(left_ticks_exp - ticks_left,base_left_speed)
                    base_right_speed = self.arret(right_ticks_exp - ticks_right,base_right_speed)
                    raw_left_speed = base_left_speed - correction
                    raw_right_speed = base_right_speed + correction
                elif self.etat == self.TOURNE:
                    base_left_speed = self.arret(left_ticks_exp - ticks_left,base_left_speed)


    def _move_ticks(self, left_ticks_exp, right_ticks_exp, speed):
        """Fonction pour exécuter les mouvements avec correction PI."""

        print(f"etat : {self.etat} , tick to go : {left_ticks_exp} , {right_ticks_exp}")
        relativeTicks = self.controller.new_relative()
        ticks_left, ticks_right = 0, 0
        integral_error = 0
        base_speed = 1        

        self.last_distance_parcourue = 0
        self.last_angle_parcouru = 0

        self.distance_parcourue = 0     
        self.angle_parcouru = 0 

        while( base_speed < speed):
            time.sleep(0.05)
            base_speed += 1
            self.controller.set_motor_speed(base_speed, base_speed)

        base_left_speed = base_speed if left_ticks_exp > 0 else -base_speed
        base_right_speed = base_speed if right_ticks_exp > 0 else -base_speed
        self.controller.set_motor_speed(base_right_speed, base_left_speed)

        raw_left_speed = 0
        raw_right_speed = 0


        while not self.action_event.is_set():
            ticks_update = self.controller.get_relative_encoder_ticks(relativeTicks)
            ticks_left += ticks_update[0]
            ticks_right += ticks_update[1]




            #Correction pour avoir des ticks coherents

            if self.etat == self.MARCHE:
                tick_error = ticks_left - ticks_right
            elif self.etat == self.TOURNE:
                tick_error = -(ticks_right + ticks_left)

            integral_error += tick_error

            correction = self.K * tick_error + self.Ki * integral_error

            if self.etat == self.MARCHE:
                base_left_speed = self.arret(left_ticks_exp - ticks_left,base_left_speed)
                base_right_speed = self.arret(right_ticks_exp - ticks_right,base_right_speed)
                raw_left_speed = base_left_speed - correction
                raw_right_speed = base_right_speed + correction
            elif self.etat == self.TOURNE:
                base_left_speed = self.arret(left_ticks_exp - ticks_left,base_left_speed)
                base_right_speed = self.arret(right_ticks_exp - ticks_right,base_right_speed)
                raw_left_speed = base_left_speed + correction
                raw_right_speed = base_right_speed + correction

            #Fin correction




            # print(f"mode : {self.etat}, tick left : {ticks_left} , tick right : {ticks_right} , correction : {correction}")

            left_speed = max(min(int(raw_left_speed), 60), -60)
            right_speed = max(min(int(raw_right_speed), 60), -60)
            self.controller.set_motor_speed(left_speed, right_speed)

            with self.pos_lock:
                self.distance_parcourue = (ticks_left + ticks_right) / 2 / self.TICK_PER_CM
                self.angle_parcouru = (ticks_right - ticks_left) / 2 / self.TICKS_PER_DEGREE

            if abs(ticks_left) >= abs(left_ticks_exp) and abs(ticks_right) >= abs(right_ticks_exp):
                break
            time.sleep(0.01)

        self.controller.set_raw_motor_speed(0, 0)
        self.etat = self.ARRET

        time.sleep(0.1)


    def _start_action(self, target, *args):
        """Lance une action dans un thread séparé."""
        if self.action_thread and self.action_thread.is_alive():
            self.stop()  # Interrompt l'action en cours

        self.etat = self.etatFutur

        self.action_event.clear()
        self.action_thread = threading.Thread(target=target, args=args)
        self.action_thread.start()




    def moveForward(self, distance_m='a', base_speed = 20):
        """Déplace le robot en avant."""
        print("coucour")
        self.etatFutur = self.MARCHE
        self.etat = self.MARCHE
        if isinstance(distance_m, str):
            speed = base_speed if distance_m == 'a' else -base_speed
            self.controller.set_motor_speed(speed, speed)
        else:
 
            print("coucou")
            ticks_to_move = int(distance_m * self.TICK_PER_CM)
            self._start_action(self._move_ticks, ticks_to_move, ticks_to_move, base_speed)





    def turn(self, angle_deg='d',base_speed = 10):
        """Fait tourner le robot."""
        self.etatFutur = self.TOURNE
        self.etat = self.TOURNE
        if isinstance(angle_deg, str):
            speed = base_speed if angle_deg == 'd' else -base_speed
            self.controller.set_motor_speed(speed, -speed)
        else:
            ticks_for_rotation = int(self.TICKS_PER_DEGREE*angle_deg)
            self._start_action(self._move_ticks_turn, -ticks_for_rotation, ticks_for_rotation, base_speed)


    
    def distMoved(self):
        with self.pos_lock:
            movedOf = self.distance_parcourue - self.last_distance_parcourue
            self.last_distance_parcourue = self.distance_parcourue
            return movedOf



    def angleMoved(self):
        with self.pos_lock:
            movedOf = self.angle_parcouru - self.last_angle_parcouru
            self.last_angle_parcouru = self.angle_parcouru
            return movedOf




    def stop(self):
        """Arrête le robot et interrompt toute action."""
        self.action_event.set()
        if self.action_thread:
            self.action_thread.join()
        self.controller.set_raw_motor_speed(0, 0)
        self.etat = self.ARRET



    def arret(self, diff, speed):
        if speed == 0:
            return speed
        signe = int(speed/abs(speed))
        speed = abs(speed)
        speed = min(speed, 5 + 2/self.TICK_PER_CM*abs(diff))
        
        
        return speed*signe
