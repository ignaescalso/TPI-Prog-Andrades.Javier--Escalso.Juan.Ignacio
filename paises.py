import csv
import os

# CONSTANTES

ARCHIVO_CSV = "paises.csv"

# Encabezados del archivo CSV
ENCABEZADOS = ["nombre", "poblacion", "superficie", "continente"]

# FUNCIONES DE ARCHIVO CSV

def cargar_paises(archivo):
    """
    Lee el archivo CSV y retorna una lista de diccionarios.
    Cada diccionario representa un país con sus datos.

    Parámetros:
        archivo (str): ruta/nombre del archivo CSV.

    Retorna:
        list: lista de diccionarios con los datos de cada país.
              Retorna lista vacía si el archivo no existe.

    Manejo de errores:
        - FileNotFoundError: si el archivo no existe, retorna lista vacía.
        - ValueError: si un campo numérico no puede convertirse.
        - Exception: cualquier otro error inesperado de lectura.
    """
    paises = []

    if not os.path.exists(archivo):
        # Si el archivo no existe aún, se comienza con lista vacía
        return paises

    try:
        with open(archivo, mode="r", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            for numero_fila, fila in enumerate(lector, start=2):
                # Verificar que la fila tenga todos los campos requeridos
                if not all(campo in fila for campo in ENCABEZADOS):
                    print(f"AVISO: Fila {numero_fila} ignorada: faltan columnas.")
                    continue

                # Verificar que ningún campo esté vacío
                if not all(fila[campo].strip() for campo in ENCABEZADOS):
                    print(f"AVISO: Fila {numero_fila} ignorada: campos vacíos.")
                    continue

                try:
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion":  int(fila["poblacion"].strip()),
                        "superficie": int(fila["superficie"].strip()),
                        "continente": fila["continente"].strip()
                    }
                    paises.append(pais)

                except ValueError:
                    print(f"AVISO: Fila {numero_fila} ignorada: "
                          "población/superficie deben ser números enteros.")

    except PermissionError:
        print(f"ERROR: Sin permiso para leer '{archivo}'.")
    except Exception as e:
        print(f" ERROR INESPERADO AL LEER EL ARCHIVO CSV: {e}")

    return paises


def guardar_paises(paises, archivo):
    """
    Guarda la lista de países en el archivo CSV, sobreescribiéndolo.

    Parámetros:
        paises (list): lista de diccionarios con datos de países.
        archivo (str): ruta/nombre del archivo CSV de destino.

    Manejo de errores:
        - PermissionError: si no hay permisos de escritura.
        - Exception: cualquier otro error inesperado.
    """
    try:
        with open(archivo, mode="w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=ENCABEZADOS)
            escritor.writeheader()
            escritor.writerows(paises)

    except PermissionError:
        print(f"ERROR: Sin permiso para escribir en '{archivo}'.")
    except Exception as e:
        print(f"ERROR INESPERADO AL GUARDAR EL ARCHIVO CSV: {e}")


# FUNCIONES DE VALIDACIÓN

def validar_entero_positivo(texto, nombre_campo):
    """
    Intenta convertir 'texto' a entero positivo.
    Muestra un mensaje de error si no es posible.

    Parámetros:
        texto (str): cadena ingresada por el usuario.
        nombre_campo (str): nombre del campo (para el mensaje de error).

    Retorna:
        int o None: el entero si es válido, None si no lo es.
    """
    try:
        valor = int(texto.strip())
        if valor <= 0:
            print(f"ERROR: '{nombre_campo}' debe ser un número mayor a cero.")
            return None
        return valor
    except ValueError:
        print(f"ERROR: '{nombre_campo}' debe ser un número entero.")
        return None


def nombre_existe(paises, nombre):
    """
    Verifica si ya existe un país con ese nombre exacto (sin distinguir mayúsculas).

    Parámetros:
        paises (list): lista actual de países.
        nombre (str): nombre a buscar.

    Retorna:
        bool: True si el nombre ya está registrado, False si no.
    """
    nombre_lower = nombre.strip().lower()
    return any(p["nombre"].lower() == nombre_lower for p in paises)

# FUNCIONES AUXILIARES DE CLAVE
def obtener_nombre(pais):
    return pais["nombre"]

def obtener_poblacion(pais):
    return pais["poblacion"]

def obtener_superficie(pais):
    return pais["superficie"]

# FUNCIONES CRUD (Alta, Modificación, Búsqueda)

def agregar_pais(paises):
    """
    Solicita al usuario los datos de un nuevo país y lo agrega a la lista.
    No permite campos vacíos ni nombres duplicados.

    Parámetros:
        paises (list): lista de países donde se agregará el nuevo registro.

    Efecto:
        Agrega un diccionario a 'paises' y guarda el CSV si todo es válido.
    """
    print("\n--- Agregar nuevo país ---")

    # El usuario ingresa el nombre del país
    nombre = input("Nombre del país: ").strip()
    # Valida que el nombre no esté vacío
    if not nombre:
        print("ERROR: El nombre no puede estar vacío.")
        return
    #Valida que el país no esté duplicado
    if nombre_existe(paises, nombre):
        print(f"ERROR: Ya existe un país llamado '{nombre}'.")
        return

    # El usuario ingresa la población del país y se validan datos
    poblacion = validar_entero_positivo(input("Población: "), "Población")
    if poblacion is None:
        return

    # Superficie
    superficie = validar_entero_positivo(input("Superficie (km²): "), "Superficie")
    if superficie is None:
        return

    # Continente
    continente = input("Continente: ").strip()
    if not continente:
        print("ERROR: El continente no puede estar vacío.")
        return

    # Crear y agregar el diccionario del país
    nuevo_pais = {
        "nombre":     nombre,
        "poblacion":  poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo_pais)
    guardar_paises(paises, ARCHIVO_CSV)
    print(f"País '{nombre}' agregado correctamente.")


def actualizar_pais(paises):
    """
    Busca un país por nombre exacto y permite actualizar
    su Población y/o Superficie.

    Parámetros:
        paises (list): lista de países donde se buscará y modificará.

    Efecto:
        Modifica los campos del diccionario encontrado y guarda el CSV.
    """
    print("\n--- Actualizar datos de un país ---")
    nombre = input("Nombre exacto del país a actualizar: ").strip()

    if not nombre:
        print("ERROR: Debe ingresar un nombre.")
        return

    # Buscar el país en la lista (ignorando mayúsculas/minúsculas)
    pais_encontrado = None
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            pais_encontrado = p
            break

    if pais_encontrado is None:
        print(f"ERROR: No se encontró ningún país llamado '{nombre}'.")
        return

    print(f"País encontrado: {pais_encontrado['nombre']} | "
          f"Población: {pais_encontrado['poblacion']:,} | "
          f"Superficie: {pais_encontrado['superficie']:,} km²")

    # Actualizar población (Enter para dejar sin cambios)
    nueva_pob = input("Nueva población (Enter para no cambiar): ").strip()
    if nueva_pob:
        valor = validar_entero_positivo(nueva_pob, "Población")
        if valor is None:
            return
        pais_encontrado["poblacion"] = valor

    # Actualizar superficie
    nueva_sup = input("Nueva superficie en km² (Enter para no cambiar): ").strip()
    if nueva_sup:
        valor = validar_entero_positivo(nueva_sup, "Superficie")
        if valor is None:
            return
        pais_encontrado["superficie"] = valor

    guardar_paises(paises, ARCHIVO_CSV)
    print(f"Datos de '{pais_encontrado['nombre']}' actualizados.")


def buscar_pais(paises):
    """
    Busca países cuyo nombre contenga el texto ingresado
    (coincidencia parcial, sin distinguir mayúsculas).

    Parámetros:
        paises (list): lista de países donde se realizará la búsqueda.

    Efecto:
        Imprime en pantalla los países que coincidan con la búsqueda.
    """
    print("\n--- Buscar país por nombre ---")
    termino = input("Ingrese nombre o parte del nombre: ").strip()

    if not termino:
        print("Debe ingresar al menos un carácter para buscar.")
        return

    resultados = [p for p in paises if termino.lower() in p["nombre"].lower()]

    if not resultados:
        print(f"No se encontraron países con '{termino}'.")
    else:
        print(f"\n  Resultados ({len(resultados)} encontrado/s):")
        mostrar_tabla(resultados)

# FUNCIONES DE FILTRADO

def filtrar_por_continente(paises):
    """
    Filtra y muestra los países que pertenecen al continente ingresado.

    Parámetros:
        paises (list): lista completa de países.
    """
    print("\n--- Filtrar por continente ---")
    continente = input("  Continente: ").strip()

    if not continente:
        print("ERROR: Debe ingresar un continente.")
        return

    resultados = [p for p in paises if p["continente"].lower() == continente.lower()]

    if not resultados:
        print(f"No se encontraron países en '{continente}'.")
    else:
        print(f"\n Países en {continente} ({len(resultados)}):")
        mostrar_tabla(resultados)


def filtrar_por_rango_poblacion(paises):
    """
    Filtra y muestra los países cuya población se encuentra
    dentro del rango [min_pob, max_pob] ingresado por el usuario.

    Parámetros:
        paises (list): lista completa de países.
    """
    print("\n--- Filtrar por rango de población ---")

    min_pob = validar_entero_positivo(input("Población mínima: "), "Mínimo")
    if min_pob is None:
        return

    max_pob = validar_entero_positivo(input("Población máxima: "), "Máximo")
    if max_pob is None:
        return

    if min_pob > max_pob:
        print("ERROR: El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if min_pob <= p["poblacion"] <= max_pob]

    if not resultados:
        print(f"No hay países con población entre {min_pob:,} y {max_pob:,}.")
    else:
        print(f"\n  Países con población entre {min_pob:,} y {max_pob:,} ({len(resultados)}):")
        mostrar_tabla(resultados)


def filtrar_por_rango_superficie(paises):
    """
    Filtra y muestra los países cuya superficie se encuentra
    dentro del rango [min_sup, max_sup] ingresado por el usuario.

    Parámetros:
        paises (list): lista completa de países.
    """
    print("\n--- Filtrar por rango de superficie ---")

    min_sup = validar_entero_positivo(input("Superficie mínima (km²): "), "Mínimo")
    if min_sup is None:
        return

    max_sup = validar_entero_positivo(input("Superficie máxima (km²): "), "Máximo")
    if max_sup is None:
        return

    if min_sup > max_sup:
        print("ERROR: El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if min_sup <= p["superficie"] <= max_sup]

    if not resultados:
        print(f"  No hay países con superficie entre {min_sup:,} y {max_sup:,} km².")
    else:
        print(f"\n  Países con superficie entre {min_sup:,} y {max_sup:,} km² ({len(resultados)}):")
        mostrar_tabla(resultados)

# FUNCIONES DE ORDENAMIENTO

def ordenar_paises(paises):
    """
    Ordena y muestra la lista de países según el criterio elegido
    por el usuario: nombre, población o superficie.
    El usuario también elige el orden (ascendente o descendente).

    Parámetros:
        paises (list): lista completa de países.

    Nota:
        Se usa sorted() con key= para no modificar la lista original.
        El parámetro reverse=True invierte el orden (descendente).
    """
    print("\n--- Ordenar países ---")
    print("¿Por qué campo ordenar?")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    opcion = input("Opción: ").strip()

    # Mapeo de opción → clave del diccionario
    campos = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in campos:
        print("  [Error] Opción inválida.")
        return

    clave = campos[opcion]

    print("¿En qué orden?")
    print("1. Ascendente")
    print("2. Descendente")
    orden = input("Opción: ").strip()

    if orden not in ("1", "2"):
        print("ERROR: Opción de orden inválida.")
        return

    invertir = (orden == "2")

    # sorted() retorna una nueva lista ordenada sin modificar 'paises'
    if clave == "nombre":
        paises_ordenados = sorted(paises, key=obtener_nombre, reverse=invertir)
    elif clave == "poblacion":
        paises_ordenados = sorted(paises, key=obtener_poblacion, reverse=invertir)
    else:
        paises_ordenados = sorted(paises, key=obtener_superficie, reverse=invertir)

    direccion = "descendente" if invertir else "ascendente"
    print(f"\n  Países ordenados por '{clave}' ({direccion}):")
    mostrar_tabla(paises_ordenados)

# FUNCIONES DE ESTADÍSTICAS

def mostrar_estadisticas(paises):
    """
    Calcula y muestra las siguientes estadísticas del dataset:
      - País con mayor y menor población.
      - Promedio de población.
      - Promedio de superficie.
      - Cantidad de países por continente.

    Parámetros:
        paises (list): lista completa de países (debe tener al menos 1).

    Nota sobre los cálculos:
        - max() y min() con key= buscan el diccionario con el valor más alto/bajo.
        - sum() / len() calcula el promedio aritmético.
        - Un diccionario auxiliar 'conteo' agrupa los países por continente.
    """
    print("\n--- Estadísticas generales ---")

    if not paises:
        print("  No hay datos suficientes para calcular estadísticas.")
        return

    # País con mayor y menor población
    pais_max_pob = max(paises, key=obtener_poblacion)
    pais_min_pob = min(paises, key=obtener_poblacion)

    print(f"\n  País con MAYOR población: {pais_max_pob['nombre']} "
          f"({pais_max_pob['poblacion']:,} hab.)")
    print(f"  País con MENOR población: {pais_min_pob['nombre']} "
          f"({pais_min_pob['poblacion']:,} hab.)")

    # Promedios
    total_paises = len(paises)
    prom_poblacion = sum(p["poblacion"]  for p in paises) // total_paises
    prom_sup = sum(p["superficie"] for p in paises) // total_paises

    print(f"\n Promedio de población:  {prom_poblacion:,} hab.")
    print(f"Promedio de superficie: {prom_sup:,} km²")

    # Cantidad de países por continente
    # Se recorre la lista y se cuenta usando un diccionario
    conteo = {}
    for p in paises:
        cont = p["continente"]
        if cont in conteo:
            conteo[cont] += 1
        else:
            conteo[cont] = 1

    print(f"\n  Cantidad de países por continente ({total_paises} en total):")
    # Ordenar el conteo por nombre de continente para mejor lectura
    for continente in sorted(conteo):
        print(f"- {continente}: {conteo[continente]}")

# FUNCIÓN DE VISUALIZACIÓN

def mostrar_tabla(paises):
    """
    Imprime una tabla formateada en consola con los datos de una
    lista de países.

    Parámetros:
        paises (list): lista de diccionarios a mostrar.

    Nota:
        Se usan f-strings con ancho fijo (ljust/rjust) para alinear columnas.
        El formato {:,} en enteros agrega separadores de miles.
    """
    if not paises:
        print("(Lista vacía)")
        return

    # Encabezado de la tabla
    sep = "-" * 72
    print(f"\n {sep}")
    print(f"{'NOMBRE':<22} {'POBLACIÓN':>15} {'SUPERFICIE':>15} {'CONTINENTE':<15}")
    print(f"{sep}")

    for p in paises:
        print(f"{p['nombre']:<22} {p['poblacion']:>15,} {p['superficie']:>15,} {p['continente']:<15}")

    print(f"{sep}\n")


def mostrar_todos(paises):
    """
    Muestra todos los países cargados en la lista usando mostrar_tabla().

    Parámetros:
        paises (list): lista completa de países.
    """
    print("\n--- Todos los países ---")
    if not paises:
        print("No hay países cargados.")
    else:
        print(f"Total: {len(paises)} país/es registrado/s.")
        mostrar_tabla(paises)

# MENÚ PRINCIPAL

def mostrar_menu():
    """
    Imprime en pantalla el menú principal con todas las opciones
    disponibles para el usuario.
    """
    print("\n" + "=" * 50)
    print("GESTIÓN DE DATOS DE PAÍSES")
    print("=" * 50)
    print("1. Agregar un país")
    print("2. Actualizar población/superficie de un país")
    print("3. Buscar país por nombre")
    print("4. Filtrar por continente")
    print("5. Filtrar por rango de población")
    print("6. Filtrar por rango de superficie")
    print("7. Ordenar países")
    print("8. Mostrar estadísticas")
    print("9. Mostrar todos los países")
    print("0. Salir")
    print("=" * 50)


def main():
    """
    Función principal del programa.
    Carga el dataset desde el CSV, muestra el menú y despacha
    las opciones elegidas por el usuario en un bucle hasta que
    elija salir (opción 0).
    """
    print("\n  Cargando datos desde CSV...")
    paises = cargar_paises(ARCHIVO_CSV)
    print(f"  {len(paises)} país/es cargado/s.")

    # Diccionario que mapea cada opción a su función correspondiente
    opciones = {
        "1": agregar_pais,
        "2": actualizar_pais,
        "3": buscar_pais,
        "4": filtrar_por_continente,
        "5": filtrar_por_rango_poblacion,
        "6": filtrar_por_rango_superficie,
        "7": ordenar_paises,
        "8": mostrar_estadisticas,
        "9": mostrar_todos,
    }

    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ").strip()

        if opcion == "0":
            print("\n¡Hasta luego!\n")
            break
        elif opcion in opciones:
            # Llamar a la función correspondiente pasando la lista
            opciones[opcion](paises)
        else:
            print("ERROR: Opción inválida. Ingrese un número del 0 al 9.")

# PUNTO DE ENTRADA

if __name__ == "__main__":
    main()
