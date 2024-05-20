from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import numpy as np
import math


# inicjowanie zmiennych globalnych
type_function = ""
poly_degree = 0
created_widgets = []
entry_list = []
value_x_min = 0
value_x_max = 0
coefficients = [0, 0, 0, 0, 0, 0, 0, 0]
second_coefficients = []


# konfiguracja root
root = Tk()
root.title("Program do funkcji")
root.geometry("1350x750")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# konfiguracja font
btn_font = font.Font(size=12, weight="bold", family="Arial")
input_font = font.Font(size=12, family="Arial")
input_font_2 = font.Font(size=13, family="Arial")
input_font_3 = font.Font(size=13, family="Arial")


# funckja do znikania frameów
def hide_frame(frame):
    frame.pack_forget()
    frame_plot_range.place_forget()

# funkcja do usuwania widgetów z frame_caluclations


def destroy_widgets():
    global created_widgets
    for widget in created_widgets:
        widget.destroy()

def hide_all_frame():
    if frame_poly_input.winfo_ismapped():
        frame_poly_input.pack_forget()
    elif frame_linear_input.winfo_ismapped():
        frame_linear_input.pack_forget()
    elif frame_square_input.winfo_ismapped():
        frame_square_input.pack_forget()
    elif frame_trig_input.winfo_ismapped():
        frame_trig_input.pack_forget()

# funkcja do pokazywania framów i zamykania wcześniejszych (dla funkcji liniowej i kwadratowej)
def show_frame(frame):
    frame_linear_input.pack_forget()
    frame_square_input.pack_forget()
    frame_poly_degree_input.pack_forget()
    frame_poly_input.pack_forget()
    frame_trig_input.pack_forget()
    hide_frame(frame_plot_range)
    frame.pack()
    remove_plot()  # usuwanie wykresu
    destroy_widgets()  # usuwanie informacji dodatkowych



# funkcja do pokazywania pola do wpisania stopnia wielomianu
def show_poly_degree_input():
    hide_all_frame()
    frame_poly_degree_input.pack()
    remove_plot()  # przy każdym kliknięciu na przyciski główne usuwany jest wykres
    destroy_widgets()  # i obliczenia

# funkcja do obliczania pola pod wykresem dla funkcji liniowej


def area_under_plot(value_a, value_b):
    area_under_plot_label = tk.Label(
        frame_calculations, text="Pole pod wykresem", font=input_font_2, width=100, anchor="w", justify="left", fg="#000080")
    created_widgets.append(area_under_plot_label)
    # obliczenie całki z funkcji liniowej i podłożenie za x x_max i odjęcie x_min
    area = value_a*value_x_max**2/2+value_b*value_x_max - \
        value_a*value_x_min**2/2-value_b*value_x_min
    area_under_plot_output = tk.Label(
        frame_calculations, width=100, anchor="w", justify="left", text=f"Pole pod wykresem w przedziale ({value_x_min}, {value_x_max}) wynosi {area} ", font=input_font_2)
    created_widgets.append(area_under_plot_output)
    area_under_plot_label.grid(row=10, column=0)

    area_under_plot_output.grid(row=11, column=0, padx=(50,0))


# funkcja przetwarzająca x_min i x_max, przedział do obliczania pola pod wykresem dla funkcji liniowej
def value_x_max_min_proccesing(value_x_min_input, value_x_max_input, value_a, value_b):
    global value_x_max
    global value_x_min

    value_x_min = float(value_x_min_input.get())
    value_x_max = float(value_x_max_input.get())

    area_under_plot(value_a, value_b)


# Dodatkowe obliczenia dla funkcji liniowej
def linear_calculations(value_a, value_b):

    global value_x_min
    global value_x_max

    value_a = float(value_a)
    value_b = float(value_b)
    root_label = tk.Label(frame_calculations,
                          text="Miejsca zerowe ", font=input_font_3, width=100, anchor="w", justify="left", fg="#000080")
    root_label.grid(row=0, column=0)
    created_widgets.append(root_label)
    if value_a == 0 and value_b == 0:
        function_root = tk.Label(
            frame_calculations, text="Miejsca zerowe funkcji to zbiór liczb rzeczywistych", font=input_font_2, width=100, anchor="w", justify="left")
    elif value_a == 0:
        function_root = tk.Label(
            frame_calculations, text="Funkcja nie posiada miejsc zerowych", width=100,  font=input_font_2, anchor="w", justify="left")
    else:
        function_root = tk.Label(
            frame_calculations, text=f"Miejsce zerowe funkcji:{(-1*value_b/value_a):.4g}", width=100,  font=input_font_2, anchor="w", justify="left")
    function_root.grid(row=1, column=0, padx=(50, 0))
    created_widgets.append(function_root)

    monocity_label = tk.Label(
        frame_calculations, text="Monotoniczność ", font=input_font_3, width=100, anchor="w", justify="left", fg="#000080")
    monocity_label.grid(row=2, column=0)
    created_widgets.append(monocity_label)
    monotonicity = ""
    if value_a > 0:
        monotonicity = "rosnąca"
    elif value_a < 0:
        monotonicity = "malejąca"
    else:
        monotonicity = "stała"

    monotonicity_label = tk.Label(
        frame_calculations, text=f"Funkcja jest {monotonicity} na całej swojej dziedzinie.", font=input_font_2, width=100, anchor="w", justify="left", fg="#000000")
    monotonicity_label.grid(row=3, column=0, padx=(50, 0))
    created_widgets.append(monotonicity_label)

    more_than_zero_label = tk.Label(frame_calculations,
                                    text="Wartości większe od 0 ", font=input_font_2, width=100, anchor="w", justify="left", fg="#000080")
    more_than_zero_label.grid(row=4, column=0)
    created_widgets.append(more_than_zero_label)
    more_than_zero = ""
    if value_a > 0:
        more_than_zero = tk.Label(
            frame_calculations, text=f"Funkcja przyjmuje podane wartości w przedziale ( {(-1 * value_b / value_a):.4g}4, +niesk).", width=100, anchor="w", justify="left", font=input_font_2)
    elif value_a < 0:
        more_than_zero = tk.Label(
            frame_calculations, text=f"Funkcja przyjmuje podane wartości w przedziale (-niesk, {(-1*value_b/value_a):.4g}).", width=100, anchor="w", justify="left", font=input_font_2)
    elif value_b > 0:
        more_than_zero = tk.Label(
            frame_calculations, text=f"Funkcja przyjmuje podane wartości na całej swojej dziedzinie.", width=100, anchor="w", justify="left", font=input_font_2)
    else:
        more_than_zero = tk.Label(
            frame_calculations, text=f"Funkcja nie przyjmuje wartości większych od zera.", width=100, anchor="w", justify="left", font=input_font_2)
    more_than_zero.grid(row=5, column=0, padx=(50, 0))
    created_widgets.append(more_than_zero)

    frame_calculations.rowconfigure(7, minsize=26)
    frame_calculations.rowconfigure(8, minsize=26)
    frame_calculations.rowconfigure(9, minsize=26)

    value_x_max_min_title = tk.Label(frame_calculations, text="Podaj przedział aby obliczyć pole pod wykresem",
                                     width=100, anchor="w", justify="left", font=input_font_3, fg="#000080")
    value_x_max_min_title.grid(row=6, column=0)
    created_widgets.append(value_x_max_min_title)

    value_x_min_label = tk.Label(
        frame_calculations, text="Podaj x min", font=input_font_2, width=15, anchor="w", justify="left",)
    value_x_max_label = tk.Label(
        frame_calculations, text="Podaj x max", font=input_font_2, width=15, anchor="w", justify="left",)
    value_x_min_input = tk.Entry(
        frame_calculations, width=15)
    value_x_max_input = tk.Entry(
        frame_calculations, width=15)
    value_x_max_min_btn = tk.Button(frame_calculations, text="Potwierdź", width=31, command=lambda: value_x_max_min_proccesing(
        value_x_min_input, value_x_max_input, value_a, value_b))
    value_x_min_label.place(x=52, y=176)
    created_widgets.append(value_x_min_label)
    value_x_min_input.place(x=152, y=178)
    created_widgets.append(value_x_min_input)
    value_x_max_label.place(x=52, y=202)
    created_widgets.append(value_x_max_label)
    value_x_max_input.place(x=152, y=204)
    created_widgets.append(value_x_max_input)
    value_x_max_min_btn.place(x=26, y=228)
    created_widgets.append(value_x_max_min_btn)


#funkcja do zbierania danych i wysyłania do funkcji rysującej wykres i robiącej dodatkowe obliczenia dla funkcji liniowej
def linear_processing():

    global type_function
    type_function = "li"

    global x_range
    global y_range
    x = x_range_input.get()
    y = y_range_input.get()
    x_range = x
    y_range = y
    if x_range == "":
        x_range = 10
    if y_range == "":
        y_range = 10

    value_a = li_input_a.get()
    value_b = li_input_b.get()
    value_c = 0

    if not value_a or not value_b or not (value_a.replace(".", "", 1).isdigit() or value_a.replace("-", "", 1).replace(".", "", 1).isdigit()) or not (value_b.replace(".", "", 1).isdigit() or value_b.replace("-", "", 1).replace(".", "", 1).isdigit()):
        messagebox.showerror("Błąd", "Podana wartość nie jest liczbą.")
        return

    linear_calculations(value_a, value_b)
    generate_li_sq_plot(type_function, value_a, value_b,
                        value_c, x_range, y_range)


# funkcja do obliczania pola pod wykresem dla funkcji kwadratowej
def sq_area_under_plot(value_x_min, value_x_max, value_a, value_b, value_c):
    # obliczenie całki z funkcji kwadratowej i podłożenie za x x_max i odjęcie x_min
    area_under_field_value = (value_a * value_x_max ** 3) / 3 + (value_b * value_x_max ** 2) / 2 + value_c * value_x_max - (value_a * value_x_max ** 3) / 3 - ( value_b * value_x_min ** 2) / 2 - value_c * value_x_min
    area_under_field = f"Pole pod wykresem w przedziale ({value_x_min},{value_x_max}) wynosi {area_under_field_value}"

    area_under_field_label = tk.Label(frame_calculations,
                                      text="Pole pod wykresem ", font=input_font_2, width=100, anchor="w", justify="left", fg="#000080")
    area_under_field_label.grid(row=10, column=0)
    created_widgets.append(area_under_field_label)
    area_under_field_output = tk.Label(
        frame_calculations, text=area_under_field, font=input_font_2, width=100, anchor="w", justify="left",)
    area_under_field_output.grid(row=11, column=0, padx=(50,0))
    created_widgets.append(area_under_field_output)


# funkcja przetwarzająca x_min i x_max, przedział do obliczania pola pod wykresem dla funkcji kwadratowej
def sq_value_x_max_min_proccesing(value_x_min_input, value_x_max_input, value_a, value_b, value_c):
    global value_x_max
    global value_x_min

    value_x_min = float(value_x_min_input.get())
    value_x_max = float(value_x_max_input.get())

    sq_area_under_plot(value_x_min, value_x_max, value_a, value_b, value_c)

# Dodatkowe obliczenia dla funkcji liniowej


def square_calculations(value_a, value_b, value_c):
    value_a = float(value_a)
    value_b = float(value_b)
    value_c = float(value_c)
    delta = value_b**2-(4*value_a*value_c)
    p = -1*value_b/(2*value_a)
    q = -1*delta/(4*value_a)

    function_root = ""
    values_above_zero = ""
    monocity = ""

    if delta > 0:
        delta_root = math.sqrt(delta)
        x1 = (-1*value_b-delta_root)/(2*value_a)
        x2 = (-1*value_b+delta_root)/(2*value_a)
        if x1 > x2:
            x1, x2 = x2, x1
        function_root = f"Funkcja przymuje wartość 0 dla x1 = {x1:.4g}  oraz x2  = {x2:.4g}"
        if value_a > 0:
            values_above_zero = f"Funkcja przyjmuje podane wartości w przedziale (- niesk, {x1:.4g}) oraz ({x2:.4g}, +niesk)"

        elif value_a < 0:
            values_above_zero = f"Funkcja przyjmuje podane wartości w przedziale ({x1:.4g}, {x2:.4g})"
    if delta == 0:
        x0 = p
        function_root = f"Funkcja posiada jedno miejsce zerowe x0 = {x0:.4g}"
        if value_a > 0:
            values_above_zero = "Funkcja przyjmuje podane wartości w przedziale (- niesk, {x0:.4g}) oraz ({x0:.4g}, +niesk)"
        else:
            values_above_zero = "Funkcja nie przyjmuje wartości większych od 0"
    if delta < 0:
        function_root = "Funkcja nie posiada miejsc zerowych."
        if value_a > 0:
            values_above_zero = "Funkcja przyjmuje podane wartości na całej swojej dziedzinie."
        else:
            values_above_zero = "Funkcja nie przyjmuje wartości większych od 0"

    if value_a > 0:
        monocity = f"Funkcja rośnie w przedziale ({p:.4g}, + niesk) i maleje w ( - niesk, {p:.4g})"
    elif value_a < 0:
        monocity = f"Funkcja rośnie w przedziale ( - niesk, {p:.4g}) i maleje w ({p:.4g}, + niesk)"

    root_label = tk.Label(frame_calculations,
                          text="Miejsca zerowe ", font=input_font_3, width=100, anchor="w", justify="left", fg="#000080")
    root_label.grid(row=0, column=0)
    created_widgets.append(root_label)

    function_root = tk.Label(
        frame_calculations, text=function_root, font=input_font_2, width=100, anchor="w", justify="left",)
    function_root.grid(row=1, column=0, padx=(50,0))
    created_widgets.append(function_root)

    more_than_zero_label = tk.Label(frame_calculations,
                                    text="Wartości większe od 0 ", font=input_font_2, width=100, anchor="w", justify="left", fg="#000080")
    more_than_zero_label.grid(row=2, column=0)
    created_widgets.append(more_than_zero_label)

    more_than_zero = tk.Label(
        frame_calculations, text=values_above_zero, font=input_font_2, width=100, anchor="w", justify="left",)
    more_than_zero.grid(row=3, column=0, padx=(50,0))
    created_widgets.append(more_than_zero)

    monocity_label = tk.Label(frame_calculations,
                              text="Monotoniczność ", font=input_font_2, width=100, anchor="w", justify="left", fg="#000080")
    monocity_label.grid(row=4, column=0)
    created_widgets.append(monocity_label)

    monocity_output = tk.Label(
        frame_calculations, text=monocity, font=input_font_2, width=100, anchor="w", justify="left",)
    monocity_output.grid(row=5, column=0, padx=(50,0))
    created_widgets.append(monocity_output)

    value_x_max_min_title = tk.Label(frame_calculations, text="Podaj przedział aby obliczyć pole pod wykresem",
                                     width=100, anchor="w", justify="left", font=input_font_3, fg="#000080")
    value_x_max_min_title.grid(row=6, column=0)
    created_widgets.append(value_x_max_min_title)

    frame_calculations.rowconfigure(7, minsize=26)
    frame_calculations.rowconfigure(8, minsize=26)
    frame_calculations.rowconfigure(9, minsize=26)

    value_x_min_label = tk.Label(
        frame_calculations, text="Podaj x min", font=input_font_2, width=15, anchor="w", justify="left",)
    value_x_max_label = tk.Label(
        frame_calculations, text="Podaj x max", font=input_font_2, width=15, anchor="w", justify="left",)
    value_x_min_input = tk.Entry(
        frame_calculations, width=15)
    value_x_max_input = tk.Entry(
        frame_calculations, width=15)
    value_x_max_min_btn = tk.Button(frame_calculations, text="Potwierdź", width=27, command=lambda: sq_value_x_max_min_proccesing(
        value_x_min_input, value_x_max_input, value_a, value_b, value_c))
    value_x_min_label.place(x=52, y=176)
    created_widgets.append(value_x_min_label)
    value_x_min_input.place(x=152, y=178)
    created_widgets.append(value_x_min_input)
    value_x_max_label.place(x=52, y=202)
    created_widgets.append(value_x_max_label)
    value_x_max_input.place(x=152, y=204)
    created_widgets.append(value_x_max_input)
    value_x_max_min_btn.place(x=26, y=228)
    created_widgets.append(value_x_max_min_btn)


# funkcja do zbierania danych i wysyłania do funkcji rysującej wykres i robiącej dodatkowe obliczenia dla funkcji kwadratowej
def square_processing():

    global type_function
    type_function = "sq"

    global x_range
    global y_range
    x = x_range_input.get()
    y = y_range_input.get()
    x_range = x
    y_range = y
    if x_range == "":
        x_range = 10
    if y_range == "":
        y_range = 10

    value_a = sq_input_a.get()
    value_b = sq_input_b.get()
    value_c = sq_input_c.get()

    if not value_a or not (value_a.replace(".", "", 1).isdigit() or value_a.replace("-", "", 1).replace(".", "", 1).isdigit()) or value_a.isspace():
        messagebox.showerror("Błąd", "Podana wartość a nie jest liczbą.")
        return
    elif float(value_a) == 0:
        messagebox.showerror(
            "Błąd", "Współczynnik a musi być różny od zera.")
        return

    if not value_b or not (value_b.replace(".", "", 1).isdigit() or value_b.replace("-", "", 1).replace(".", "", 1).isdigit()) or value_b.isspace():
        messagebox.showerror("Błąd", "Podana wartość b nie jest liczbą.")
        return

    if not value_c or not (value_c.replace(".", "", 1).isdigit() or value_c.replace("-", "", 1).replace(".", "", 1).isdigit()) or value_c.isspace():
        messagebox.showerror("Błąd", "Podana wartość c nie jest liczbą.")
        return

    generate_li_sq_plot(type_function, value_a, value_b,
                        value_c, x_range, y_range)
    square_calculations(value_a, value_b, value_c)


# funkcja do ponownego zebrania danych potrzebnych do narysowania wykresu w przypadku zmiany zakresu wykresu dla wszystkich rodzajów funkcji
def values_processing(type_function, x_range, y_range):
    if type_function == "li":
        value_a = li_input_a.get()
        value_b = li_input_b.get()
        value_c = 0
        generate_li_sq_plot(type_function, value_a, value_b,
                            value_c, x_range, y_range)
    elif type_function == "sq":
        value_a = sq_input_a.get()
        value_b = sq_input_b.get()
        value_c = sq_input_c.get()
        generate_li_sq_plot(type_function, value_a, value_b,
                            value_c, x_range, y_range)
    elif type_function == "po":
        global poly_degree
        po_values_processing(poly_degree, x_range, y_range)


def po_value_x_max_min_proccesing(value_x_min_input, value_x_max_input, coefficients):
    global value_x_max
    global value_x_min

    value_x_min = float(value_x_min_input.get())
    value_x_max = float(value_x_max_input.get())
    x_max = value_x_max
    x_min = value_x_min
    
    area_under_plot = coefficients[0] * x_max ** 8 / 8 + coefficients[1] * x_max ** 7 / 7 + coefficients[2] * x_max ** 6 / 6 + coefficients[3] * x_max ** 5 / 5 + coefficients[4] * x_max ** 4 / 4 + coefficients[5] * x_max ** 3 / 3 + coefficients[6] * x_max ** 2 / 2 + coefficients[7] * \
        x_max - (coefficients[0] * x_min ** 8 / 8 + coefficients[1] * x_min ** 7 / 7 + coefficients[2] * x_min ** 6 / 6 + coefficients[3] * x_min **
                 5 / 5 + coefficients[4] * x_min ** 4 / 4 + coefficients[5] * x_min ** 3 / 3 + coefficients[6] * x_min ** 2 / 2 + coefficients[7] * x_min)
    
    
    area_under_plot_label = tk.Label(
        frame_calculations, text=f"Pole pod wykresem dla wielomianu w przedziale ({value_x_min}; {value_x_max}) = {area_under_plot}", font=input_font_2, width=100, anchor="w", justify="left", fg="#000080")
    area_under_plot_label.grid(row=6, column=0, pady=50)
    created_widgets.append(area_under_plot_label)


# Funkcja do obliczania miejsc zerowych dla wielomianów
def calculate_zeros(second_coefficients, coefficients):
    zeros = np.roots(second_coefficients)
    real_zeros = [zero for zero in zeros if np.isreal(zero)]
    rounded_zeros = [round(zero.real, 2) for zero in real_zeros]
    x_max = 1
    x_min = -1
    po_calculations(x_max, x_min, rounded_zeros, coefficients)


# Dodatkowe obliczenia dla wielomianów
def po_calculations(x_max, x_min, rounded_zeros, coefficients):
  

    root_label = tk.Label(frame_calculations,
                          text="Miejsca zerowe ", font=input_font_3, width=100, anchor="w", justify="left", fg="#000080")
    root_label.grid(row=0, column=0)
    created_widgets.append(root_label)

    function_root = tk.Label(
        frame_calculations, text=f"Miejsca zerowe wielomianu to: {rounded_zeros}", font=input_font_2, width=100, anchor="w", justify="left")
    function_root.grid(row=1, column=0, padx=(50,0))
    created_widgets.append(function_root)


    frame_calculations.rowconfigure(3, minsize=26)
    frame_calculations.rowconfigure(4, minsize=26)
    frame_calculations.rowconfigure(5, minsize=26)
    frame_calculations.rowconfigure(6, minsize=26)

    value_x_max_min_title = tk.Label(frame_calculations, text="Podaj przedział aby obliczyć pole pod wykresem",
                                     width=100, anchor="w", justify="left", font=input_font_3, fg="#000080")
    value_x_max_min_title.grid(row=2, column=0)
    created_widgets.append(value_x_max_min_title)

    value_x_min_label = tk.Label(
        frame_calculations, text="Podaj x min", font=input_font_2, width=15, anchor="w", justify="left")
    value_x_min_input = tk.Entry( frame_calculations, width=10)
    value_x_min_label.place(x=52, y=74)
    value_x_min_input.place(x=152, y=76)
    created_widgets.append(value_x_min_label)
    created_widgets.append(value_x_min_input)
    
    value_x_max_label = tk.Label(
        frame_calculations, text="Podaj x max", font=input_font_2, width=15, anchor="w", justify="left")
    value_x_max_input = tk.Entry( frame_calculations, width=10)
    value_x_max_label.place(x=52, y=100)
    value_x_max_input.place(x=152, y=102)
    created_widgets.append(value_x_max_label)
    created_widgets.append(value_x_max_input)
    value_x_max_min_btn = tk.Button(frame_calculations, text="Potwierdź", width=23, command=lambda: po_value_x_max_min_proccesing(value_x_min_input, value_x_max_input, coefficients))
    value_x_max_min_btn.place(x=26, y=128)
    created_widgets.append(value_x_max_min_btn)
    


# funkcja do zbierania danych i wysyłania do funkcji rysującej wykres i robiącej dodatkowe obliczenia dla wielomianów

def po_values_processing(poly_degree, x_range, y_range):
    global type_function
    global coefficients
    type_function = "po"

    if x_range == "":
        x_range = 10
    if y_range == "":
        y_range = 10
    x_range = int(x_range)
    y_range = int(y_range)
    global coefficient

    second_coefficients = []

    for i in range(poly_degree):
        entry_value = entry_list[i].get()
        if not entry_value or not (entry_value.replace(".", "", 1).isdigit() or entry_value.replace("-", "", 1).replace(".", "", 1).isdigit()):
            messagebox.showerror(
                "Błąd", "Jedna z wartości nie jest liczbą lub jest pusta.")
            return
        coefficient = float(entry_value)
        second_coefficients.append(coefficient)

    # Sprawdzenie długości współczynników
    if len(second_coefficients) < poly_degree:
        messagebox.showerror(
            "Błąd", "Nie wprowadzono wszystkich współczynników.")
        return

    # Zamiana miejsc współczynników
    coefficients = second_coefficients[::-1] + [0] * (8 - poly_degree)
    coefficients.reverse()
    

    calculate_zeros(second_coefficients, coefficients)
    generate_polynomial_plot(coefficients, x_range, y_range)



# Zmienianie zakresu wykresu
def change_range_plot(type_function):
    global x_range
    global y_range
    x = float(x_range_input.get())
    y = float(y_range_input.get())

    x_range = x
    y_range = y
    values_processing(type_function, x_range, y_range)


# funkcja generująca odpowiednią ilość pól do wprowadzania dla wielomianów
def poly_input_generator():
    for widget in frame_poly_input.winfo_children():
        widget.destroy()
    frame_poly_input.pack()
    global poly_degree
    poly_degree = int(po_input_a.get()) + 1

    if poly_degree < 4 or poly_degree > 8:
        messagebox.showerror(
            "Błąd", "Podaj poprawny zakres stopnia wielomianu (3-7)")
        return

    hide_frame(frame_poly_degree_input)
    row = 0
    column = 0
    global entry_list
    entry_list = []

    for i in range(poly_degree):
        label = tk.Label(
            frame_poly_input, text=f"Podaj a{poly_degree-i-1}: ", width=15, height=1, font=input_font)
        entry = tk.Entry(frame_poly_input, width=10)
        entry.config(font=("Arial", 12))
        label.grid(row=row, column=column*2, padx=2, pady=10)
        entry.grid(row=row, column=column*2+1, padx=2, pady=10)
        column += 1
        if column == 3:
            row += 1
            column = 0
        if i+1 == poly_degree:
            po_input_submit_btn = tk.Button(
                frame_poly_input, text="Potwierdź", command=lambda: po_values_processing(poly_degree, 10, 10))
            po_input_submit_btn.grid(row=row, column=column+2)

        entry_list.append(entry)  # Dodanie entry do listy entry_list

def tri_calculations(tri_type):
    print(tri_type)
    generate_trigonometric_plot(tri_type)

# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z miejscem na podstawowe przyciski
# frame button
frame_btn = tk.Frame(root)
frame_btn.pack()

btn_linear = tk.Button(frame_btn, text="Funkcja Liniowa", width=18, height=2, padx=1, bg="#C3D6DB",
                       activebackground="#B2C5CA", font=btn_font, command=lambda: show_frame(frame_linear_input))
btn_linear.grid(row=0, column=0, padx=50, pady=35)

btn_square = tk.Button(frame_btn, text="Funkcja Kwadratowa", width=18, height=2, padx=1, bg="#C3D6DB",
                       activebackground="#B2C5CA", font=btn_font, command=lambda: show_frame(frame_square_input))
btn_square.grid(row=0, column=1, padx=50)

btn_polynomial = tk.Button(frame_btn, text="Wielomiany", width=18, height=2, padx=1,
                           bg="#C3D6DB",  activebackground="#B2C5CA", font=btn_font, command=show_poly_degree_input)
btn_polynomial.grid(row=0, column=2, padx=50)

btn_trigonometry = tk.Button(frame_btn, text="F. trygonometryczne", width=18, height=2, padx=1,
                           bg="#C3D6DB",  activebackground="#B2C5CA", font=btn_font, command=lambda: show_frame(frame_trig_input))
btn_trigonometry.grid(row=0, column=3, padx=50)

# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z miejscem na wprowadzanie współrzędnych funkcji liniowej
# frame linear input
frame_linear_input = tk.Frame(root)
frame_linear_input.pack()

frame_linear_input.columnconfigure(2, minsize=100)
frame_linear_input.columnconfigure(5, minsize=100)

# definiowanie
li_function_pattern_label = tk.Label(
    frame_linear_input, text="Wzór funkcji y = ax + b", width=20, height=1, font=input_font)

li_input_a_label = tk.Label(
    frame_linear_input, text="Podaj a: ", width=15, height=1, font=input_font)
li_input_a = tk.Entry(frame_linear_input, width=10)
li_input_a.config(font=("Arial", 12))
li_input_b_label = tk.Label(
    frame_linear_input, text="Podaj b: ", width=15, height=1, font=input_font)
li_input_b = tk.Entry(frame_linear_input, width=10)
li_input_b.config(font=("Arial", 12))

li_submit_btn = tk.Button(
    frame_linear_input, text="Potwierdź", command=linear_processing)


# pozycjonowanie
li_function_pattern_label.place(x=300, y=0)

li_input_a_label.grid(row=1, column=0, padx=2, pady=50)
li_input_a.grid(row=1, column=1, padx=2, pady=10)

li_input_b_label.grid(row=1, column=3, padx=2, pady=10)
li_input_b.grid(row=1, column=4, padx=2, pady=10)

li_submit_btn.grid(row=1, column=6, padx=2, pady=10)


# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z miejscem na wprowadzanie współrzędnych funkcji kwadratowej
# frame square input
frame_square_input = tk.Frame(root)
frame_square_input.pack()

frame_square_input.columnconfigure(2, minsize=40)
frame_square_input.columnconfigure(5, minsize=40)
frame_square_input.columnconfigure(8, minsize=40)

# definiowanie
sq_function_pattern_label = tk.Label(
    frame_square_input, text="Wzór funkcji y = ax^2 + bx + c", width=25, height=1, font=input_font)

sq_input_a_label = tk.Label(
    frame_square_input, text="Podaj a: ", width=15, height=1, font=input_font)
sq_input_a = tk.Entry(frame_square_input, width=10)
sq_input_a.config(font=("Arial", 12))
sq_input_b_label = tk.Label(
    frame_square_input, text="Podaj b: ", width=15, height=1, font=input_font)
sq_input_b = tk.Entry(frame_square_input, width=10)
sq_input_b.config(font=("Arial", 12))
sq_input_c_label = tk.Label(
    frame_square_input, text="Podaj c: ", width=15, height=1, font=input_font)
sq_input_c = tk.Entry(frame_square_input, width=10)
sq_input_c.config(font=("Arial", 12))

sq_submit_btn = tk.Button(
    frame_square_input, text="Potwierdź", command=square_processing)

# pozycjonowanie
sq_function_pattern_label.place(x=360, y=0)

sq_input_a_label.grid(row=1, column=0, padx=2, pady=50)
sq_input_a.grid(row=1, column=1, padx=2, pady=10)

sq_input_b_label.grid(row=1, column=3, padx=2, pady=10)
sq_input_b.grid(row=1, column=4, padx=2, pady=10)

sq_input_c_label.grid(row=1, column=6, padx=2, pady=10)
sq_input_c.grid(row=1, column=7, padx=2, pady=10)

sq_submit_btn.grid(row=1, column=9, padx=2, pady=10)


# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z miejscem na wprowadzanie współrzędnych stopnia wielomianu
# frame poly input
frame_poly_degree_input = tk.Frame(root)
frame_poly_degree_input.pack()

# definiowanie
po_function_pattern_label = tk.Label(
    frame_poly_degree_input, text="Wzór funkcji W(x) =a_n x^n +a_{n-1} x^{n-1} +...+ a_1 x +a_0", width=46, height=1, font=input_font)

po_input_a_label = tk.Label(
    frame_poly_degree_input, text="Podaj stopień wielomianu: ", width=25, height=1, font=input_font_2)
po_input_a = tk.Entry(frame_poly_degree_input, width=10)
po_submit_btn = tk.Button(frame_poly_degree_input,
                          text="Potwierdź", command=poly_input_generator)

# pozycjonowanie
po_function_pattern_label.place(x=0, y=0)

po_input_a_label.grid(row=1, column=0, padx=10, pady=50)
po_input_a.grid(row=1, column=1, padx=10, pady=10)
po_submit_btn.grid(row=1, column=2, padx=10, pady=10)

# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z miejscem na wprowadzanie pól do wpisywania kolejnych współrzędnych wielomianu (inputy dodawane za pomocą funkcji)
frame_poly_input = tk.Frame(root)
frame_poly_input.pack()

# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a dla funkcji trygonometrycznych

frame_trig_input = tk.Frame(root)
frame_trig_input.pack()


btn_trig_sinus = tk.Button(frame_trig_input, text="Sinus", width=12, height=2, padx=1, bg="#d9d5b8",
                       activebackground="#c4c1a5", font=btn_font, command=lambda: tri_calculations("sinus"))
btn_trig_sinus.grid(row=0, column=0, padx=30, pady=20)
btn_trig_cosinus = tk.Button(frame_trig_input, text="Cosinus", width=12, height=2, padx=1, bg="#d9d5b8",
                       activebackground="#c4c1a5", font=btn_font, command=lambda: tri_calculations("cosinus") )
btn_trig_cosinus.grid(row=0, column=1, padx=30, pady=20)
btn_trig_tanges = tk.Button(frame_trig_input, text="Tanges", width=12, height=2, padx=1, bg="#d9d5b8",
                       activebackground="#c4c1a5", font=btn_font, command=lambda: tri_calculations("tanges") )
btn_trig_tanges.grid(row=0, column=2, padx=30, pady=20)
btn_trig_cotanges = tk.Button(frame_trig_input, text="Cotanges", width=12, height=2, padx=1, bg="#d9d5b8",
                       activebackground="#c4c1a5", font=btn_font, command=lambda: tri_calculations("cotanges") )
btn_trig_cotanges.grid(row=0, column=3, padx=30, pady=20)
#command=lambda: show_frame(generate_sinus_plot)
# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z miejscem na wprowadzanie zakresu (x,y) wykresu
frame_plot_range = tk.Frame(root)
frame_plot_range.place(x=88, y=670)

frame_plot_range.columnconfigure(0, minsize=40)
frame_plot_range.columnconfigure(3, minsize=40)
frame_plot_range.columnconfigure(6, minsize=40)

# definiowanie
info_label = tk.Label(
    frame_plot_range, text="Podaj zakres x i y aby przeskalować wykres", font=input_font_2)

x_range_label = tk.Label(
    frame_plot_range, text="Podaj zakres x", font=input_font)
y_range_label = tk.Label(
    frame_plot_range, text="Podaj zakres y", font=input_font)

x_range_input = tk.Entry(frame_plot_range, width=10)
y_range_input = tk.Entry(frame_plot_range, width=10)

plot_range_btn = tk.Button(frame_plot_range, text="Potwierdź",
                           command=lambda: change_range_plot(type_function))

# pozycjonowanie
info_label.grid(row=0, column=1, columnspan=4, pady=5)

x_range_label.grid(row=1, column=0, padx=10)
x_range_input.grid(row=1, column=1)

y_range_label.grid(row=1, column=3)
y_range_input.grid(row=1, column=4, padx=10)

plot_range_btn.grid(row=1, column=5)
# ----------------------------------------------------------------------------------------------------------------------------------------------
# dodawanie frame'a z obliczeniami

frame_calculations = tk.Frame(root, width=300, height=400)
frame_calculations.place(x=620, y=260)


# ----------------------------------------------------------------------------------------------------------------------------------------------
# Funkcje do rysowania wykresów
canvas = None

# funkcja rysująca wykres


def draw_plot(canvas, title=None):
    canvas.get_tk_widget().place(x=88, y=260)
    frame_plot_range.place(x=88, y=670)
    if title:
        plot = canvas.figure.gca()  # Pobierz aktualny subplot z figury
        plot.set_title(title)  # Ustaw tytuł wykresu na podany tytuł




# funkcja usuwająca wykres


def remove_plot():
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None

# funkcja generująca wykres funkcji liniowej lub kwadratowej


def generate_li_sq_plot(type_function, a, b, c, x_range, y_range):

    x_range = float(x_range)
    y_range = float(y_range)
    global canvas
    if a == "":
        a = 0
    if b == "":
        b = 0
    if c == "":
        c = 0
    if x_range > y_range:
        x = np.linspace(-1*x_range, x_range, 100)
    else:
        x = np.linspace(-1*y_range, y_range, 100)

    if type_function == "li":
        y = float(a) * x + float(b)
    elif type_function == "sq":
        y = float(a) * x**2 + float(b) * x + float(c)

    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(111)
    plot.plot(x, y)

    plot.set_xlim(-1*x_range, x_range)
    plot.set_ylim(-1*y_range, y_range)

    plot.axhline(0, color='black', linewidth=0.5)
    plot.axvline(0, color='black', linewidth=0.5)

    if canvas:
        remove_plot()  # Usunięcie poprzedniego wykresu

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    draw_plot(canvas)


# funkcja generująca wykres wielomianu
def generate_polynomial_plot(coefficients, x_range, y_range):

    if x_range > y_range:
        x = np.linspace(-1*x_range, x_range, 100)
    else:
        x = np.linspace(-1*y_range, y_range, 100)
    y = np.polyval(coefficients, x)

    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(111)
    plot.plot(x, y)

    plot.set_xlim(-1*x_range, x_range)
    plot.set_ylim(-1*y_range, y_range)

    plot.axhline(0, color='black', linewidth=0.5)
    plot.axvline(0, color='black', linewidth=0.5)
    global canvas
    if canvas:
        remove_plot()  # Usunięcie poprzedniego wykresu

    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    draw_plot(canvas)

#sinus    

def generate_trigonometric_plot(trig_function):
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    if trig_function == "sinus":
        y = np.sin(x)
        title = "Wykres funkcji sinus"
    elif trig_function == "cosinus":
        y = np.cos(x)
        title = "Wykres funkcji cosinus"
    elif trig_function == "tanges":
        y = np.tan(x)
        title = "Wykres funkcji tangens"
    elif trig_function == "cotanges":
        y = 1 / np.tan(x)
        title = "Wykres funkcji cotangens"
    # Dodaj inne rodzaje funkcji trygonometrycznych, jeśli są potrzebne

    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(111)
    plot.plot(x, y)

    # Ustawianie etykiet na osiach x jako wielokrotności wartości pi
    x_ticks = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
    x_labels = [r'$-2\pi$', r'$-\frac{3\pi}{2}$', r'$-\pi$', r'$-\frac{\pi}{2}$', '0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    plot.set_xticks(x_ticks)
    plot.set_xticklabels(x_labels)

    plot.set_xlim(-2*np.pi, 2*np.pi)
    plot.set_ylim(-2, 2)  # Zakładamy ograniczenie dla y w celu uniknięcia nieskończoności dla funkcji tangens

    plot.axhline(0, color='black', linewidth=0.5)
    plot.axvline(0, color='black', linewidth=0.5)

    global canvas
    if canvas:
        remove_plot()

    canvas = FigureCanvasTkAgg(figure, master=root)  # 'root' to Twoje okno tkintera
    canvas.draw()
    draw_plot(canvas, title=title) 


# ukrywanie frame'ów po rozpoczęciu programu
hide_frame(frame_linear_input)
hide_frame(frame_square_input)
hide_frame(frame_poly_degree_input)
hide_frame(frame_poly_input)
hide_frame(frame_trig_input)
frame_plot_range.place_forget()


# Główna pętla
root.mainloop()