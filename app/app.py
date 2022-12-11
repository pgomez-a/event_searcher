import tkinter as tk
from tkcalendar import DateEntry

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

def open_menu(window) -> None:
    '''
    Open menu screen when the button is pressed.
    '''
    global menuscreen_image
    menuscreen_image = tk.PhotoImage(file='images/menuscreen.png')
    menuscreen_label = tk.Label(window, image=menuscreen_image)
    menuscreen_label.place(x=0, y=0, relwidth=1, relheight=1)
    free_options = ['Gratuito',
                    'No gratuito']
    free_inside = tk.StringVar(window)
    free_inside.set('GRATUITO')
    free_menu = tk.OptionMenu(window, free_inside, *free_options)
    free_menu.place(relx=0.19, rely=0.13, anchor='center')
    bar_options = ['CHOPERA',
                   'EL SALVADOR',
                   'CORTES',
                   'PALOS DE MOGUER',
                   'LOS JERONIMOS',
                   'RECOLETOS',
                   'UNIVERSIDAD']
    bar_inside = tk.StringVar(window)
    bar_inside.set('BARRIO')
    bar_menu = tk.OptionMenu(window, bar_inside, *bar_options)
    bar_menu.place(relx=0.07, rely=0.31, anchor='center')
    acc_options = ['Accesible',
                   'Sin información sobre accesibilidad para movilidad reducida',
                   'Bucle de inducción magnético']
    acc_inside = tk.StringVar(window)
    acc_inside.set('ACCESIBILIDAD')
    acc_menu = tk.OptionMenu(window, acc_inside, *acc_options)
    acc_menu.place(relx=0.12, rely=0.49, anchor='center')
    date = DateEntry(window, bf='black')
    date.place(relx=0.79, rely=0.21, anchor='center')
    type_options = ['ProgramacionDestacadaAgendaCultura',
                    'CursosTalleres',
                    '-',
                    'JOBO',
                    'TeatroPerformance',
                    'DanzaBaile',
                    'RecitalesPresentacionesActosLiterarios',
                    'ActividadesCalleArteUrbano',
                    'Exposiciones',
                    'ExcursionesItinerariosVisitas',
                    'ConferenciasColoquios']
    type_inside = tk.StringVar(window)
    type_inside.set('TIPO')
    type_menu = tk.OptionMenu(window, type_inside, *type_options)
    type_menu.place(relx=0.93, rely=0.38, anchor='center')
    inst_options = ['Teatro Circo Price',
                    'Fernán Gómez Centro Cultural de la Villa',
                    'Centro de Cultura Contemporánea Conde Duque',
                    'Medialab en Matadero. Matadero Madrid',
                    'Matadero Madrid',
                    'Teatro Español',
                    'Espacio Abierto Quinta de los Molinos',
                    'CentroCentro',
                    'Naves Español en Matadero',
                    'Casa del Lector']
    inst_inside = tk.StringVar(window)
    inst_inside.set('INSTALACIÓN')
    inst_menu = tk.OptionMenu(window, inst_inside, *inst_options)
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
        event_but = tk.Button(window, text='BUSCAR EVENTO', command=lambda: open_menu(window))
        event_but.place(relx=0.5, rely=0.6, anchor='center')
    return

if __name__ == '__main__':
    root = tk.Tk()
    config_root(root, title='ESearcher', width=860, height=500)
    gif, frame_list, last_frame, anim = load_app(root)
    root.after(100, animate_gif(root, 0, 0))
    root.mainloop()
