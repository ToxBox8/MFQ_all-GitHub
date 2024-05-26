from math import sqrt
import cmath
import math
from colorama import Fore, Back, Style
import keyboard
import random
import sys
import turtle
from turtle import *
import os
import subprocess
import shutil
import matplotlib.pyplot as plt

def fyq():


    def mrumrua():     
        
            
    
        #----funcion de mrua de velocidad------#       
        def mrua_VV():
                                        

            print("\nHas elejido MRUA de velocidad!")
            print("      vº = v - a * t\n")
            mrua = input("Que dato quires hallar: ").lower()

            if mrua == "v":
                # Solicita al usuario que introduzca los valores
                mrua_vo = float(input("Dame el valor de vº: "))
                mrua_t = float(input("Dame el valor de t: "))
                mrua_a = float(input("Dame el valor de a: "))
                                                                                                                                                                                                                    
                # Calcula la velocidad final
                v = mrua_vo + mrua_a * mrua_t

                # Imprime la solución
                print("La velocidad final es: ", v)
                mfmain()
            elif mrua =="vº":
                                            
                mrua_v = float(input("Dame el valor de v: "))
                mrua_t = float(input("Dame el valor de t: "))
                mrua_a = float(input("Dame el valor de a: "))

                vº = mrua_v - mrua_a * mrua_t
                                            
                print ("La velocidad inicial es:", vº)
                mfmain()
                                        
            elif mrua =="t":
                                            
                mrua_vº = float(input("Dame el valor de vº: "))
                mrua_v = float(input("Dame el valor de v: "))
                mrua_a = float(input("Dame el valor de a: "))

                t = (mrua_v - mrua_vº) / mrua_a

                print ("El tiempo  es:", t)
                mfmain()
                                        
            elif mrua =="a":
                                            
                mrua_v = float(input("Dame el valor de v: "))
                mrua_vº = float(input("Dame el valor de vº: "))
                mrua_t = float(input("Dame el valor de t: "))

                a = (mrua_v - mrua_vº) / mrua_t

                print ("La velocidad inicial es:", a)
                mfmain()

            #-----mrua de posion----#
        def mrua_PP ():
            print("\nHas elejido MRUA de posicion!")
            print("    x = xº + vº * t + 0.5 * a * t ** 2\n")


            mruap = input("Que dato quires hallar: ").lower()

            if mruap == "x":#TERMINAR DE HACER MRUA_PP

                mruap_xº = float(input("Dame el valor de xº: "))
                mruap_vº = float(input("Dame el valor de vº: "))
                mruap_t = float(input("Dame el valor de t: "))
                mruap_a =  float(input("Dame el valor de a: "))

                x = mruap_xº + mruap_vº * mruap_t + 0.5 * mruap_a * mruap_t ** 2 

                print ("La posicion final es x:", x)
                mfmain()
            #-----MRU-------------------------------------------------------------#
        def mru():
            
                print("Has elejido MRU!")
                print("    La formula es: x = xº + vº * t\n")
                mru = input("Que dato quires hallar: ").lower()

                if mru == "x":
                            
                    mru_xº = float(input("Dame el valor de xº: "))
                    mru_v = float(input("Dame el valor de vº: "))
                    mru_t = float(input("Dame el valor de t: "))
                    
                    x =  mru_xº+mru_v*mru_t 
                        

                    print ("La posicion final es x:", x)
                    mfmain()

                    
                elif mru == "xº":
                            
                    mru_x = float(input("Dame el valor de x: "))
                    mru_v = float(input("Dame el valor de vº: "))
                    mru_t = float(input("Dame el valor de t: "))
                        
                    xº = (mru_v*mru_t)/ mru_x

                    print ("La posicion final es xº:", xº )   
                    mfmain()
                elif mru == "t":
                            
                    mru_d = float(input("Dame la distancia: "))
                    mru_v = float(input("Dame el valor de v: "))
                    
                        
                    t = mru_d / mru_v

                    print ("El tiempo es :", t ) 
                    mfmain()   


        #------- elejir entre mru o mrua-----------------#
        mru_o_mrua = input("Que movimiento rectilineo uniforme quieres hacer MRU o MRUA: ").lower()
        if mru_o_mrua == "mrua":#######----resultado MRUA----####################################
                
            #------mrua_v_p--------#                                                            #
            def mrua_v_p():                                                                     #
                while 1<9:                                                                                   #
                    mruavp = input("que quieres hallar velocidad(V) o posicion(P): ")               #
                                                                                                        # 
                    if mruavp == "posicion" or mruavp == "p":  
                                                                    #
                        mrua_PP()                                                           #
                    elif mruavp == "velocidad" or mruavp == "v":                                    #
                        mrua_VV()                                                                   #
                                                                                                    #                                                                                    #
            mrua_v_p()    
        #---------------mru--------------                                                          #
        elif mru_o_mrua == "mru":#----------reseultado MRU---------#
            mru()

    def sustentacion():
        print("\nHas elegido sustentación!\n")

        def sus_main():
            print("\nElige una opción:\n1. Calcular fuerza de sustentación\n2. Calcular coeficiente de sustentación\n3. Calcular densidad del fluido\n4. Calcular velocidad del fluido\n5. Calcular área de la sección transversal\n6. Calcular presión dinámica\n0. Salir")
            opcion = int(input("Ingrese el número de la opción deseada: "))

            if opcion == 1:
                fuerza_sustentacion()
            elif opcion == 2:
                coeficiente_de_sustentacion()
            elif opcion == 3:
                densidad_del_fluido()
            elif opcion == 4:
                velocidad_del_fluido()
            elif opcion == 5:
                area_de_la_seccion_transversal()
            elif opcion == 6:
                presion_dinamica()
            elif opcion == 0:
                print("Saliendo...\n")
            else:
                print("Opción inválida. Por favor, elige una opción válida.")
                sus_main()

        def fuerza_sustentacion():
            d = float(input("Densidad del fluido en kg/m^3: "))
            v = float(input("Velocidad del fluido en m/s: "))
            Cl = float(input("Coeficiente de sustentación: "))
            A = float(input("Área de sección transversal en m^2: "))
            presion_dinamica = d * v ** 2 / 2
            fuerza_sustentacion = presion_dinamica * Cl * A
            print("La fuerza de sustentación es:", fuerza_sustentacion, "N")
            sus_main()

        def coeficiente_de_sustentacion():
            d = float(input("Densidad del fluido en kg/m^3: "))
            v = float(input("Velocidad del fluido en m/s: "))
            A = float(input("Área de sección transversal en m^2: "))
            L = float(input("Fuerza de sustentación en Newtons: "))
            presion_dinamica = d * v ** 2 / 2
            coeficiente_de_sustentacion = 2 * L / (d * v ** 2 * A)
            print("El coeficiente de sustentación es:", coeficiente_de_sustentacion)
            sus_main()

        def densidad_del_fluido():
            v = float(input("Velocidad del fluido en m/s: "))
            Cl = float(input("Coeficiente de sustentación: "))
            A = float(input("Área de sección transversal en m^2: "))
            L = float(input("Fuerza de sustentación en Newtons: "))
            d = 2 * L / (v ** 2 * A * Cl)
            print("La densidad del fluido es:", d, "kg/m^3")
            mfmain()

        def velocidad_del_fluido():
            Cl = float(input("Coeficiente de sustentación: "))
            A = float(input("Área de sección transversal en m^2: "))
            L = float(input("Fuerza de sustentación en Newtons: "))
            d = float(input("Densidad del fluido en kg/m^3: "))
            v = (2 * L / (d * A * Cl)) ** 0.5
            print("La velocidad del fluido es:", v, "m/s")
            sus_main()

        def area_de_la_seccion_transversal():
            v = float(input("Velocidad del fluido en m/s: "))
            Cl = float(input("Coeficiente de sustentación: "))
            L = float(input("Fuerza de sustentación en Newtons: "))
            d = float(input("Densidad del fluido en kg/m^3: "))
            A = (2 * L / (d * v ** 2 * Cl))
            print("El área de la sección transversal es:", A, "m^2")
            sus_main()

        def presion_dinamica():
            d = float(input("Densidad del fluido en kg/m^3: "))
            v = float(input("Velocidad del fluido en m/s: "))
            presion_dinamica = d * v ** 2 / 2
            print("La presión dinámica es:", presion_dinamica, "Pa")
            sus_main()

        sus_main()

###------codigo de flujo----------########


    def fluidos():
            def flujo_main():
                print("\n Elige una opción\n1. tipo de flujo \n2. Calcular la densidad del fluido \n3. Calcular la velocidad del fluido \n4. Calcular la fuerza viscosa \n5. Calcular la distancia \n0 Salir")
                opcion = int(input("Elige una opción: "))
                if opcion == 1:
                    flujo_laminar()
                elif opcion == 2:
                    densidad()
                elif opcion == 3:
                    velocidad()
                elif opcion == 4:
                    fuerza_viscosa()
                elif opcion == 5:
                    distancia()        

            def flujo_laminar():
                d = float(input("densidad del fluido en kg/m^3 "))
                v = float(input("velocidad del fluido en m/s "))
                L = float(input("distancia en m "))
                fuerza_viscosa = float(input("viscosidad en kg/m*s"))
                reynolds = d * v * L / fuerza_viscosa
                print("El numero de reynolds es: ")
                print("El numero de reynolds es: ", reynolds)
                if reynolds < 2300:
                    print("El flujo es laminar")
                elif reynolds > 4000:
                    print("El flujo es turbulento")
                elif reynolds > 2300 and reynolds < 4000:
                    print("El flujo es transitorio")

            def densidad():
                v = float(input("velocidad del fluiso en m/s "))
                L = float (input("distancia en m "))
                fuerza_viscosa = float(input("viscosidad en kg/m*s "))
                reynolds = float(input("número de reynolds "))
                densidad = reynolds * fuerza_viscosa / (v * L)
                print("La densidad del fluido es: Kg/m^3")
                print("la densidad es: ", densidad)

            def velocidad():
                d = float(input("densidad del fluido en kg/m^3 "))
                L = float(input("distancia en m "))
                fuerza_viscosa = float(input("viscosidad en kg/m*s "))
                reynolds = float(input("número de reynolds "))
                velocidad = reynolds * fuerza_viscosa / (d * L)
                print("La velocidad del fluido es: ")
                print("La velocidad del fluido es: ", velocidad)

            def fuerza_viscosa():
                d = float(input("densidad del fluido en kg/m^3 "))
                v = float(input("velocidad del fluido en m/s "))
                L = float(input("distancia en m "))
                reynolds = float(input("número de reynolds "))
                fuerza_viscosa = reynolds * d * v / L
                print("La fuerza viscosa es: ")
                print("La fuerza viscosa es: ", fuerza_viscosa)
            def distancia():
                d = float(input("densidad en kg/m^3 "))
                v = float(input("velocidad en m/s "))
                fuerza_viscosa = float(input("viscosidad en kg/m*s "))
                reynolds = float(input("número de reynolds "))
                L = reynolds * fuerza_viscosa/(d * v)
                print("La distancia es: ")
                print("La distancia es:",L,"m")

            flujo_main()

        
##################################################################################################### 

    def densidad_de_la_sus():

        print("\nHas elegido la formula de la densidad!")

        def Calcular_la_densidad():

            m_d = float(input("Dame la masa:"))
            v_d = float(input("Dame el volumen:"))
            d_d = m_d/v_d
            print("La densidad es",d_d,"g/cm3")

        def Calcular_la_masa():

            v = float(input("el volumen de la sustancia en cm*3"))
            d = float(input("la densidad de la sustancia g/cm*3"))
            m = d*v
            print("la masa de la sustancia", m,"g")

        def Calcular_el_volumen():
            m = float(input("la masa d la sustancia en g"))
            d = float(input("la densidad de la sustancia g/cm3"))
            v = m/d
            print ("el volumen de la sustancia es:", v,"cm3")

        elegir_d = input("1 densidad\n2 masa\n3 volumen\n0 salir\n")

        if elegir_d == "1" or elegir_d =="densidad":
            Calcular_la_densidad()

        elif elegir_d == "2" or elegir_d =="masa":
            Calcular_la_masa()

        elif elegir_d == "3" or elegir_d =="volumen":
            Calcular_el_volumen()

        elif elegir_d == "0" or elegir_d =="salir":
            print("Saliendo...\n")

        else:
            print("opcion invalida")
            densidad_de_la_sus()

    def Formula_de_Mach():
        print ("\nBienvenido a la calculadora de numero de Mach!\n")

        def susm_main():
            print("\nElige una opción:\n\t1. Calcular número de Mach\n\t2. Calcular la velocidad real\n\t3. Calcular velocidad local del sonido\n\t0. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                numero_de_Mach()
            elif opcion == 2:
                velocidad_real()
            elif opcion == 3:
                Velocidad_local_del_sonido()
            elif opcion == 0:
                print("Saliendo...\n")
            else :
                print("Opción no válida")
                susm_main()

        def numero_de_Mach():

            v = float(input("velocidad real en m/s "))
            a = float(input("velocidad local del sonido en m/s "))
            Mach = v/a

            print ("el numero de mach es",Mach)
            susm_main()

        def velocidad_real():
            a = float(input("velocidad local del sonido en m/s "))
            Mach = float(input("numero de mach "))
            v = a*Mach

            print ("la velocidad real es",v,"m/s")
            susm_main()

        def Velocidad_local_del_sonido():
            v = float(input("velocidad real en m/s "))
            Mach = float(input("numero de mach "))
            a = v/Mach

            print ("la velocidad local del sonido es",a,"m/s")
            susm_main()
		
        susm_main()
    def  gravitacion():
        def gravitacion_main():
            print("\nElige una opción.\n1. Calcula la fuerza de atracción gravitatoria\n2. Calcular la distancia\n3. calcular la masa del cuerpo mayor\n4. Calcular la masa del cuerpo menor\n0. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                fuerza_G()
            elif opcion == 2:
                distancia()
            elif opcion == 3:
                masa_mayor()
            elif opcion == 4:
                masa_menor()
            elif opcion == 0:
                print("Saliendo...\n")
            else :
                print("Opción no válida.\n")
                gravitacion_main()
        def fuerza_G():
            r = float(input("ingrese la distancia en m: "))
            m1 = float(input("ingrese la masa del cuerpo mayor en kg: "))
            m2 = float(input("ingrese la masa del cuerpo menor en kg: "))
            G = 6.67408e-11
            F = G * (m1 * m2) / (r**2)

            print ("La fuerza de atracción es",F,"N")
            gravitacion_main()
        
        def distancia():
            F = float(input("ingrese la fuerza de atracción en N: "))
            m1 = float(input("ingrese la masa del cuerpo mayor en kg: "))
            m2 = float(input("ingrese la masa del cuerpo menor en kg: "))
            G = 6.67408e-11
            r = (G*m1*m2/F)**0.5
            print ("La distancia es",r,"m")
            gravitacion_main()
        
        def masa_mayor():
            F = float(input("ingrese la fuerza de atracción en N: "))
            r = float(input("ingrese la distancia en m: "))
            m2 = float(input("ingrese la masa del cuerpo menor en kg: "))
            G = 6.67408e-11
            m1 = (F*r**2)/(G*m2)
            print ("La masa del cuerpo mayor es",m1,"kg")
            gravitacion_main()
        def masa_menor():
            F = float(input("ingrese la fuerza de atracción en N: "))
            r = float(input("ingrese la distancia en m: "))
            m1 = float(input("ingrese la masa del cuerpo mayor en kg: "))
            G = 6.67408e-11
            m2 = (F*r**2)/(G*m1)
            print ("La masa del cuerpo menor es",m2,"kg")
            gravitacion_main()

        gravitacion_main()

    
    def ley_de_hooke():
        def hooke_main():
            print("\n Has elegido la ley de Hooke \n1. Calcular la fuerza reparadora elastica \n2. Calcular la constante elastica del muelle \n3. Calcular la elongacion del muelle \n0. Salir")
            opcion = int(input(". Elige una opcion: "))
            if opcion == 1:
                
                fre()
            elif opcion == 2:
        
                ke()
            elif opcion == 3:
                
                x()
            elif opcion == 0:
                print("Saliendo...")
            else:
                print("opcion no valida")
                hooke_main()
            
        def fre():
            print("\n Has elegido la fuerza reparadora elastica")
            k = float(input("constante elastica del muelle en N/m "))
            x = float(input("elongacion del muelle en m "))
            
            fre = k * x
            print("La fuerza reparadora elastica es: ", fre, "N")
            hooke_main()
        def ke():
            print("\n Has elegido la constante elastica del muelle")
            f = float(input("fuerza reparadora elastica en N "))
            x = float(input("elongacion del muelle en m "))
            ke = f / x
            print("La constante elastica del muelle es: ", ke, "N/m")
            hooke_main()
        def x():
            print("\n Has elegido la elongacion del muelle")
            f = float(input("Fuerza reparadora elastica en N: "))
            k = float(input("Constante elastica del muelle en N/m: "))
            x = f / k
            print("La elongacion del muelle es: ", x, "m")
            hooke_main()
        hooke_main()

        
    def v_esc():
        print("\nHas elegido la velocidad de escape")
        
        def v_esc_elegir():
            print("\nElige una opcion: \n1. Calcular la velocidad de escape del sistema\n2. Calcular la distancia\n3. Calcular la masa del cuerpo mayor\n0. Salir")
            opcion = int(input("elige una opción: "))
            
            if opcion == 1:
                v()
            elif opcion == 2:
                distancia()
            elif opcion == 3:
                masa()
            elif opcion == 0:
                print("Saliendo...\n")
            else:
                print("opción invalida")
                v_esc()

        def v():
            M = float(input("ingrese la masa del cuerpo mayor Kg: "))
            r = float(input("ingrese la distancia entre los cuerpos en metros: "))
            G = 6.6743*10**-11
            v = (2*G*M/r)**0.5
    
            print("La velocidad de escape es:",v,"m/s")
            v_esc_elegir()
    
        def distancia():
            M = float(input("ingrese la masa del cuerpo mayor Kg: "))
            G = 6.6743*10**-11
            v = float(input("ingrese la velocidad de escape en m/s: "))
            r = 2*G*M/v**2
            print("La distancia es:",r,"m")
            v_esc_elegir()

        def masa():
            R = float(input("ingrese la distancia entre los cuerpos en metros: "))
            G = 6.6743*10**-11
            v = float(input("ingrese la velocidad de escape en m/s: "))
            M = v_esc**2*R/(2*G)
            print("La masa del cuerpo mayor es:",M,"Kg")
            v_esc_elegir()
            
        v_esc_elegir()
    
    def fuem():
        def fuem_main():
            print("\nElige una opción\n1 Calcula la fuerza electrica\n2 Calcula la distancia entre las cargas\n3 Calcula la carga electrica del la carga 1\n4 Calcula la carga electrica del la carga 2 \n0 Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                fuee()
            elif opcion == 2:
                dist()
            elif opcion == 3:
                q1()
            elif opcion == 4:
                q2()
            elif opcion == 0:
                print("Saliendo...")
            else :
                print("Opción no válida.\n")
                fuem_main()
        
        def fuee():
            q1 = float(input("Introduce la carga de la carga 1 en Culombios: "))
            q2 = float(input("Introduce la carga de la carga 2 en Culombios: "))
            dist = float(input("Introduce la distancia entre las cargas en metros: "))
            k = 8.9875*10**9
            fuerza = k*q1*q2/dist**2
            print("La fuerza electrica es: ", fuerza, "N")
            fuem_main()
        
        def dist():
            q1 = float(input("Introduce la carga de la carga 1 en Culombios: "))
            q2 = float(input("Introduce la carga de la carga 2 en Culombios: "))
            fuerza = float(input("Introduce la fuerza electrica en Newtons: "))
            k = 8.9875*10**9
            dist = ((q1*q2*k)/fuerza)**0.5
            print("La distancia entre las cargas es: ", dist, "m")
            fuem_main()
        
        def q1():
            q2 = float(input("Introduce la carga de la carga 2 en Culombios: "))
            fuerza = float(input("Introduce la fuerza electrica en Newtons: "))
            dist = float(input("Introduce la distancia entre las cargas en metros: "))
            k = 8.9875*10**9
            q1 = (fuerza*dist**2)/(k*q2)
            print("el valor de la carga es:",q1,"C")
            fuem_main()
        
        def q2():
            q1 = float(input("Introduce la carga de la carga 1 en Culombios: "))
            fuerza = float(input("Introduce la fuerza electrica en Newtons: "))
            dist = float(input("Introduce la distancia entre las cargas en metros: "))
            k = 8.9875*10**9
            q2 = (fuerza*dist**2)/(k*q1)
            print("el valor de la carga es:",q2,"C")
            fuem_main()

        fuem_main()

    def relatividad_especial():
        def r_e():
            print("\nElige una opción: \n\t1. Calcula la energía\n\t2. Calcula la masa\n0. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                Energía()
            elif opcion == 2:
                Masa()
            elif opcion == 0:
                print("Saliendo")
            else:
                print("Opción no válida")
                r_e()
        
        def Energía():
            M =float(input("Ingrese la masa en kg: "))
            c = 299792458
            E = M*c**2
            print("La energía es: ", E,"J")
            r_e()
        def Masa():
            E = float(input("Ingrese la energía en J: "))
            c = 299792458
            M = E/c**2
            print("La masa es: ", M,"kg")
            r_e()
        
        r_e()

    def segunda_ley_de_newton():
        print ("\nHas elegido calcular la 2ª ley de Newton\n")

        def fm_main():
            print("Elige una opción:\n\t1. Calcular la fuerza motriz\n\t2. Calcular la eceleracíon\n\t3. Calcular la masa\n\t0. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                    fuerza_motriz()
            elif opcion == 2:
                aceleracion()
            elif opcion == 3:
                    masa()
            elif opcion == 0:
                print("Saliendo...\n")
            else :
                print("Opción incorrecta")
                fm_main()


        def fuerza_motriz():
            m = float(input("Ingrese la masa del cuerpo en kg: "))
            a = float(input("Ingrese la aceleracion del cuerpo en m/s^2: "))
            f = m*a

            print("La fuerza es: ", f ," N")
            fm_main()

        def aceleracion():
            m = float(input("Ingrese la masa del cuerpo en k: "))
            f = float(input("Ingrese la fuerza del cuerpo en Newtons: "))
            a = f/m

            print("La aceleracion es: ", a, "m/s^2")
            fm_main()

        def masa():
            f = float(input("Ingrese la fuerza del cuerpo en Newtons: "))
            a = float(input("Ingrese la aceleracion del cuerpo en m/s^2: "))
            m = f/a

            print("La masa es: ", m," kg")
            fm_main()
                    
        fm_main()
    def agujeros_negros():
        def main():
            print("\nElige una opción:\n1. Calcular el radio del agujero negro\n2 Calcular la masa del cuerpo atraido\n3. Salir")
            option = int(input("Elige una opción: "))

            if option == 1:
                radio()
            elif option == 2:
                masa()
            elif option == 0:
                print("Saliendo...")
            else:
                print("opcion no valida")
                main()
            
        def radio():
            G = 6.67428*10**-11
            M = float(input("Ingrese la masa del objeto en kg: "))
            if M < 0:
                print("La masa no puede ser negativa")
                radio()
            c = 299792458**2
            r = 2*G*M/c**2

            print ("El radio del agujero negros es",r,"m")

        def masa():
            G = 6.67428*10**-11
            M = float(input("Ingrese la masa del objeto en kg: "))
            if M < 0:
                print("La masa no puede ser negativa")
                masa()
            c = 299792458**2
            r = float(input("Ingrese el radio del agugero negro en metros: "))
            if r < 0:
                print("El radio no puede ser negativo")
                masa()
            M = r*c**2/(2*G)
            print ("La masa del cuerpo atraido es",M,"kg")

        main()

    def Peso():
        print ("\nHas elegido calcular el peso\n")

        def fm_main():
            print("\nElige una opción:\n1. Calcular la fuerza del peso\n2. Calcular la masa\n0. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                fuerza_del_peso()
            elif opcion == 2:
                masa()
            
            elif opcion == 0:
                print("Saliendo...\n")
            else :
                print("Opción incorrecta")
                fm_main()


        def fuerza_del_peso():
            m = float(input("Masa del cuerpo en kg: "))
            g = 9.8
            f = m*g

            print("Ingrese la la fuerza es: ", f," N")
            fm_main()


        def masa():
            f = float(input("Ingrese lafuerza del cuerpo en Newtons: "))
            g = 9.8
            m = f/g

            print("La masa es: ", m," kg")
            fm_main()
                    
        fm_main()


    def Ldo():
        def Ldo_main():
            print("\nElige una opción. \n1. Calcula la pontencia\n2. Calcula la intensidad\n3. Calcula la resistencia\n0. Salir")
            opcion = int(input("Elige una opción:"))
            if opcion == 1:
                V()
            elif opcion == 2:
                I()
            elif opcion == 3:
                R()
            elif opcion ==0:
                print("Saliendo...\n")
            else:
                print("Opción no válida. \n")
                Ldo_main()
        def V():
            I = float(input("Ingrese la intensidad en amperios: "))
            R = float(input("Ingrese la resistencia en ohmios: "))
            V = I*R
            print("La potencia es: ", V, "V")
            Ldo_main()
        
        def I():
            V = float(input("Ingrese la potencia en voltios: "))
            R = float(input("Ingrese la resistencia en ohmios: "))
            I = V/R
            print("La intensidad es: ", I, "A")
            Ldo_main()
        
        def R():
            V = float(input("Ingrese la potencia en voltios: "))
            I = float(input("Ingrese la intensidad en amperios: "))
            R = V/I
            print("La resistencia es: ", R, "Ω")
            Ldo_main()
        
        Ldo_main()

    def rozamiento():
        def rozamiento_main():
            print("\nelige una opción:\n1. fuerza de rozamiento\n2. coeficiente de rozamiento\n3. fuerza normal\n0. salir")
            option = int(input("Elige una opción: "))
            if option == 1:
                fue_roz()
            elif option == 2:
                coef_roz()
            elif option == 3:
                fue_normal()

            elif option == 0:
                print("Saliendo...")
            else:
                print("Opción no valida")
                rozamiento()

        
        def fue_roz():
            coe_roz = float(input("Ingrese el coeficiete de rozamiento: "))
            N = float(input("Ingrese la fuerza normal: "))

            fue_roz = coe_roz * N
            print("La fuerza de rozamiento es: ", fue_roz,"N")
            rozamiento_main()
        def coef_roz():
            fue_roz = float(input("Ingrese la fuerza de rozamiento: "))
            N = float(input("Ingrese la fuerza normal: "))
            rozamiento_main()
            coe_roz = fue_roz / N
            print("El coeficiente de rozamiento es: ", coe_roz)
            rozamiento_main()
        def fue_normal():
            fue_roz = float(input("Ingrese la fuerza de rozamiento: "))
            coe_roz = float(input("Ingrese el coeficiente de rozamiento: "))
            N = fue_roz / coe_roz
            print("La fuerza normal es: ", N,"N")
            
            rozamiento_main()


        rozamiento_main()






    def tiro():
    #repsaarrrrrr martin ----------------------------------       
        def tiro_elegir():
            print("\nElige una opción. \n1. Calcula la altura máxima\n2. Calcular el angulo para una distacia dada\n3. Calcular el tiempo de vuelo\n4. Calcular la distancia horizontal\n0. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                altura_maxima()
            
            elif opcion ==2:
                calcular_angulo()
            
            elif opcion == 3:
                calcular_tiempo_vuelo()
            
            elif opcion == 4:
                calcular_distancia_horizontal()
            
            elif opcion == 0:
                print("Gracias por usar el programa")
                tiro()
            
            else:
                print("Opción no válida")
                tiro()
                
            
            
        def altura_maxima():
            velocidad_inicial = float(input("Ingrese la velocidad inicial en m/s: "))
            angulo_de_tiro = float(input("Ingrese el angulo de tiro: "))
            g = 9.8
            angulo_radianes = math.radians(angulo_de_tiro)
            altura_max = (velocidad_inicial ** 2 * (math.sin(angulo_radianes) ** 2)) / (2 * g)
            print("La altura máxima alcanzada es:", altura_max, "metros")

        def calcular_angulo():
            angulo_rad = math.atan((9.81 * distancia) / (velocidad_inicial ** 2))
            angulo_grados = math.degrees(angulo_rad)
            distancia = float(input("Ingrese la distancia a la que llegará el proyectil en m: "))
            velocidad_inicial = float(input("Ingrese la velocidad inicial en m/s: "))
            angulo_necesario = calcular_angulo(distancia, velocidad_inicial)
            print("El ángulo necesario para lograr una distancia de", distancia, "metros es:", angulo_necesario, "grados")
        
        def calcular_tiempo_vuelo():
            tiempo_vuelo = (2 * velocidad_inicial * math.sin(math.radians(angulo_de_tiro))) / 9.81
            velocidad_inicial = float(input("Ingrese la velocidad inicial en m/s: "))
            angulo_de_tiro = float(input("Ingrese el ángulo de tiro en grados: "))
            g = 9.8
            tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo_de_tiro)
            print("El tiempo de vuelo en un tiro parabólico es:", tiempo_vuelo, "segundos")
            
        def calcular_distancia_horizontal():
            tiempo_vuelo = (2 * velocidad_inicial * math.sin(math.radians(angulo_de_tiro))) / 9.81
            distancia_horizontal = velocidad_inicial * math.cos(math.radians(angulo_de_tiro)) * tiempo_vuelo
            velocidad_inicial = float(input("Ingrese la velocidad inicial en m/s: "))
            angulo_de_tiro = float(input("Ingrese el angulo de tiro: "))
            distancia_horizontal = calcular_distancia_horizontal(velocidad_inicial, angulo_de_tiro)
            print("La distancia horizontal recorrida en un tiro parabólico es:", distancia_horizontal, "metros")
        
        tiro_elegir()

    def ley_gases_ideales():
        print("\n¡Has elegido la Ley de los Gases Ideales!")
        
        gas = input("¿Qué dato quieres hallar (P, V, n, T)?: ").lower()

        R = 0.0821  

        if gas == "p":
            V = float(input("Ingrese el volumen del gas en m^3: "))
            n = float(input("Ingrese el numero de moles: "))
            T = float(input("Ingrese la temperatura en kelvin: "))
            P = (6.022*10**23*n * R * T) / V
            print("La presión es P:", P,"atm")

        elif gas == "v":
            P = float(input("Ingrese la presión del gas en atm: "))
            n = float(input("Ingrese el numero de moles: "))
            T = float(input("Ingrese la temperatura en kelvin: "))
            V = (6.022*10**23*n * R * T) / P
            print("El volumen es V:", V,"m^3")

        elif gas == "n":
            P = float(input("Ingrese la presión del gas en atm: "))
            V = float(input("Ingrese el volumen del gas en m^3: "))
            T = float(input("Ingrese la temperatura en kelvin: "))
            n = (P * V) / (R * T*6.022*10**23)
            print("El número de moles del gas es:", n)

        elif gas == "t":
            P = float(input("Ingrese la presión del gas en atm: "))
            V = float(input("Ingrese el volumen del gas en m^3: "))
            n = float(input("Ingrese el numero de moles: "))
            T = (P * V) / (n *6.022*10**23 * R)
            print("La temperatura es T:", T,"Kelvin")

        else:
            print("No has introducido una opción válida. Por favor, introduce P, V, n o T.")


    def factores_de_conversion():
        

        def convertir_unidades_g():
            print("\n¡Has elegido convertir unidades de masa!")
            unidades = {"kg": 1000, "hg": 100, "dag": 10, "g": 1, "dg": 0.1, "cg": 0.01, "mg": 0.001}
            unidad_origen = input("¿Cuál es la unidad de origen (kg, hg, dag, g, dg, cg, mg)?: ").lower()
            unidad_destino = input("¿Cuál es la unidad de destino (kg, hg, dag, g, dg, cg, mg)?: ").lower()
            valor = float(input("¿Cuál es el valor que quieres convertir?: "))

            if unidad_origen not in unidades or unidad_destino not in unidades:
                print("Has introducido una unidad no válida. Por favor, introduce kg, hg, dag, g, dg, cg o mg.")
                return

            valor_gramos = valor * unidades[unidad_origen]
            valor_convertido = valor_gramos / unidades[unidad_destino]

            print(f"{valor} {unidad_origen} son {valor_convertido} {unidad_destino}")
            factores_de_conversion()

        def convertir_unidades_m():
            print("\n¡Has elegido convertir unidades de longitud!")
            unidades = {"km": 1000, "hm": 100, "dam": 10, "m": 1, "dm": 0.1, "cm": 0.01, "mm": 0.001}
            unidad_origen = input("¿Cuál es la unidad de origen (km, hm, dam, m, dm, cm, mm)?: ").lower()
            unidad_destino = input("¿Cuál es la unidad de destino (km, hm, dam, m, dm, cm, mm)?: ").lower()
            valor = float(input("¿Cuál es el valor que quieres convertir?: "))

            if unidad_origen not in unidades or unidad_destino not in unidades:
                print("Has introducido una unidad no válida. Por favor, introduce km, hm, dam, m, dm, cm o mm.")
                return

            valor_metros = valor * unidades[unidad_origen]
            valor_convertido = valor_metros / unidades[unidad_destino]

            print(f"{valor} {unidad_origen} son {valor_convertido} {unidad_destino}")
            factores_de_conversion()
        
        def convertir_unidades_l():
            print("\n¡Has elegido convertir unidades de litros!")
            unidades = {"kl": 1000, "hl": 100, "dal": 10, "L": 1, "dl": 0.1, "cl": 0.01, "ml": 0.001}
            unidad_origen = input("¿Cuál es la unidad de origen (kl, hl, dal, L, dl, cl, ml)?: ").lower()
            unidad_destino = input("¿Cuál es la unidad de destino (kl, hl, dal, L, dl, cl, ml)?: ").lower()
            valor = float(input("¿Cuál es el valor que quieres convertir?: "))

            if unidad_origen not in unidades or unidad_destino not in unidades:
                print("Has introducido una unidad no válida. Por favor, introduce kl, hl, dal, L, dl, cl o ml.")
                return

            valor_metros = valor * unidades[unidad_origen]
            valor_convertido = valor_metros / unidades[unidad_destino]

            print(f"{valor} {unidad_origen} son {valor_convertido} {unidad_destino}")
            factores_de_conversion()

        def convertir_unidades_T():
            print("\n¡Has elegido convertir unidades de tiempo!")
            unidades = {"h": 3600, "min": 60, "s": 1, "ms": 0.001, "us": 1e-6, "ns": 1e-9}
            unidad_origen = input("¿Cuál es la unidad de origen (h, min, s, ms, us, ns)?: ").lower()
            unidad_destino = input("¿Cuál es la unidad de destino (h, min, s, ms, us, ns)?: ").lower()
            valor = float(input("¿Cuál es el valor que quieres convertir?: "))

            if unidad_origen not in unidades or unidad_destino not in unidades:
                print("Has introducido una unidad no válida. Por favor, introduce h, min, s, ms, us o ns.")
                return

            valor_segundos = valor * unidades[unidad_origen]
            valor_convertido = valor_segundos / unidades[unidad_destino]

            print(f"{valor} {unidad_origen} son {valor_convertido} {unidad_destino}")
            factores_de_conversion()





        print("\nEn que unidad quieres trabajar:"
            
            "\n\t1. distancia"
            "\n\t2. masa"
            "\n\t3. litro"
            "\n\t4. Tiempo"
            
            
            
            
            
            
            )
        factores = input("Ingrese el número de la opción deseada: ")
        if factores == "1":
            convertir_unidades_m()
        elif factores =="2":
            convertir_unidades_g()
        elif factores =="3":
            convertir_unidades_l()
        elif factores =="4":
            convertir_unidades_T()
    
    def pascal():
        def pascmain():
            print("\nElige una opción. \n1. Calcula la presión\n2. Calcula la fuerza\n3. Calcula la superficie\n0. Salir")
            opc = int(input("Opción: "))
            if opc == 1:
                presion()
            elif opc == 2:
                fuerza()
            elif opc == 3:
                superficie()
            elif opc == 0:
                print("Saliendo...")
                pascal()
            else:
                print("Opción incorrecta")
        

        def presion():
            F = float(input("Ingrese la fuerza en N: "))
            A = float(input("Ingrese la superficie en m^2: "))
            P = F/A
            print("La presión es: ", P, "Pascales")
            pascmain()
        
        def fuerza():
            P = float(input("Ingrese la presión en Pascales: "))
            A = float(input("Ingrese la superficie en m^2: "))
            F = P*A
            print("La fuerza es: ", F, "N")
            pascmain()
        
        def superficie():
            P = float(input("Ingrese la presión en Pascales: "))
            F = float(input("Ingrese la fuerza en N: "))
            S = F/P
            print("La superficie es: ", S, "m^2")
            pascmain()
        
        pascmain()

    

    def  main_fyq():
        print(
            
            "Elige una opcion:"
            "\n\t1. MRU y MRUA      6. Gravitacion            11. Segunda ley de Newton       16. Tiro parabolico             "       
            "\n\t2. Sustentacion    7. Ley de hooke           12. Agujero negros              17. Ley de los gases ideales"
            "\n\t3. Flujo           8. Velocidad de escape    13. Peso                        18. Factores de conversión"
            "\n\t4. Densidad        9. Fuerza electrica       14. Ley de Ohm                  19. Pascal"
            "\n\t5. Mach            10. Relatividad especial  15. Fuerza de rozamiento" 
            "\n\t                                                                             0. Salir"
            ""
            ""



                )

        elejir_f = input("Ingrese el número de la opción deseada:  ")
                    
        if elejir_f == "mru" or elejir_f == "mrua" or elejir_f == "mru y mrua" or elejir_f == "1":    
            mrumrua()

        elif elejir_f == "sustentacion" or elejir_f == "2":
            sustentacion()
            
        elif elejir_f == "Flujo " or elejir_f=="3":
            fluidos()

        elif elejir_f == "densidad" or elejir_f == "4":
            densidad_de_la_sus()

        elif elejir_f == "5" or elejir_f == "Mach":
            Formula_de_Mach()

        elif elejir_f == "6" or elejir_f == "gravitacion":
            gravitacion()

        elif elejir_f == "7" or elejir_f == "ley de hooke":
            ley_de_hooke()

        elif elejir_f == "8" or elejir_f == "velocidad de escape":
            v_esc()
        
        elif elejir_f == "9" or elejir_f == "fuerza electrica":
            fuem()

        elif elejir_f == "10" or elejir_f == "relatividad especial":
            relatividad_especial()

        elif elejir_f == "11" or elejir_f == "Segunda ley de Newton":
            segunda_ley_de_newton()

        elif elejir_f == "12" or elejir_f == "agujeros negros":
            agujeros_negros()
            
        elif elejir_f == "13" or elejir_f == "Peso":
            Peso()

        elif elejir_f == "14" or elejir_f == "Ley Ohm":
            Ldo() 

        elif elejir_f == "15" or elejir_f == "Fuerza de rozamiento":
            rozamiento()
        
        elif elejir_f == "16" or elejir_f == "tiro parabolico":
            tiro()
        elif elejir_f == "17" or elejir_f == "ley de los gases ideales":
            ley_gases_ideales()
        elif elejir_f =="18":
            factores_de_conversion()
        elif elejir_f =="19":
            pascal()


            
        


        elif elejir_f == "0":
            print("\nSaliendo...\n")

        else: 
            print(" Opcion ivalida")
            main_fyq()
    main_fyq()








###################################################################################33333333333333333333333333333333
3333333###################################################################################········
#---------------------TERMINA EL CODIGO DE FYQ---------------------------------##########
#####################------------------MATES---------------------------------############


def mates():

    def ec_2():
        print('¡Hola! Vamos a resolver una ecuación de segundo grado:')
        print('    ax² + bx + c = 0\n')
        # pedimos los coeficientes al usuario

            
        a, b, c = [float(input(f'Dame el coeficiente: {coef}: ')) for coef in ('a', 'b', 'c')]


            ##########################################
        discriminante =  b ** 2 - 4 * a * c
                #####################################ç 

        if discriminante == 0: 
                x_1 =  -b/ (2 * a) 
                soluciones = (x_1, x_1) 
                print(soluciones)   
                mfmain()
        elif discriminante > 0:
                x_1 = (-b+sqrt(discriminante))//(2*a)
                x_2 = (-b-sqrt(discriminante))//(2*a)
                soluciones = (x_1, x_2)
                print(soluciones)   
            
        elif discriminante <0:
                print("                    ")
                print("no hay soluciones :(")                              
                mfmain() 
        else:     
                x_1 = (-b+cmath.sqrt(discriminante))//(2*a)
                x_2 = (-b-cmath.sqrt(discriminante))//(2*a)
        
                
                print(soluciones) 
                mfmain()
        print("----------------------")

    def dado():
        
        p1, p2 = map(int, input("inserta el minimo y el maximo del dado (separados con un espacio o con una y): ").split(" y " or " "))
        num_lanzamientos = int(input("¿Cuántas veces quieres lanzar el dado? "))

        for i in range(num_lanzamientos):
            dado = random.randint(p1, p2)
            print("El resultado del lanzamiento {} es: {}".format(i+1, dado))
        main_mates()



    def funciones_grafica():
        def elegir_funcion():
            while True:
                print("\nHas elegido Funciones con graficas!")
                print("Elige una opción:\n\t1. Función lineal\n\t2. Función cuadrática\n\t0. Salir")
                opcion = int(input("Ingrese el número de la opción deseada: "))
                if opcion == 1:
                    funcion_lineal()
                elif opcion == 2:
                    funcion_cuadratica()
                elif opcion == 0:
                    print("Saliendo...")
                    break
                else:
                    print("Opción incorrecta")

        def funcion_lineal():
            coeficiente_de_x = float(input("\nIngrese el coeficiente de x: "))
            termino_independiente = float(input("Ingrese el valor del término independiente: "))
            
            x = range(-100, 101)
            fx = [coeficiente_de_x * x_val + termino_independiente for x_val in x]
            
            plt.figure()
            plt.plot(x, fx, label="Función Lineal")
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.grid(True)
            plt.xlim(-100, 100)
            plt.ylim(-100, 100)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.title("Gráfica de la Función Lineal")
            plt.show()
        
        def funcion_cuadratica():
            coeficiente_de_x_cuadrado = float(input("\nIngrese el coeficiente de x^2: "))
            coeficiente_de_x = float(input("Ingrese el coeficiente de x: "))
            termino_independiente = float(input("Ingrese el valor del término independiente: "))
            
            x = range(-100, 101)
            fx = [coeficiente_de_x_cuadrado * (x_val**2) + coeficiente_de_x * x_val + termino_independiente for x_val in x]
            
            plt.figure()
            plt.plot(x, fx, label="Función Cuadrática")
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.grid(True)
            plt.xlim(-100, 100)
            plt.ylim(-100, 100)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.title("Gráfica de la Función Cuadrática")
            plt.show()
        
        elegir_funcion()


    def funciones_sin_grafica():
        def elegir_funcion():
            print("\nHas elejido Funciones sin grafica!")
            print("Elige una opción\n\t1. Función lineal\n\t2. Función cuadrática\n\t0. Salir")
            opcion = int(input("Ingrese el número de la opción deseada: " ))
            if opcion == 1:
                funcion_lineal()
            elif opcion == 2:
                funcion_cuadratica()
            elif opcion == 0:
                print("Saliendo...")
            else:
                print("Opción incorrecta")
                elegir_funcion()
            
        def funcion_lineal():
            coeficiente_de_x = float(input("\nIngrese el coeficiente de x: "))
            termino_independiente = float(input("Ingrese el valor del término independiente: "))
            
            for x in range(-5, 6):
                fx = [coeficiente_de_x * x_val + termino_independiente for x_val in x]
                print(f"Para x = {x}, f(x) = y es igual a {fx}")

        def funcion_cuadratica():
            coeficiente_de_x_cuadrado = float(input("\nIngrese el coeficiente de x^2: "))
            coeficiente_de_x = float(input("Ingrese el coeficiente de x: "))
            termino_independiente = float(input("Ingrese el valor del término independiente: "))

            for x in range(-5, 6):
                fx = [coeficiente_de_x_cuadrado * (x_val**2) + coeficiente_de_x * x_val + termino_independiente for x_val in x]
                print(f"Para x = {x}, f(x) = y es igual a {fx}")
        
        elegir_funcion()

    def area_circulo():
        radio = float(input("Introduce el radio del círculo: "))
        area = math.pi * (radio ** 2)
        print(f"El área del círculo con radio {radio} es: {area}")

    from mpmath import mp

    def calcular_pi():
        def pi(precision):
            mp.dps = precision  # establece el número de decimales
            pi = mp.pi
            return str(pi)

        precision = int(input("\nIntroduce el número de decimales para Pi: "))
        pi_con_precision = pi(precision)
        print(f"Pi con {precision} decimales es: {pi_con_precision}")

    def mcm_main():
        def mcd(a, b):
            while b != 0:
                a, b = b, a % b
            return a

        def mcm(a, b):
            return abs(a*b) // mcd(a, b)

        num1 = int(input("\nIntroduce el primer número: "))
        num2 = int(input("Introduce el segundo número: "))
        resultado = mcm(num1, num2)
        print(f"El mínimo común múltiplo de {num1} y {num2} es: {resultado}")

    def binarioo():
        def menu():
            print("\n[------------------------------------------------]")
            print("[---------------------Binario--------------------]")
            print("[------------------------------------------------]")
            print("  1. Texto a binario")
            print("  2. Binario a texto")
            print("  3. Salir")
            opcion = int(input("Elige una opción: \n"))
            return opcion

        def main_bi():
            def texto_a_binario(texto):
                binario = ' '.join(format(ord(caracter), '08b') for caracter in texto)
                return binario

            def binario_a_texto(binario):
                binario = binario.replace(',', ' ').replace('\xa0', ' ').split(" ")
                texto = ""
                for binario_caracter in binario:
                    if len(binario_caracter) == 8:  # Solo intenta convertir subcadenas de 8 bits
                        texto += chr(int(binario_caracter, 2))
                return texto

            while True:
                opcion = menu()
                if opcion == 1:
                    print("\n[--------------------Texto a Binario--------------]")
                    texto = input("Introduce el texto que quieres traducir a binario: ")
                    resultado = texto_a_binario(texto)
                    print(f"El texto '{texto}' en binario es: {resultado}")
                elif opcion == 2:
                    print("\n[--------------------Binario a Texto----------------------]")
                    binario = input("Introduce el código binario que quieres traducir a texto: ")
                    resultado = binario_a_texto(binario)
                    print(f"El código binario '{binario}' en texto es: '{resultado}'")
                elif opcion == 3:
                    print("Saliendo del programa...")
                    break
                else:
                    print("Opción no válida. Por favor, elige una opción del menú.")
        main_bi()

            


    def main_mates():
        print(
            "\n Elige una opcion:"
            "\n\t1. Ecuacion de segundo grado"
            "\n\t2. Funciones sin grafica"
            "\n\t3. Funciones con grafica"
            "\n\t4. Dado"
            "\n\t5. Area del circulo"
            "\n\t6. Calcular Pi"
            "\n\t7. Minimo Comun Multiplo"
            "\n\t8. Binario"
            
            
            )
        elegir_mates=input("Ingrese el número de la opción deseada: ").lower()
        
        if elegir_mates == "1" or elegir_mates == "Ecuacion de segundo grado":
            ec_2()
        elif elegir_mates == "3" or elegir_mates == "funcion con grafica":
            funciones_grafica()
        elif elegir_mates == "2" or elegir_mates == "funcion sin grafica":
            funciones_sin_grafica()
        elif elegir_mates == "4" or elegir_mates == "dado":
            dado()
        elif elegir_mates == "5":
            area_circulo()
        elif elegir_mates == "6":
            calcular_pi()
        elif elegir_mates == "7":
            mcm_main()
        elif elegir_mates == "8":
            binarioo()

    main_mates()




def ejecutar_MFQ_All():
            os.chdir('C:\\Users\\Usuario\\OneDrive\\Documentos\\Python\\Pruebas\\mates')
            subprocess.run('start cmd /K python MFQ_all.py', shell=True)
    
#################################################################################
#################################################################################h
#################################################################################



#######################-------------------MAIN-------------######################

def mfmain():
    keyboard.add_hotkey('ctrl + alt', ejecutar_MFQ_All)
    while 1<2:
        fom = input("Quieres FyQ o Mates: ").lower()
        if fom == "fyq":
            fyq()
        elif fom == "mates" or fom == "m":
            mates()#noooo se ejecuta  esta mierda ayudaaaaaaaaaaaaaaaaaaaaa                                               
        else:
            print("Escribe una opcion valida por favor")
            mfmain()

mfmain()