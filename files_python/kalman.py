import math
from turtle import delay
#import matplotlib 
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
 
#import matplotlib.pyplot as plt
#import numpy as np

lista = []
archivos = ["./mr74_49.txt","./mr74_6d.txt","./mr74_5b.txt","./mr44_6d.txt","./mr44_5b.txt","./mr44_49.txt","./mr44_49_b.txt","./mr33_6d.txt","./mr33_6d_b.txt","./mr33_5b.txt","./mr33_49.txt"]
promedios = []
for i in archivos:
    lista = []
    with open(i) as archivo:
        for linea in archivo:
            lista.append(int(linea.strip()))
            #print(linea)

    #print(lista)


    class KalmanFilter:
        cov = float('nan')
        x = float('nan')
        def __init__(self, R, Q):
            """
            Constructor
            :param R: Process Noise
            :param Q: Measurement Noise
            """
            self.A = 1
            self.B = 0
            self.C = 1

            self.R = R
            self.Q = Q

        def filter(self, measurement):
            """
            Filters a measurement
            :param measurement: The measurement value to be filtered
            :return: The filtered value
            """
            u = 0
            if math.isnan(self.x):
                self.x = (1 / self.C) * measurement
                self.cov = (1 / self.C) * self.Q * (1 / self.C)
            else:
                predX = (self.A * self.x) + (self.B * u)
                predCov = ((self.A * self.cov) * self.A) + self.R

                # Kalman Gain
                K = predCov * self.C * (1 / ((self.C * predCov * self.C) + self.Q));

                # Correction
                self.x = predX + K * (measurement - (self.C * predX));
                self.cov = predCov - (K * self.C * predCov);

            return self.x

        def last_measurement(self):
            """
            Returns the last measurement fed into the filter
            :return: The last measurement fed into the filter
            """
            return self.x

        def set_measurement_noise(self, noise):
            """
            Sets measurement noise
            :param noise: The new measurement noise
            """
            self.Q = noise

        def set_process_noise(self, noise):
            """
            Sets process noise
            :param noise: The new process noise
            """
            self.R = noise

    test = KalmanFilter(0.01, 5)
    testData = lista
    filtrado = []
    for x in testData:
        print ("Data:", x)
        filtrado.append(test.filter(x))
        print ("Filtered Data: ", test.filter(x))
    print(filtrado)

    #Gráficas
    lista1 = lista
    plt.plot(lista1)   # Dibuja el gráfico
    plt.xlabel("abscisa")   # Inserta el título del eje X
    plt.ylabel("ordenada")   # Inserta el título del eje Y
    plt.ioff()   # Desactiva modo interactivo de dibujo
    lista2 = filtrado
    plt.plot(lista2)   # No dibuja datos de lista2
    plt.ion()   # Activa modo interactivo de dibujo
    plt.plot(lista2)   # Dibuja datos de lista2 sin borrar datos de lista1
    plt.show(block = True)
    #delay(60)
    promedio_datos  = sum(lista)/len(lista)
    promedio_filtro = sum(filtrado)/len(filtrado)

    print("Promedio sin filtro: ", promedio_datos, "  Promedio con filtro: ",promedio_filtro)
    promedios.append(promedio_filtro)

print("\n", promedios)
print("El promedio final para un metro es: ",sum(promedios)/len(promedios))