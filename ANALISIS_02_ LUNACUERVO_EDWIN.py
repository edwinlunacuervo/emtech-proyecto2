from operator import itemgetter
import csv

lista_datos = []

#ABRIMOS Y LEEMOS EL ARCHIVO CSV COMO DICCIONARIO Y AÑADIMOS LA INFORMACION A UNA LISTA
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    
    for registro in lector:
        lista_datos.append(registro)


        


#OPCIÓN 1,  RUTAS MAS DEMANDADAS


#LA FUNCION rutas_exportacion_importacion  REALIZA EL CONTEO DE CUANTAS VECES APARECE
#UNA RUTA. EL ARGUMENTO DE LA FUNCION ES "direccion", DONDE SE ESPERA QUE SE INTRODUZCA
#"EXPORTS" O "IMPORTS"
def rutas_exportacion_importacion (direccion):
    contador = 0
    dinero=0
    rutas_contadas = []
    rutas_conteo = []
    medio=[]

  
   #FIJAMOS UN VALOR (ruta_actual)
    for ruta in lista_datos:
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["direction"],ruta["origin"], ruta["destination"]]
            #print(ruta_actual)
            if ruta_actual not in rutas_contadas:
                #FCORREMOS EL VALOR FIJADO PARA COMPARARLO Y REALIZAR EL CONTEO
                for ruta_bd in lista_datos:
                    if ruta_actual == [ruta_bd["direction"],ruta_bd["origin"], ruta_bd["destination"]]:
                        contador += 1
                        dinero = dinero+float(ruta_bd["total_value"])
                        medio_actual=ruta_bd["transport_mode"]
                        if medio_actual not in medio:
                          medio.append(medio_actual)
                          
                #AÑADIMOS LAS RUTAS CONTADAS Y REINICIAMOS EL CONTADOR. SE EXTRAE LA INFORMACION DE
                #ORIGEN, DESTINO, CUANTOS MOVIMIENTOS TIENE, CUANDO DINERO PRODUCE Y QUE MEDIOS DE
                #TRANSPORTE USAN
                rutas_contadas.append(ruta_actual)
                rutas_conteo.append([ruta["origin"], ruta["destination"],contador,dinero,medio])
                contador = 0
                dinero = 0
                
                medio=[]
                
                                               
    rutas_conteo.sort(reverse=True, key = lambda x:x[2])
    
    return rutas_conteo


#USAMOS LA FUNCION rutas_exportacion_importacion PARA CREAR LAS LISTAS 

conteo_exportaciones = rutas_exportacion_importacion("Exports")
conteo_importaciones = rutas_exportacion_importacion("Imports")

#LA FUNCION ordenar_dinero ORDENA LAS RUTAS POR CANTIDAD MONETARIA QUE APORTAN
def ordenar_dinero(export_import):
    conteo_ord=[]
    for e_i in export_import:
      conteo_ord.append(e_i)
      conteo_ord.sort(reverse=True, key = lambda x:x[3])
    return conteo_ord

conteo_exportaciones2 = ordenar_dinero(conteo_exportaciones)
conteo_importaciones2 = ordenar_dinero(conteo_importaciones)

print("\nLas 10 rutas de exportacion con más demanda son:\n[origen,destino,movimientos,dinero,[medios de transporte]")
for k in conteo_exportaciones[:10]:
  print(k)

print("\nLas 10 rutas de exportaciones que generan más dinero son:\n[origen,destino,movimientos,dinero,[medios de transporte]]")
for k in conteo_exportaciones2[:10]:
  print(k)

print("\nLas 10 rutas de importacion de mayor demanda son:\n[origen,destino,movimientos,dinero,[medios de transporte]]")
for k in conteo_importaciones[:10]:
  print(k)

print("\nLas 10 rutas de importación que generan más dinero son:\n[origen,destino,movimientos,dinero,[medios de transporte]")
for k in conteo_importaciones2[:10]:
  print(k)


#####OPCION 2 -> medios  más importantes

##### EXTRAEMOS QUE TANTO SE REPITE UNA RUTA Y QUE TANTO DINERO APORTA
##### DE MANERA ANALOGA A LA FUNCION rutas_exportacion_importacion
def transporte (direccion):
    contador = 0
    dinero=0
    medio_contadas = []
    medio_conteo = []
     
    for medio in lista_datos:
        if medio["direction"] == direccion:
            medio_actual = [medio["direction"],medio["transport_mode"]]
            #print(ruta_actual)
            if medio_actual not in medio_contadas:
                for medio_bd in lista_datos:
                    if medio_actual == [medio_bd["direction"],medio_bd["transport_mode"]]:
                        contador += 1
                        dinero = dinero+float(medio_bd["total_value"])

                
                medio_contadas.append(medio_actual)
                medio_conteo.append([medio["transport_mode"],contador,dinero])
                contador = 0
                dinero = 0
                                               
    medio_conteo.sort(reverse=True, key = lambda x:x[2])
    
    return medio_conteo
###EVALUO LA FUNCION PARA OBTENER LOS CONTEOS PARA EXPORTACIONES E IMPORTACIONES
transporte_exp=transporte("Exports")
transporte_imp=transporte("Imports")
#############IMPRIMIMOS RESULTADOS
print("\nRutas que generan más dinero en la exportación")
print("[Medio de Transporte, Movimientos, Dinero]")
for k in transporte_exp:
  print(k)

print("\nRutas que generan más dinero en la importación")
print("[Medio de Transporte, Movimientos, Dinero]")
for k in transporte_imp:
  print(k)


# Opcion 3 --> Paises que generan el 80%
####LA FUNCION valor_movimiento EXTRAE CUANTO DINERO APORTA CADA PAIS ORIGEN
####USA COMO ARGUMENTO SI ES EXPORTACION O IMPORTACION
def valor_movimiento(direccion):
	contados = []
	valores_paises = []

	for viaje in lista_datos:
		actual = [direccion, viaje["origin"]] #["Exports", "Mexico"]
		valor = 0
		operaciones = 0

		if actual  in contados:
			continue

		for movimiento in lista_datos:
			if actual == [movimiento["direction"], movimiento["origin"]]:
				valor += int(movimiento["total_value"])
				operaciones += 1
		
		contados.append(actual)
		valores_paises.append([direccion, viaje["origin"], valor, operaciones])
	
	valores_paises.sort(reverse = True, key = lambda x:x[2])
	return valores_paises


####AÑADO EL PAIS ORIGEN CON LA CANTIDAD QUE APORTAN A DOS LISTAS
val_exp = valor_movimiento("Exports")
val_imp = valor_movimiento("Imports")

#####OBTENGO EL TOTAL QUE APORTAN LOS PAISES
def total_ing (paises):
  total=0
  for pais in paises:
    total=total+pais[2]
  return(total)

total_exp = total_ing(val_exp)
total_imp = total_ing(val_imp)

#####OBTENGO EL OCHENTA PORCIENTO
def ochentaporciento (total):
  ochenta_pc=(80*total)/100
  return ochenta_pc

ochenta_imp=ochentaporciento(total_imp)
ochenta_exp=ochentaporciento(total_exp)

#####AÑADO A LAS LISTAS val_exp, val_imp, QUE PORCENTAJE APORTAN Y ADEMAS EL PORCENTAJE CUMULADO
def razon(paises,total,porcentaje):
  ingresos_pp=0
  contador=0
  for pais in paises:
    ingresos_pp=float(ingresos_pp)+float(pais[2])
    porcentaje_acumulado=round((ingresos_pp*100)/total,3)
    cociente=round((pais[2]*100)/total,3)
    pais.append("Porcentaje que aporta: "+str(cociente)+"%")
    pais.append("Porcentaje acumulado: "+str(porcentaje_acumulado)+"%")
    contador+=1
  

razon(val_imp,total_imp,ochenta_imp)
razon(val_exp,total_exp,ochenta_exp)

######IMPRIMO RESULTADOS
print("\nPaíses que exportan y los ingresos que generan:")
print("[Tipo de movimiento, País, Dinero, Movimientos]")
for k in val_exp:
  print(k)
print("Cantidad total de ingresos que generan las exportaciones son:$",total_exp)


print("\nPaíses que importan y los ingresos que generan: ")
print("[Tipo de movimiento, País, Dinero, Movimientos]")
for k in val_imp:
  print(k)
print("Cantidad total de ingresos que generan las importaciones son:$",total_imp) 


  







#for pais in paises_80:
#	print(pais)







   