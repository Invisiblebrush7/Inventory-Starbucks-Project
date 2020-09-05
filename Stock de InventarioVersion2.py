import pandas as pd
import matplotlib.pyplot as plt 
from math import ceil
import time

Excel_File = 'InventarioVersion2.xlsx'
Lista = pd.read_excel(Excel_File,'Inventario')  #Inventory Data Frame
Nomenclatura = pd.read_excel(Excel_File,'Nomenclatura')  #Nomenclatura Data Frame
Duracion = pd.read_excel(Excel_File,'Duracion')     #Expiration Dates Data Frame

nRows = len(Lista.axes[0])
nCols = 0
Lista_Nomenclatura = []
Indice = 0
while(Indice<nRows):
    for item in Lista.iloc[Indice]:
        Lista_Nomenclatura.append(item)
    Indice += 1

for Columna in Lista.iloc[1]:
    nCols +=1

#Sales Analysis Feature

#First Feature: Graph analysis of your sales
#Lista_Nomenclatura es una lista con todas las Nomenclaturas en el File
#Lista.iloc[0] ---> First Row of the Lista Dataframe
#Nombre, Inicial, Domingo1,D2,D3,D4

def Sales_Graphs(Lista_Ventas, Producto):
    #Lista de Ventas = Y's
    #Domingos = X's
    Valores_X = [1,2,3,4]

    plt.scatter(Valores_X,Lista_Ventas)
    plt.title('Ventas de ' + str(Producto))
    plt.ylabel('Cantidad')
    plt.xlabel('Semanas')
    plt.show()
    

def Sales_Analysis(Lista_De_Productos):
    for index in range(0,nRows):
        Item_Actual = Lista.iloc[index]
        if (Item_Actual[0] in Lista_De_Productos ):
            Ventas = []
            Cantidad_Anterior = Item_Actual[1]
            for Columna in Item_Actual[2:6]:
                Venta = abs(Columna-Cantidad_Anterior)
                Ventas.append(Venta)
                Cantidad_Anterior = Columna
            Sales_Graphs(Ventas,Item_Actual[0])




def Menu():
    print("-"*50)
    print("Bienvenido al sistema de reportes de alimentos.")
    print("Para iniciar con el análisis, elige una de las siguientes opciones:")
    time.sleep(1)
    print("1. Análisis de un solo producto.")
    print("2. Análisis de diversos productos")
    print("3. Análisis de todos los productos.")
    print("4. Ver toda la nomenclatura de los productos.")
    print("5. Análisis de Ventas")
    print("6. Salir")
    print("-"*50)
    while (True):
        try:
            Opcion = int(input("Elige el número de tu elección:"))
        except:
            print("Ingresa un número")
        else:
            break
    
    return int(Opcion)

def Continuar():
    time.sleep(1)
    print("¿Desea volver a realizar alguna acción?")
    Opcion = int(input("1. Si\n2. No\n"))
    return Opcion
    
def Imprimir_Nomenclatura ():
    Indice = 0
    nRows = len(Lista.axes[0])
    while (Indice < nRows):    
        for Producto in Nomenclatura.iloc[Indice]:
            if (len(Producto) > 1 and len(Producto)<=3 ):
                print(Producto,end=": ")
            else:
                print(Producto)
        
        Indice += 1

def Comprobar_Nomenclatura(Producto):
    global Lista_Nomenclatura
    if (Producto not in Lista_Nomenclatura):
        return 0
    else:
        return 1
def Comprobar_Existencia_enLista(Lista_Alimentos,Alimento):
    if (Producto in Lista_Alimentos):
        return 1
    elif (Producto not in Lista_Alimentos):
        return 0

def Revisar_Caducidad(Producto):
    global nCols
    
    for index in range(0,nCols):
        if (Duracion.iloc[index][0] == Producto):
            return Duracion.iloc[index][1]

def Analisis(Productos):
    global nRows
    
    for item in Productos:  #Revisa cada item en la lista que el usuario quiere ver.
        index = 0
        Suma = 0
        Contador_De_Valores = 0
        Contador_Columna = 0
        while (index<nRows): #Mientras que el index no sobrepase al numero de Rows
            Item_Actual = Lista.iloc[index] #Revisa la columna con el indice *index
            if (Item_Actual[0] == item):    #Si es el item buscado, haz analisis
                for Columna in Item_Actual: #Revisa cada columna en el renglon.
                    if (Columna == item):   #Olvidamos la primera columna. No es un int
                        Contador_Columna+=1
                    elif (Columna == Item_Actual[1] and Contador_Columna == 1):
                        Cantidad_Inicial = Columna
                        Actual = Cantidad_Inicial
                        Contador_Columna +=1
                    else:
                        Suma = Suma + (Actual - Columna)
                        Actual = Columna
                        Contador_De_Valores +=1
                
                Promedio_Semanal = Suma/Contador_De_Valores
                Fin = Cantidad_Inicial/Promedio_Semanal
                Fin_Dias = Fin*7
                print("-"*70)
                print ("Total de",item,"Vendidos:",Suma)
                print("El promedio de Ventas semanal es de:",round(Promedio_Semanal,1),"por semana.")
                print("Con este promedio, el producto se terminará en",round(Fin,1),"semanas/",round(Fin_Dias,2),"días.")
                print("")
                
                #Inicia analisis con Caducidad
                Caducidad = Revisar_Caducidad(item)
                Cantidad_Inicial_Optima = Caducidad*Cantidad_Inicial/Fin_Dias
                print("Este alimento caduca en",Caducidad,"días.")
                print ("Con este promedio de ventas, la cantidad inicial óptima de",item,"es",str(round(Cantidad_Inicial_Optima,0)) + ".")
                print("")
                
                
                break
            index+=1
        Regresion_Lineal(index)
        time.sleep(1)
    print("-"*20,"Fin de analisis","-"*20)
    time.sleep(1)
    

def Regresion_Lineal (index):
    global nRows
    Valores_X = [0,1,2,3,4]
    Valores_Y = []
    for valor in Lista.iloc[index]:
        if (type(valor) == str):
            Alimento = valor
        else:
            Valores_Y.append(valor)
    
    SumaX = 0
    SumaY = 0
    MultiplicaXY = 0
    XCuadradas = 0
    indice = 0
    for valor in Valores_X:
        SumaX = SumaX + valor
        XCuadradas = XCuadradas + valor*valor
    for valor in Valores_Y:
        SumaY = SumaY + valor
        
    PromedioX = SumaX/5
    PromedioY = SumaY/5
    
    indice = 0
    while(indice<5):
        MultiplicaXY = MultiplicaXY + Valores_X[indice]*Valores_Y[indice]
        indice+=1
    
    
    Pendiente = (5*MultiplicaXY - SumaX*SumaY)/(5*XCuadradas -(SumaX)*(SumaX))
    B = PromedioY - Pendiente*PromedioX
    
    Fin_Alimento = -B/Pendiente
    
    X = Valores_X
    Y = []
    Valor = 0
    while (len(Y) != 5):
        Y.append(X[Valor]*Pendiente + B)
        Valor+=1
    
    print("Según el estudio de la regresión lineal del producto, se terminará en",round(Fin_Alimento,1),"semanas/",ceil(Fin_Alimento*7),"dias.")
    
    plt.scatter(X,Valores_Y)
    plt.title(Alimento)
    plt.ylabel('Inventario')
    plt.xlabel('Semanas')
    plt.plot(X,Y)
    plt.show()

Opcion = Menu()
while (Opcion != 6):
    Lista_De_Productos = []
    #-----------------------Opcion 1 --------------------------
    if (Opcion == 1):
        Producto = input("Ingresa el producto a analizar:")
        while (Comprobar_Nomenclatura(Producto) == 0):
            print ("Producto No Válido. Revise la tabla de Nomenclaturas para más información.")
            Producto = input("Ingresa el producto a analizar:")
        if (Producto != "SALIR"):
            Lista_De_Productos.append(Producto)
            Analisis(Lista_De_Productos)
    #-----------------------Opcion 2 --------------------------
    elif (Opcion == 2):
        Producto = input("Ingresa uno de los productos a analizar o ingrese NA para finalizar la lista:")        
        while (Producto != "NA"):
            Estado = Comprobar_Nomenclatura(Producto)
            Existencia = Comprobar_Existencia_enLista(Lista_De_Productos,Producto)
            if (Estado == 0):
                print ("Producto No Válido. Revise la tabla de Nomenclaturas para más información.")
                print("")
                time.sleep(1)
            elif (Estado == 1 and Existencia == 0):
                Lista_De_Productos.append(Producto)
                print("Alimentos por analizar:",Lista_De_Productos)
            elif (Estado == 1 and Existencia == 1 ):
                print("Producto ya en la lista.")
            Producto = input("Ingresa uno de los productos a analizar o ingrese NA para finalizar la lista:")                    
        Analisis(Lista_De_Productos)
    #-----------------------Opcion 3 --------------------------
    elif (Opcion == 3):
        Indice = 0
        while (Indice < nRows):
            Producto = Lista.iloc[Indice][0]
            Lista_De_Productos.append(Producto)
            Indice +=1
        Analisis(Lista_De_Productos)
    #-----------------------Opcion 4 --------------------------
    elif (Opcion == 4):
        Imprimir_Nomenclatura()
    #-----------------------Opcion 5 --------------------------
    elif (Opcion == 5):
        Producto = input("Ingresa uno de los productos a analizar o ingrese NA para finalizar la lista:")        
        while (Producto != "NA"):
            Estado = Comprobar_Nomenclatura(Producto)
            Existencia = Comprobar_Existencia_enLista(Lista_De_Productos,Producto)
            if (Estado == 0):
                print ("Producto No Válido. Revise la tabla de Nomenclaturas para más información.")
                print("")
                time.sleep(1)
            elif (Estado == 1 and Existencia == 0):
                Lista_De_Productos.append(Producto)
                print("Alimentos por analizar:",Lista_De_Productos)
            elif (Estado == 1 and Existencia == 1 ):
                print("Producto ya en la lista.")
            Producto = input("Ingresa uno de los productos a analizar o ingrese NA para finalizar la lista:")
        Sales_Analysis(Lista_De_Productos)
        print("-"*20,"Fin de analisis","-"*20)
        time.sleep(1)
    
    
    Opcion = Continuar()
    if (Opcion == 1):
        Opcion = Menu()
    elif (Opcion == 2):
        Opcion = 6
        print ("Gracias por usar los servicios de Bets!")
        print ("Hasta luego!")
