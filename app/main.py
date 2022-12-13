import rdflib
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import GEO
import pandas as pd
import tkinter as tk
from tkcalendar import DateEntry


def buscador_evento_por_barrio(graph, barrio):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject esearch:barrio ?Barrio. 
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for r in graph.query(q_evento, initBindings = {'?Barrio' : rdflib.Literal(str(barrio))}):
    result_list.append(r.Subject)

  return result_list

def buscador_evento_por_tipo(graph, tipo):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject esearch:tipo ?Tipo. 
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for r in graph.query(q_evento, initBindings = {'?Tipo' : rdflib.Literal(str(tipo))}):
    result_list.append(r.Subject)

  return result_list

def buscador_evento_por_gratuidad(graph, gratuidad):
  '''
  Buscador de evento por gratuidad, el usuario introduce '1'-gratuito o '0'-no gratuito
  '''
  q_evento = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject esearch:gratuito ?Gratuito. 
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for r in graph.query(q_evento, initBindings = {'?Gratuito' : rdflib.Literal(str(gratuidad))}):
    result_list.append(r.Subject)

  return result_list

def buscador_evento_por_instalacion(graph, instalacion):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject ?Nombre
  WHERE { 
    ?Subject esearch:realizadoEn ?Instalacion.
    ?Instalacion esearch:nombre ?Nombre.
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for r in graph.query(q_evento, initBindings = {'?Nombre' : rdflib.Literal(str(instalacion))}):
    result_list.append(r.Subject)

  return result_list

def buscador_evento_por_accesibilidad(graph, accesibilidad):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject esearch:realizadoEn ?Instalacion.
    ?Instalacion esearch:accesibilidad ?Accesibilidad.
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for r in graph.query(q_evento, initBindings = {'?Accesibilidad' : rdflib.Literal(str(list(str(accesibilidad))))}):
    result_list.append(r.Subject)

  return result_list

def buscador_evento_por_fecha_exacta(graph, fecha):
  q_fechas = prepareQuery('''
  SELECT
    ?Subject ?FechaInicio ?FechaFin
  WHERE { 
    ?Subject esearch:fechaInicio ?FechaInicio.
    ?Subject esearch:fechaFin ?FechaFin.
  }
  ''',
  initNs = { "esearch": ESEARCH})

  lista_fechas = []
  for r in rdf_graph.query(q_fechas):
    fecha_inicio = r.FechaInicio.value[:-11]
    fecha_fin = r.FechaFin.value[:-11]
    rango_fecha = pd.date_range(fecha_inicio,fecha_fin, freq='D').strftime('%Y-%m-%d').to_list()
    lista_fechas.append((r.Subject,rango_fecha))

  result_list = []
  for evento in lista_fechas:
    if fecha in evento[1]:
      result_list.append(evento[0])


  return result_list

def obtener_locales_barrio_evento(graph, lista_eventos_resultado):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject ?Locales
  WHERE { 
    ?Subject esearch:localesEnBarrio ?Locales.  
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for ele in lista_eventos_resultado:
    for r in graph.query(q_evento, initBindings = {'?Subject' : ele}):
      result_list.append((r.Subject.n3(), r.Locales))

  return result_list


def obtener_info_evento(graph, results_list):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject ?Titulo ?Precio ?Gratuito ?DiasSemana ?FechaInicio ?FechaFin ?Hora ?Descripcion ?Barrio ?Tipo
  WHERE { 
    ?Subject esearch:titulo ?Titulo. 
    ?Subject esearch:precio ?Precio. 
    ?Subject esearch:gratuito ?Gratuito.
    ?Subject esearch:diasSemana ?DiasSemana.
    ?Subject esearch:fechaInicio ?FechaInicio.
    ?Subject esearch:fechaFin ?FechaFin.
    ?Subject esearch:hora ?Hora.
    ?Subject esearch:descripcion ?Descripcion.
    ?Subject esearch:barrio ?Barrio.
    ?Subject esearch:tipo ?Tipo. 
  }
  ''',
  initNs = { "esearch": ESEARCH})

  result_list = []
  for ele in results_list:
    for r in graph.query(q_evento, initBindings = {'?Subject' : ele}):
      result_list.append((r.Subject.n3(), r.Titulo.value, r.Precio.value, r.Gratuito.value, r.DiasSemana.value, r.FechaInicio.value, r.FechaFin.value, r.Hora.value, r.Descripcion.value, r.Barrio.value, r.Tipo.value))

  return result_list


def obtener_info_locales(graph, results_list):
  q_evento = prepareQuery('''
  SELECT 
    ?Subject ?Direccion ?Rotulo ?Descripcion
  WHERE { 
    ?Subject esearch:dir ?Direccion.
    ?Subject esearch:rotulo ?Rotulo.
    ?Subject esearch:descripcion ?Descripcion.

  }
  ''',
  initNs={"esearch": ESEARCH})

  result_list = []
  for ele in results_list:
    for r in graph.query(q_evento, initBindings={'?Subject': ele[1]}):
      result_list.append((r.Subject.n3(), r.Direccion.value, r.Rotulo.value, r.Descripcion.value))

  return result_list


def obtener_info_instalaciones(graph, results_list):
  q_evento = prepareQuery('''
  SELECT 
    ?Evento ?Subject ?Nombre ?Acc ?Direccion
  WHERE { 
    ?Evento esearch:realizadoEn ?Subject.
    ?Subject esearch:nombre ?Nombre.
    ?Subject esearch:accesibilidad ?Acc.
    ?Subject esearch:dir ?Direccion.

  }
  ''',
  initNs={"esearch": ESEARCH})

  result_list = []
  for ele in results_list:
    for r in graph.query(q_evento, initBindings={'?Evento': ele}):
      result_list.append((r.Evento.n3(), r.Direccion.value, r.Nombre.value, r.Acc.value))

  return result_list


#for acc in lista_accesibilidad:
  #print(buscador_evento_por_accesibilidad(rdf_graph, acc)) #1.6 no funciona


def config_root(window, title:str, width:int, height:int, resizable=True) -> None:
    '''
    Set the configuration for the window title and geometry.
    '''
    window.title(title)
    screen_width = window.winfo_screenwidth()
    screen_height= window.winfo_screenheight()
    center_x = int((screen_width / 2) - (width / 2))
    center_y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{center_x}+{center_y}')
    if resizable:
        window.resizable(False, False)
    global background_image
    background_image = tk.PhotoImage(file='images/background.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    return

def load_app(window):
    '''
    Loading page for the ESearcher App.
    '''
    frame_index = 0
    frame_list = []
    while True:
        try:
            part = f'gif -index {frame_index}'
            frame = tk.PhotoImage(file='images/load.gif', format=part)
        except:
            last_frame = frame_index - 1
            break
        frame_list.append(frame)
        frame_index += 1
    gif = tk.Label(window, bg='#88cffa')
    gif.place(relx=0.5, rely=0.5, anchor='center')
    return gif, frame_list, last_frame, None

def search_event(events, entry, menu) -> None:
    idx = entry.get()
    men = menu.get()
    if men and men != 'OPCIONES' and idx and idx.isdigit() and int(idx) > 0 and int(idx) <= len(events):
        global event_mylist
        global event_frame
        if event_mylist:
            event_mylist.pack_forget()
            event_frame.pack_forget()
        idx = int(idx) - 1
        uri_evento = events[idx][0][1:-1]
        out = obtener_info_instalaciones(rdf_graph, [rdflib.term.URIRef(uri_evento)])
        event_frame = tk.Frame(root, width=48, height=17)
        event_scrollbar = tk.Scrollbar(event_frame, orient='vertical')
        event_mylist = tk.Listbox(event_frame, width=48, height=17, yscrollcommand=event_scrollbar.set)
        event_scrollbar.config(command=event_mylist.yview)
        event_scrollbar.pack(side='right', fill='y')
        event_frame.pack(side='right')
        event_mylist.insert('end', ' *** EVENTO ' + str(idx + 1) + ' ***')
        if men == 'Instalación evento':
            event_mylist.insert('end', ' *** INSTALACIÓN ***')
            event_mylist.insert('end', ' Dirección: ' + out[0][1])
            event_mylist.insert('end', ' Instalación: ' + out[0][2])
            event_mylist.insert('end', ' Accesibilidad: ' + out[0][3])
            event_mylist.insert('end', '')
            event_mylist.pack(side='right')
        elif men == 'Locales cercanos':
            out = obtener_locales_barrio_evento(rdf_graph, [rdflib.term.URIRef(uri_evento)])
            out = obtener_info_locales(rdf_graph, out)
            event_mylist.insert('end', ' *** LOCALES CERCANOS ***')
            for item in out:
                event_mylist.insert('end', ' Dirección: ' + item[1])
                event_mylist.insert('end', ' Descripción: ' + item[2])
                event_mylist.insert('end', ' Nombre local: ' + item[3])
                event_mylist.insert('end', '')
            event_mylist.pack(side='right')
        elif men == 'Transporte':
            pass
    return

def print_event(events):
    if events:
        global eventscreen_image
        eventscreen_image = tk.PhotoImage(file='images/eventscreen.png')
        eventscreen_label = tk.Label(root, image=eventscreen_image)
        eventscreen_label.place(x=0, y=0, relwidth=1, relheight=1)
        global frame
        frame = tk.Frame(root, width=48)
        scrollbar = tk.Scrollbar(frame, orient='vertical')
        global mylist
        mylist = tk.Listbox(frame, width=48, yscrollcommand = scrollbar.set )
        scrollbar.config( command = mylist.yview )
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='left', fill='y')
        mylist.insert('end', ' RESULTADOS DE LA BÚSQUEDA')
        for idx, event in enumerate(events):
            mylist.insert('end', ' *** EVENTO ' + str(idx + 1) + ' ***')
            mylist.insert('end', ' Título: ' + event[1][:45])
            mylist.insert('end', ' Precio: ' + event[2][:45])
            mylist.insert('end', ' Gratuito: ' + event[3][:45])
            mylist.insert('end', ' Dias semana: ' + event[4])
            mylist.insert('end', ' Fecha inicio: ' + event[5])
            mylist.insert('end', ' Fecha fin: ' + event[6])
            mylist.insert('end', ' Hora: ' + event[7])
            mylist.insert('end', ' Descripción: ' + event[8][:45])
            mylist.insert('end', ' Barrio: ' + event[9][:45])
            mylist.insert('end', ' Tipo: ' + event[10][:45])
            mylist.insert('end', '')
            mylist.insert('end', '')
        mylist.pack(side='left', fill='y')
        message = tk.Label(root, text='Evento número (1-'+str(len(events))+'):')
        message.place(relx=0.72, rely=0.05, anchor='center')
        entry = tk.Entry(root, width=3)
        entry.place(relx=0.84, rely=0.05, anchor='center')
        entry_options = ['Instalación evento', 'Locales cercanos', 'Transporte']
        global entry_inside
        entry_inside = tk.StringVar(root)
        entry_inside.set('OPCIONES')
        entry_menu = tk.OptionMenu(root, entry_inside, *entry_options)
        entry_menu.place(relx=0.75, rely=0.10, anchor='center')
        event_but = tk.Button(root, text='BUSCAR EVENTO', command=lambda: search_event(events, entry, entry_inside))
        event_but.place(relx=0.75, rely=0.16, anchor='center')
        menu_but = tk.Button(root, text='VOLVER AL MENÚ PRINCIPAL', command=lambda: open_menu(root))
        menu_but.place(relx=0.75, rely=0.95, anchor='center')
    return

def gratuito_event(event) -> None:
    val = free_inside.get()
    if val == 'Gratuito':
        out = buscador_evento_por_gratuidad(rdf_graph, 1)
    else:
        out = buscador_evento_por_gratuidad(rdf_graph, 0)
    out = obtener_info_evento(rdf_graph, out)
    print_event(out)
    return

def barrio_event(event) -> None:
    val = bar_inside.get()
    out = buscador_evento_por_barrio(rdf_graph, val)
    out = obtener_info_evento(rdf_graph, out)
    print_event(out)
    return

def accesibilidad_event(event) -> None:
    val = acc_inside.get()
    out = buscador_evento_por_accesibilidad(rdf_graph, val)
    out = obtener_info_evento(rdf_graph, out)
    print_event(out)
    return

def tipo_event(event) -> None:
    val = type_inside.get()
    out = buscador_evento_por_tipo(rdf_graph, val)
    out = obtener_info_evento(rdf_graph, out)
    print_event(out)
    return

def instalacion_event(event) -> None:
    val = inst_inside.get()
    out = buscador_evento_por_instalacion(rdf_graph, val)
    out = obtener_info_evento(rdf_graph, out)
    print_event(out)
    return


def fecha_event() -> None:
    val = date.get_date()
    out = buscador_evento_por_fecha_exacta(rdf_graph, str(val))
    out = obtener_info_evento(rdf_graph, out)
    print_event(out)
    return


def open_menu(window) -> None:
    '''
    Open menu screen when the button is pressed.
    '''
    if mylist:
        mylist.pack_forget()
        frame.pack_forget()
    global menuscreen_image
    menuscreen_image = tk.PhotoImage(file='images/menuscreen.png')
    menuscreen_label = tk.Label(window, image=menuscreen_image)
    menuscreen_label.place(x=0, y=0, relwidth=1, relheight=1)
    free_options = ['Gratuito', 'No gratuito']
    global free_inside
    free_inside = tk.StringVar(window)
    free_inside.set('GRATUITO')
    free_menu = tk.OptionMenu(window, free_inside, *free_options, command=gratuito_event)
    free_menu.place(relx=0.19, rely=0.13, anchor='center')
    bar_options = lista_barrios
    global bar_inside
    bar_inside = tk.StringVar(window)
    bar_inside.set('BARRIO')
    bar_menu = tk.OptionMenu(window, bar_inside, *bar_options, command=barrio_event)
    bar_menu.place(relx=0.07, rely=0.31, anchor='center')
    acc_options = lista_accesibilidad
    global acc_inside
    acc_inside = tk.StringVar(window)
    acc_inside.set('ACCESIBILIDAD')
    acc_menu = tk.OptionMenu(window, acc_inside, *acc_options, command=accesibilidad_event)
    acc_menu.place(relx=0.12, rely=0.49, anchor='center')
    global date
    date = DateEntry(window, bf='black')
    date.place(relx=0.79, rely=0.21, anchor='center')
    date_but = tk.Button(window, text='BUSCAR', command=lambda: fecha_event())
    date_but.place(relx=0.89, rely=0.21, anchor='center')
    type_options = lista_tipos
    global type_inside
    type_inside = tk.StringVar(window)
    type_inside.set('TIPO')
    type_menu = tk.OptionMenu(window, type_inside, *type_options, command=tipo_event)
    type_menu.place(relx=0.93, rely=0.38, anchor='center')
    inst_options = lista_instalaciones
    global inst_inside
    inst_inside = tk.StringVar(window)
    inst_inside.set('INSTALACIÓN')
    inst_menu = tk.OptionMenu(window, inst_inside, *inst_options, command=instalacion_event)
    inst_menu.place(relx=0.85, rely=0.56, anchor='center')
    return

def animate_gif(window, count:int, start:int) -> None:
    '''
    Display the gif for the loading page.
    '''
    if start < 50:
        gif.config(image = frame_list[count])
        count +=1
        if count > last_frame:
            count = 0
        anim = window.after(100, lambda :animate_gif(window, count, start+1))
    else:
        global titlescreen_image
        titlescreen_image = tk.PhotoImage(file='images/titlescreen.png')
        titlescreen_label = tk.Label(window, image=titlescreen_image)
        titlescreen_label.place(x=0, y=0, relwidth=1, relheight=1)
        menu_but = tk.Button(window, text='BUSCAR EVENTO', command=lambda: open_menu(window))
        menu_but.place(relx=0.5, rely=0.6, anchor='center')
    return

if __name__ == '__main__':
    rdf_graph = rdflib.Graph()
    rdf_graph.parse('data.txt', format='turtle')

    ESEARCH = rdflib.Namespace('http://www.upm.es/ontology/eventsearcher#')
    GEOF = rdflib.Namespace('http://www.opengis.net/def/function/geosparql/')
    OPGS = rdflib.Namespace('http://www.opengis.net/def/uom/OGC/1.0/')

    lista_barrios = ['CHOPERA', 'EL SALVADOR', 'CORTES', 'PALOS DE MOGUER', 'LOS JERONIMOS', 'RECOLETOS', 'UNIVERSIDAD']
    lista_tipos = ['ProgramacionDestacadaAgendaCultura', 'CursosTalleres', '-', 'JOBO', 'TeatroPerformance', 'DanzaBaile',
            'RecitalesPresentacionesActosLiterarios', 'ActividadesCalleArteUrbano', 'Exposiciones', 'ExcursionesItinerariosVisitas',
            'ConferenciasColoquios']
    lista_instalaciones = ['Teatro Circo Price', 'Fernán Gómez Centro Cultural de la Villa', 'Centro de Cultura Contemporánea Conde Duque',
            'Medialab en Matadero. Matadero Madrid', 'Matadero Madrid', 'Teatro Español', 'Espacio Abierto Quinta de los Molinos', 'CentroCentro',
            'Naves Español en Matadero', 'Casa del Lector']
    lista_accesibilidad = ['1', '3', '1.6']

    global mylist
    mylist = None

    global event_mylist
    event_mylist = None

    root = tk.Tk()
    config_root(root, title='ESearcher', width=860, height=500)
    gif, frame_list, last_frame, anim = load_app(root)
    root.after(100, animate_gif(root, 0, 0))
    root.mainloop()
