# animation_utils.py
# Módulo de utilidades para animaciones en aplicaciones CustomTkinter

import math
import tkinter as tk
from typing import Dict, Any, Callable, Union, Optional


def ease_in_out_quad(t: float) -> float:
    """
    Función de easing que acelera al principio y desacelera al final.
    
    Args:
        t: Valor de progreso entre 0.0 y 1.0
        
    Returns:
        Valor suavizado entre 0.0 y 1.0
    """
    return 2 * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 2) / 2


def ease_out_cubic(t: float) -> float:
    """
    Función de easing que desacelera al final.
    
    Args:
        t: Valor de progreso entre 0.0 y 1.0
        
    Returns:
        Valor suavizado entre 0.0 y 1.0
    """
    return 1 - math.pow(1 - t, 3)


def ease_in_cubic(t: float) -> float:
    """
    Función de easing que acelera al principio.
    
    Args:
        t: Valor de progreso entre 0.0 y 1.0
        
    Returns:
        Valor suavizado entre 0.0 y 1.0
    """
    return t * t * t


def ease_bounce(t: float) -> float:
    """
    Función de easing con efecto rebote al final.
    
    Args:
        t: Valor de progreso entre 0.0 y 1.0
        
    Returns:
        Valor suavizado entre 0.0 y 1.0
    """
    n1 = 7.5625
    d1 = 2.75
    
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def animar_widget(
    widget: Any,
    inicio: Dict[str, Any],
    fin: Dict[str, Any],
    duracion: int = 500,
    easing: Callable[[float], float] = ease_in_out_quad,
    master: Optional[Any] = None,
    al_completar: Optional[Callable[[], None]] = None
) -> None:
    """
    Animación general para cualquier widget.
    
    Args:
        widget: Widget a animar
        inicio: Diccionario con valores iniciales (relx, rely, etc.)
        fin: Diccionario con valores finales
        duracion: Duración de la animación en milisegundos
        easing: Función de suavizado a utilizar
        master: Widget maestro para el método after (opcional)
        al_completar: Función a ejecutar al completar la animación
    """
    if master is None:
        master = widget
        
    # Posicionar widget al inicio
    widget.place(**inicio)
    
    tiempo_paso = 16  # ~60fps
    pasos_totales = duracion // tiempo_paso
    paso_actual = 0
    
    def interpolar(valor_inicial, valor_final, progreso):
        """Interpola entre dos valores según el progreso"""
        return valor_inicial + (valor_final - valor_inicial) * progreso
    
    def actualizar_animacion():
        nonlocal paso_actual
        if paso_actual <= pasos_totales:
            # Calcular progreso normalizado (0.0 a 1.0)
            progreso = paso_actual / pasos_totales
            progreso_suavizado = easing(progreso)
            
            # Calcular y actualizar propiedades
            propiedades_actuales = {}
            
            # Interpolar cada propiedad numérica
            for prop in inicio:
                if prop in fin and isinstance(inicio[prop], (int, float)) and isinstance(fin[prop], (int, float)):
                    propiedades_actuales[prop] = interpolar(inicio[prop], fin[prop], progreso_suavizado)
                else:
                    # Copiar propiedades no numéricas
                    propiedades_actuales[prop] = inicio[prop]
            
            # Actualizar posición del widget
            widget.place_configure(**propiedades_actuales)
            
            # Programar siguiente frame
            paso_actual += 1
            master.after(tiempo_paso, actualizar_animacion)
        else:
            # Finalizar animación
            widget.place(**fin)
            
            # Ejecutar callback si existe
            if al_completar:
                al_completar()
    
    # Iniciar la animación
    actualizar_animacion()


def animar_transicion(
    frame_saliente: Any,
    frame_entrante: Any,
    saliente_inicio: Dict[str, Any],
    saliente_fin: Dict[str, Any],
    entrante_inicio: Dict[str, Any],
    entrante_fin: Dict[str, Any],
    duracion: int = 800,
    easing: Callable[[float], float] = ease_in_out_quad,
    master: Optional[Any] = None,
    al_completar: Optional[Callable[[], None]] = None
) -> None:
    """
    Realiza una animación de transición entre dos frames.
    
    Args:
        frame_saliente: Frame que sale de la vista
        frame_entrante: Frame que entra a la vista
        saliente_inicio: Diccionario con posición inicial del frame saliente
        saliente_fin: Diccionario con posición final del frame saliente
        entrante_inicio: Diccionario con posición inicial del frame entrante
        entrante_fin: Diccionario con posición final del frame entrante
        duracion: Duración de la animación en milisegundos
        easing: Función de suavizado a utilizar
        master: Widget maestro para el método after (opcional)
        al_completar: Función a ejecutar al completar la animación
    """
    if master is None:
        master = frame_saliente.master or frame_entrante.master
        
    # Posicionar frames al inicio
    frame_saliente.place(**saliente_inicio)
    frame_entrante.place(**entrante_inicio)
    
    tiempo_paso = 16  # ~60fps
    pasos_totales = duracion // tiempo_paso
    paso_actual = 0
    
    def interpolar(valor_inicial, valor_final, progreso):
        """Interpola entre dos valores según el progreso"""
        return valor_inicial + (valor_final - valor_inicial) * progreso
    
    def actualizar_animacion():
        nonlocal paso_actual
        if paso_actual <= pasos_totales:
            # Calcular progreso normalizado (0.0 a 1.0)
            progreso = paso_actual / pasos_totales
            progreso_suavizado = easing(progreso)
            
            # Calcular posiciones actuales para cada frame
            pos_saliente, pos_entrante = {}, {}
            
            # Interpolar propiedades numéricas
            for prop in ['relx', 'rely', 'x', 'y']:
                if prop in saliente_inicio and prop in saliente_fin:
                    pos_saliente[prop] = interpolar(
                        saliente_inicio[prop], saliente_fin[prop], progreso_suavizado)
                
                if prop in entrante_inicio and prop in entrante_fin:
                    pos_entrante[prop] = interpolar(
                        entrante_inicio[prop], entrante_fin[prop], progreso_suavizado)
            
            # Copiar propiedades no numéricas
            for prop in ['anchor']:
                if prop in saliente_inicio:
                    pos_saliente[prop] = saliente_inicio[prop]
                if prop in entrante_inicio:
                    pos_entrante[prop] = entrante_inicio[prop]
            
            # Actualizar posiciones
            frame_saliente.place_configure(**pos_saliente)
            frame_entrante.place_configure(**pos_entrante)
            
            # Programar siguiente frame
            paso_actual += 1
            master.after(tiempo_paso, actualizar_animacion)
        else:
            # Finalizar animación
            frame_saliente.place_forget()
            frame_entrante.place(**entrante_fin)
            
            # Ejecutar callback si existe
            if al_completar:
                al_completar()
    
    # Iniciar la animación
    actualizar_animacion()


def deslizar_horizontal(
    widget: Any,
    desde_x: Union[float, int],
    hasta_x: Union[float, int],
    es_relativo: bool = True,
    duracion: int = 500,
    easing: Callable[[float], float] = ease_in_out_quad,
    master: Optional[Any] = None,
    al_completar: Optional[Callable[[], None]] = None
) -> None:
    """
    Desliza un widget horizontalmente.
    
    Args:
        widget: Widget a animar
        desde_x: Posición inicial X
        hasta_x: Posición final X
        es_relativo: True para usar relx, False para usar x
        duracion: Duración en milisegundos
        easing: Función de suavizado
        master: Widget maestro (opcional)
        al_completar: Función a ejecutar al completar
    """
    prop = 'relx' if es_relativo else 'x'
    
    inicio = {prop: desde_x}
    fin = {prop: hasta_x}
    
    # Copiar propiedades de posición actuales
    for p in ['rely', 'y', 'anchor']:
        try:
            valor = widget.place_info()[p]
            if valor:
                # Convertir a tipo adecuado si es necesario
                if p in ['rely', 'y']:
                    try:
                        valor = float(valor)
                    except ValueError:
                        pass
                inicio[p] = valor
                fin[p] = valor
        except (KeyError, AttributeError):
            pass
    
    animar_widget(widget, inicio, fin, duracion, easing, master, al_completar)


def deslizar_vertical(
    widget: Any,
    desde_y: Union[float, int],
    hasta_y: Union[float, int],
    es_relativo: bool = True,
    duracion: int = 500,
    easing: Callable[[float], float] = ease_in_out_quad,
    master: Optional[Any] = None,
    al_completar: Optional[Callable[[], None]] = None
) -> None:
    """
    Desliza un widget verticalmente.
    
    Args:
        widget: Widget a animar
        desde_y: Posición inicial Y
        hasta_y: Posición final Y
        es_relativo: True para usar rely, False para usar y
        duracion: Duración en milisegundos
        easing: Función de suavizado
        master: Widget maestro (opcional)
        al_completar: Función a ejecutar al completar
    """
    prop = 'rely' if es_relativo else 'y'
    
    inicio = {prop: desde_y}
    fin = {prop: hasta_y}
    
    # Copiar propiedades de posición actuales
    for p in ['relx', 'x', 'anchor']:
        try:
            valor = widget.place_info()[p]
            if valor:
                # Convertir a tipo adecuado si es necesario
                if p in ['relx', 'x']:
                    try:
                        valor = float(valor)
                    except ValueError:
                        pass
                inicio[p] = valor
                fin[p] = valor
        except (KeyError, AttributeError):
            pass
    
    animar_widget(widget, inicio, fin, duracion, easing, master, al_completar)


def transicion_deslizante(
    frame_saliente: Any,
    frame_entrante: Any,
    direccion: str = "izquierda",
    duracion: int = 800,
    easing: Callable[[float], float] = ease_in_out_quad,
    master: Optional[Any] = None,
    al_completar: Optional[Callable[[], None]] = None
) -> None:
    """
    Realiza una transición deslizante entre dos frames.
    
    Args:
        frame_saliente: Frame que sale
        frame_entrante: Frame que entra
        direccion: Dirección de la transición: "izquierda", "derecha", "arriba", "abajo"
        duracion: Duración en milisegundos
        easing: Función de suavizado
        master: Widget maestro (opcional)
        al_completar: Función a ejecutar al completar
    """
    if master is None:
        master = frame_saliente.master or frame_entrante.master
    
    # Configurar posiciones según dirección
    if direccion == "izquierda":
        # El actual sale por la izquierda, el nuevo entra desde la derecha
        animar_transicion(
            frame_saliente=frame_saliente,
            frame_entrante=frame_entrante,
            saliente_inicio={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            saliente_fin={'relx': -0.5, 'rely': 0.5, 'anchor': "center"},
            entrante_inicio={'relx': 1.5, 'rely': 0.5, 'anchor': "center"},
            entrante_fin={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            duracion=duracion,
            easing=easing,
            master=master,
            al_completar=al_completar
        )
    elif direccion == "derecha":
        # El actual sale por la derecha, el nuevo entra desde la izquierda
        animar_transicion(
            frame_saliente=frame_saliente,
            frame_entrante=frame_entrante,
            saliente_inicio={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            saliente_fin={'relx': 1.5, 'rely': 0.5, 'anchor': "center"},
            entrante_inicio={'relx': -0.5, 'rely': 0.5, 'anchor': "center"},
            entrante_fin={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            duracion=duracion,
            easing=easing,
            master=master,
            al_completar=al_completar
        )
    elif direccion == "arriba":
        # El actual sale por arriba, el nuevo entra desde abajo
        animar_transicion(
            frame_saliente=frame_saliente,
            frame_entrante=frame_entrante,
            saliente_inicio={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            saliente_fin={'relx': 0.5, 'rely': -0.5, 'anchor': "center"},
            entrante_inicio={'relx': 0.5, 'rely': 1.5, 'anchor': "center"},
            entrante_fin={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            duracion=duracion,
            easing=easing,
            master=master,
            al_completar=al_completar
        )
    elif direccion == "abajo":
        # El actual sale por abajo, el nuevo entra desde arriba
        animar_transicion(
            frame_saliente=frame_saliente,
            frame_entrante=frame_entrante,
            saliente_inicio={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            saliente_fin={'relx': 0.5, 'rely': 1.5, 'anchor': "center"},
            entrante_inicio={'relx': 0.5, 'rely': -0.5, 'anchor': "center"},
            entrante_fin={'relx': 0.5, 'rely': 0.5, 'anchor': "center"},
            duracion=duracion,
            easing=easing,
            master=master,
            al_completar=al_completar
        )
    else:
        raise ValueError(f"Dirección desconocida: {direccion}")
