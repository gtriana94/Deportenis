import sys
import time
import sqlite3
import pandas as pd
import re



def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break

def opciones_yn():
    print('[S]i')
    print('[N]o')

def run():
    opciones_yn()

    command = input()
    command = command[0:1]
    command = command.upper()

    if command == 'S':
        input_options()
    elif command == 'N':
         sys.exit
    else:
        print('Comando inválido')
        run()
        time.sleep(10)

def iniciar():
    conn = sqlite3.connect("db_distributors_dp.db")
    c = conn.cursor()
    
    c.execute(""" 
        create table if not exists distributors(
            id_distribuidor integer primary key AUTOINCREMENT,
            nombre text not null,
            fecha_registro datetime default current_timestamp,
            fecha_ultima_modificacion datetime default current_timestamp
        );
    """)

    c.execute("""
        create table if not exists persons(
            id_distribuidor integer primary_key,
            nombres text not null,
            apellido_paterno not null,
            apellido_materno
        );
    """)

    c.execute("""
        create table if not exists addresses(
            id_distribuidor integer primary_key,
            calle text not null,
            numero_casa integer not null,
            colonia text not_null,
            codigo_postal integer not null
        );
    """)

    c.execute("""
        create table if not exists phone_numbers(
            id_distribuidor integer primary_key,
            telefono integer not null
        );
    """)

    print("Se inicio con exito")

    conn.close()

def opciones():
    print('Selecciona una opción:')
    print('[V]er de distribuidores')
    print('[A]gregar distribuidor')
    print('[M]odificar distribuidor')
    print('[E]liminar distribuidor')
    print('[B]uscar distribuidor')
    print('[S]ALIR')

def input_options():
    opciones()

    command = input()
    command = command.upper()

    if command == 'V':
        view_distributors()
    elif command == 'A':
        add_distributor()
    elif command == 'M':
        update_distributor()
    elif command == 'E':
        delete_distributor()
    elif command == 'B':
        serch_distributor()
        pass
    elif command == 'S':
        sys.exit
    else:
        print('Comando inválido')
        input_options()
        time.sleep(15)

def view_distributors():
    conn = sqlite3.connect("db_distributors_dp.db")
    c = conn.cursor()

    c.execute("""
        select
            d.id_distribuidor
        ,   d.nombre nombre_distribuidor
        ,   p.nombres nombre_titular
        ,   p.apellido_paterno
        ,   p.apellido_materno
        ,   pn.telefono
        ,   a.calle
        ,   a.numero_casa
        ,   a.colonia
        ,   a.codigo_postal
        ,   d.fecha_registro
        ,   d.fecha_ultima_modificacion
        from
            distributors d
        left join
            persons p
        on
            p.id_distribuidor = d.id_distribuidor
        left join
            addresses a
        on
            a.id_distribuidor = d.id_distribuidor
        left join
            phone_numbers pn
        on
            pn.id_distribuidor = d.id_distribuidor
    """)
    distributors = c.fetchall()

    if(len(distributors) < 1):
        print("Sin distribuidores que mostrar.")
    else:
        print(pd.DataFrame(distributors, columns =['id', 'nombre_distribuidor', 'nombre_titular', 'apellido_paterno', 'apellido_materno', 
        'telefono', 'calle', 'numero_casa', 'colonia', 'codigo_postal', 'fecha_registro', 'fecha_ultima_modificacion']))
    
    conn.close()
    print("¿Desea realizar otra operación?")
    run()

def add_distributor():
    conn = sqlite3.connect("db_distributors_dp.db")
    c = conn.cursor()

## Solicitar datos

    nombre_distribuidor = text_clean(input("Ingrese nombre comercial: "))

    nombres_persona = text_clean(input("Ingrese nombre de la persona: "))

    apellido_paterno = text_clean(input("Ingrese apellido paterno: "))

    apellido_materno = text_clean(input("Ingrese apellido materno: "))

    telefono = inputNumber("Ingrese telefono: ")

    calle = text_clean(input("Calle: "))

    numero_casa = inputNumber("Número: ")

    colonia = text_clean(input("Colonia: "))

    codigo_postal = inputNumber("Código postal: ")

## Consultar id correspondiente al registro
    c.execute("select max(id_distribuidor) from distributors;")
    ultimo_id = c.fetchone()

    if (ultimo_id[0] is None):
        id_distribuidor = 1
    else:
        id_distribuidor = int(ultimo_id[0]) + 1
    
## Insertar registros
    insert_distributors = (nombre_distribuidor)

    c.execute("insert into distributors (nombre) values(?)", [insert_distributors])
    conn.commit()

    c.execute("insert into persons (id_distribuidor, nombres, apellido_paterno, apellido_materno) values(?, ?, ?, ?)", (id_distribuidor, nombres_persona, apellido_paterno, apellido_materno))
    conn.commit()

    c.execute("insert into addresses (id_distribuidor, calle, numero_casa, colonia, codigo_postal) values(?, ?, ?, ?, ?)", (id_distribuidor, calle, numero_casa, colonia, codigo_postal))
    conn.commit()

    c.execute("insert into phone_numbers (id_distribuidor, telefono) values(?, ?)", (id_distribuidor, telefono))
    conn.commit()

    print("Registro exitoso")
    conn.close()
    print("¿Desea realizar otra operación?")
    run()

def update_distributor():
    conn = sqlite3.connect("db_distributors_dp.db")
    c = conn.cursor()

##  Solicitar datos

    id_distribuidor = input("Ingrese id distribuidor a modificar: ")

    nombre_distribuidor = text_clean(input("Ingrese nombre comercial: "))

    nombres_persona = text_clean(input("Ingrese nombre de la persona: "))

    apellido_paterno = text_clean(input("Ingrese apellido paterno: "))

    apellido_materno = text_clean(input("Ingrese apellido materno: "))

    telefono = inputNumber("Ingrese telefono: ")

    calle = text_clean(input("Calle: "))

    numero_casa = inputNumber("Número: ")

    colonia = text_clean(input("Colonia: "))

    codigo_postal = inputNumber("Código postal: ")

## Insertar registros

    c.execute("update distributors set nombre = ?, fecha_ultima_modificacion = CURRENT_TIMESTAMP where id_distribuidor = ?;", (nombre_distribuidor, id_distribuidor))
    conn.commit()

    c.execute("update persons set nombres = ?, apellido_paterno = ?, apellido_materno = ? where id_distribuidor = ?;", (nombres_persona, apellido_paterno, apellido_materno, id_distribuidor))
    conn.commit()

    c.execute("update addresses set calle = ?, numero_casa = ?, colonia = ?, codigo_postal = ? where id_distribuidor = ?;", (calle, numero_casa, colonia, codigo_postal, id_distribuidor))
    conn.commit()

    c.execute("update phone_numbers set telefono = ? where id_distribuidor = ?;", (telefono, id_distribuidor))
    conn.commit()

    print("Actualización exitosa")
    conn.close()
    print("¿Desea realizar otra operación?")
    run()

def delete_distributor():
    conn = sqlite3.connect("db_distributors_dp.db")
    c = conn.cursor()

    id_distribuidor = input("Ingrese id distribuidor a eliminar: ")

    c.execute("delete from distributors where id_distribuidor = ?;", (id_distribuidor))
    conn.commit()

    print("Eliminación exitosa")
    conn.close()
    print("¿Desea realizar otra operación?")
    run()

def serch_distributor():
    conn = sqlite3.connect("db_distributors_dp.db")
    c = conn.cursor()

    ## Metodo de busqueda

    print("Seleccionar metodo de busqueda: ")
    print('[1] Nombre (puede escribir solo una parte del nombre)')
    print('[2] Fecha de registro')
    print('[3] Rango de fechas')
    print('[4] Mes de registro')
    print('[0] Salir')

    command = input()

    if command == '1':
        pass
        nombre = text_clean(input("Nombre comercial: ")).upper()
        nombre = '%'+nombre+'%'
        c.execute("""
                select
                    d.id_distribuidor
                ,   d.nombre nombre_distribuidor
                ,   p.nombres nombre_titular
                ,   p.apellido_paterno
                ,   p.apellido_materno
                ,   pn.telefono
                ,   a.calle
                ,   a.numero_casa
                ,   a.colonia
                ,   a.codigo_postal
                ,   d.fecha_registro
                ,   d.fecha_ultima_modificacion
                from
                    distributors d
                left join
                    persons p
                on
                    p.id_distribuidor = d.id_distribuidor
                left join
                    addresses a
                on
                    a.id_distribuidor = d.id_distribuidor
                left join
                    phone_numbers pn
                on
                    pn.id_distribuidor = d.id_distribuidor
                where
                    d.nombre like ?
            """, [nombre])
        distributors_filter = c.fetchall()
    
    elif command == '2':
        fecha_registro = input("Fecha de registro (aaaa-mm-dd): ")
        c.execute("""
                select
                    d.id_distribuidor
                ,   d.nombre nombre_distribuidor
                ,   p.nombres nombre_titular
                ,   p.apellido_paterno
                ,   p.apellido_materno
                ,   pn.telefono
                ,   a.calle
                ,   a.numero_casa
                ,   a.colonia
                ,   a.codigo_postal
                ,   d.fecha_registro
                ,   d.fecha_ultima_modificacion
                from
                    distributors d
                left join
                    persons p
                on
                    p.id_distribuidor = d.id_distribuidor
                left join
                    addresses a
                on
                    a.id_distribuidor = d.id_distribuidor
                left join
                    phone_numbers pn
                on
                    pn.id_distribuidor = d.id_distribuidor
                where
                    date(d.fecha_registro) = ?
            """, [fecha_registro])
        distributors_filter = c.fetchall()

    elif command == '3':
        fecha_inicio = input("Fecha de inicial (aaaa-mm-dd): ")
        fecha_final = input("Fecha de final (aaaa-mm-dd): ")
        c.execute("""
                select
                    d.id_distribuidor
                ,   d.nombre nombre_distribuidor
                ,   p.nombres nombre_titular
                ,   p.apellido_paterno
                ,   p.apellido_materno
                ,   pn.telefono
                ,   a.calle
                ,   a.numero_casa
                ,   a.colonia
                ,   a.codigo_postal
                ,   d.fecha_registro
                ,   d.fecha_ultima_modificacion
                from
                    distributors d
                left join
                    persons p
                on
                    p.id_distribuidor = d.id_distribuidor
                left join
                    addresses a
                on
                    a.id_distribuidor = d.id_distribuidor
                left join
                    phone_numbers pn
                on
                    pn.id_distribuidor = d.id_distribuidor
                where
                    date(d.fecha_registro) between ? and ?
            """, (fecha_inicio, fecha_final))
        distributors_filter = c.fetchall()

    elif command == '4':
        mes_registro = int(input("Numero del mes de registro: "))
        if len(str(mes_registro)) == 1:
            mes_registro = '0' + str(mes_registro)
        else:
            str(mes_registro)
        c.execute("""
                select
                    d.id_distribuidor
                ,   d.nombre nombre_distribuidor
                ,   p.nombres nombre_titular
                ,   p.apellido_paterno
                ,   p.apellido_materno
                ,   pn.telefono
                ,   a.calle
                ,   a.numero_casa
                ,   a.colonia
                ,   a.codigo_postal
                ,   d.fecha_registro
                ,   d.fecha_ultima_modificacion
                from
                    distributors d
                left join
                    persons p
                on
                    p.id_distribuidor = d.id_distribuidor
                left join
                    addresses a
                on
                    a.id_distribuidor = d.id_distribuidor
                left join
                    phone_numbers pn
                on
                    pn.id_distribuidor = d.id_distribuidor
                where
                    strftime('%m', date(d.fecha_registro)) = ?
            """, [mes_registro])
        distributors_filter = c.fetchall()

    elif command == '0':
        sys.exit
    else:
        print('Comando inválido')
        serch_distributor()
        time.sleep(15)
    conn.close()

    df = pd.DataFrame(distributors_filter, columns=['id_distribuidor', 'nombre_distribuidor', 'nombre_titular', 'apellido_paterno', 'apellido_materno',
    'telefono', 'calle', 'numero_casa', 'colonia', 'codigo_postal', 'fecha_registro', 'fecha_ultima_modificacion'])

    visualizer(df)


def text_clean(x):
    
    text = str(x)

    to_remove = {"1": "i", "3": "e", "4": "a", "5": "s", "7" : "t", "8" : "b", "0" : "o"}

    for char in to_remove.keys():
        text = text.replace(char, to_remove[char])

    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    to_remove_specific = {"CALLE" : " ", "AVENIDA" : " ", "COLONIA" : " "}

    for char in to_remove_specific.keys():
        text = text.upper().replace(char, to_remove_specific[char])
    
    return text

def visualizer(x):

    for i in x.index:
        ## Nombre
        print('Nombre: %s %s %s' %(x['nombre_titular'].iloc[i], x['apellido_paterno'].iloc[i], x['apellido_materno'].iloc[i]))
        ## Ubicación
        print('Calle: %s, #%s, Colonia: %s, CP: %s' %(x['calle'].iloc[i], x['numero_casa'].iloc[i], x['colonia'].iloc[i], x['codigo_postal'].iloc[i]))
        ## Telefono
        print('Telefono: %s' %(x['telefono'].iloc[i]))
        ## Datos de actualización
        if x['fecha_registro'].iloc[i] != x['fecha_ultima_modificacion'].iloc[i]:
            print('El registro fue modificado el dia: %s' %(x['fecha_ultima_modificacion'].iloc[i]))

    print("¿Desea realizar otra operación?")
    run()