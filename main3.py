import flet as ft
import time
import math
from math import sqrt
import flet.canvas as cv
import numpy as np
import matplotlib.pyplot as plt
import base64
import os
from fontTools.misc.bezierTools import calcBounds
from numpy.random.mtrand import triangular
from io import BytesIO
from uuid import uuid4  # Для уникальных имен файлов
from PIL import Image
import random
from tornado.speedups import websocket_mask

plt.switch_backend('agg')


def ShowText(page):
    page.views.append(
        ft.View(
            "/show_text",
            [
                ft.AppBar(title=ft.Text("Show text"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ft.Row(
                    controls=[
                        ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            value=f"Hello world left",
                            size=20,
                            weight=20,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START),
                ft.Row(
                    controls=[
                        ft.Text(
                            value=f"Hello world center",
                            size=20,
                            weight=20,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),

                ft.Row(
                    controls=[
                        ft.Text(
                            value=f"Hello world right",
                            size=20,
                            weight=20,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
            ],
        )
    )


def ShowTable(page):
    page.views.append(
        ft.View(
            "/show_text",
            [
                ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Имя")),
                        ft.DataColumn(ft.Text("Возраст")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("1")),
                                ft.DataCell(ft.Text("Алексей")),
                                ft.DataCell(ft.Text("25")),
                            ],
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("2")),
                                ft.DataCell(ft.Text("Мария")),
                                ft.DataCell(ft.Text("30")),
                            ],
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("3")),
                                ft.DataCell(ft.Text("Иван")),
                                ft.DataCell(ft.Text("28")),
                            ],
                        ),
                    ]
                )
            ]
        )
    )


def DeleteSymbols(page):
    pass


def main(page: ft.Page):
    page.title = "Routes Example"
    content = ft.Column()
    page.add(
        ft.Column(
            [
                content,  # Контейнер для добавляемых элементов
            ],
            spacing=20,
        )
    )

    def route_change(route):
        page.views.clear()
        content.controls.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Show text", on_click=lambda _: page.go("/show_text"), width=500),
                    ft.ElevatedButton("Show table", on_click=lambda _: page.go("/show_table"), width=500),
                    ft.ElevatedButton("Delete symbols", on_click=lambda _: page.go("/delete_symbols"), width=500),
                    ft.ElevatedButton("Find line", on_click=lambda _: page.go("/find_line"), width=500),
                    ft.ElevatedButton("Move revers line", on_click=lambda _: page.go("/move_revers_line"), width=500),
                    ft.ElevatedButton("Draw square", on_click=lambda _: page.go("/draw_square"), width=500),
                    ft.ElevatedButton("Draw triangle in circle", on_click=lambda _: page.go("/draw_triangle_in_circle"),
                                      width=500),
                    ft.ElevatedButton("Draw triangle with circle", on_click = lambda _: page.go("/draw_triangle_with_circle") ,width=500),
                    ft.ElevatedButton("Draw histogram", on_click=lambda _: page.go("/plot_histogram"), width=500),
                    ft.ElevatedButton("Highlight matrix min/max",
                                      on_click=lambda _: page.go("/highlight_matrix_min_max"), width=500),
                    ft.ElevatedButton("Color rows", on_click=lambda _: page.go("/color_rows_by_index"), width=500),
                    ft.ElevatedButton("Color columns", on_click=lambda _: page.go("/color_columns_by_reverse_index"),
                                      width=500),
                    ft.ElevatedButton("Gradient matrix", on_click=lambda _: page.go("/gradient_sort_matrix"),
                                      width=500),
                ],
            )
        )
        if page.route == "/show_text":
            ShowText(page)
        if page.route == "/show_table":
            ShowTable(page)
        if page.route == "/delete_symbols":
            DeleteSymbols(page)
        if page.route == "/find_line":
            input_field = ft.TextField(label="Введите текст", width=300)
            output_text = ft.Text("")

            def find_last_matching_line(file_path, search_string):
                last_matching_line_number = -1  # Инициализируем переменную для хранения номера строки

                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_number, line in enumerate(file, start=1):
                        if search_string in line:  # Проверяем частичное совпадение
                            last_matching_line_number = line_number

                return last_matching_line_number

            def display_text(e):
                file_path = "C:\\Users\\Егор\\PycharmProjects\\pythonProject\\Test.txt"

                search_string = str(input_field.value)

                last_line_number = find_last_matching_line(file_path, search_string)
                if last_line_number != -1:
                    output_text.value = f"Номер последней строки, содержащей '{search_string}': {last_line_number}"
                else:
                    output_text.value = f"Строка '{search_string}' не найдена в файле."
                page.update()

            page.views.append(
                ft.View(
                    "/delete_symbols",
                    [
                        ft.AppBar(title=ft.Text("Find line"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        ft.ElevatedButton(text="Отправить", on_click=display_text),
                        input_field,
                        output_text
                    ]
                )
            )
        if page.route == "/move_revers_line":
            def read_text_from_file(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()

            # Функция для анимации бегущей строки
            def animate_text(e):
                text_content = read_text_from_file(
                    "C:\\Users\\Егор\\PycharmProjects\\pythonProject\\Test.txt")  # Задаем путь к вашему файлу
                marquee_text.value = text_content + " " * 10  # Добавляем пробелы для паузы между циклами
                marquee_text.update()

                # Двигаем текст справа налево
                for _ in range(len(marquee_text.value) * 3):  # Длительность движения
                    marquee_text.value = marquee_text.value[-1] + marquee_text.value[:-1]
                    page.update()
                    time.sleep(0.1)  # Задержка для плавного движения текста

            marquee_text = ft.Text("", style="headlineMedium")
            page.views.append(
                ft.View(
                    "/move_revers_line",
                    [
                        ft.AppBar(title=ft.Text("Move revers line"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        ft.ElevatedButton(text="Начать движение текста", on_click=animate_text),
                        marquee_text
                    ]
                )
            )
        if page.route == "/draw_square":
            page.views.append(
                ft.View(
                    "/draw_square",
                    [
                        ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        ft.Container(
                            width=100,
                            height=100,
                            bgcolor="blue",  # Цвет квадрата
                            alignment=ft.alignment.center
                        )]
                )
            )
        if page.route == "/draw_triangle_in_circle":

            def draw_shapes(e):
                try:
                    radius = int(radius_input.value)
                    if radius <= 0:
                        error_text.value = "Радиус должен быть положительным числом!"
                        page.update()
                        return

                    # Создаем новый холст
                    canvas_shapes = []

                    # Центр круга
                    center_x, center_y = 200, 200

                    # Рисуем круг
                    canvas_shapes.append(
                        cv.Circle(
                            center_x,  # Координата x центра круга
                            center_y,  # Координата y центра круга
                            radius,
                            ft.Paint(color=ft.colors.RED)  # Цвет заливки круга
                        )
                    )

                    # Координаты треугольника
                    points = []
                    for i in range(3):
                        angle = math.radians(90 + i * 120)  # Угол для равностороннего треугольника
                        x = center_x + radius * math.cos(angle)
                        y = center_y - radius * math.sin(angle)
                        points.append((x, y))  # Добавляем координаты в формате (x, y)

                    # Рисуем треугольник
                    canvas_shapes.append(
                        cv.Path(
                            [
                                cv.Path.MoveTo(points[0][0], points[0][1]),
                                cv.Path.LineTo(points[1][0], points[1][1]),
                                cv.Path.LineTo(points[2][0], points[2][1]),
                            ],
                            ft.Paint(color=ft.colors.GREEN), )
                    )

                    # Обновляем холст с фигурами
                    canvas.content = cv.Canvas(shapes=canvas_shapes)
                    error_text.value = ""
                    page.update()
                except ValueError:
                    error_text.value = "Введите корректное число!"
                    page.update()

            # Поле ввода радиуса
            radius_input = ft.TextField(
                label="Введите радиус круга",
                width=200,
                on_submit=draw_shapes
            )

            # Кнопка для обновления круга и треугольника
            draw_button = ft.ElevatedButton(
                text="Нарисовать",
                on_click=draw_shapes
            )

            # Холст для рисования
            canvas = ft.Container(
                width=400,
                height=400,
                content=cv.Canvas()
            )

            # Текст для вывода ошибок
            error_text = ft.Text(color=ft.colors.RED)

            page.views.append(
                ft.View(
                    "/draw_triangle_in_circle",
                    [
                        ft.AppBar(title=ft.Text("Draw triangle in circle"), bgcolor=ft.colors.SURFACE_VARIANT),
                        radius_input,
                        draw_button,
                        canvas,
                        error_text
                    ]
                )
            )
        if page.route == "/plot_histogram":
            def create_histogram(e):
                content.controls.clear()
                # Считываем вектор из текстового поля
                vector = [float(x) for x in vector_input.value.split()]

                if not vector:
                    raise ValueError("Вектор не может быть пустым. Введите числа, разделенные пробелами.")

                # Построение гистограммы
                plt.figure(figsize=(5, 3))  # Размер графика
                plt.bar(range(len(vector)), vector, color="blue")
                plt.title("Гистограмма")
                plt.xlabel("Индексы")
                plt.ylabel("Значения")

                # Сохранение графика в файл
                filename = f"{uuid4().hex}.png"
                filepath = os.path.join("temp", filename)
                os.makedirs("temp", exist_ok=True)  # Создание директории temp, если её нет
                plt.savefig(filepath, bbox_inches="tight")
                plt.close()  # Закрытие графика
                image = ft.Image(src=filepath, width=600, height=400)
                content.controls.append(image)
                page.update()

            vector_input = ft.TextField(label="Введите вектор значений (через пробел)", width=400)
            plot_button = ft.ElevatedButton("Построить гистограмму", on_click=create_histogram)

            page.views.append(
                ft.View(
                    "/plot_histogram",
                    [
                        ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        vector_input,
                        plot_button,
                        content,
                    ]
                )
            )
        if page.route == "/highlight_matrix_min_max":
            def process_matrix(e):
                try:
                    content.controls.clear()
                    # Считываем матрицу из текстового поля
                    matrix = [[int(x) for x in line.split()] for line in matrix_input.value.split("\n")]
                    flat = [item for sublist in matrix for item in sublist]
                    min_val, max_val = min(flat), max(flat)

                    # Создаем таблицу с подсветкой
                    table = ft.DataTable(
                        columns=[ft.DataColumn(ft.Text(f"Кол-{i}")) for i in range(len(matrix[0]))],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Container(
                                            content=ft.Text(str(cell)),
                                            bgcolor="red" if cell == min_val else "green" if cell == max_val else None,
                                            padding=5
                                        )
                                    )
                                    for cell in row
                                ]
                            )
                            for row in matrix
                        ],
                    )
                    content.controls.append(table)
                    page.update()

                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
                    page.snack_bar.open = True
                    page.update()

            # Поле для ввода матрицы
            matrix_input = ft.TextField(label="Введите матрицу построчно (через пробел)", multiline=True, width=400)
            process_button = ft.ElevatedButton("Обработать", on_click=process_matrix)
            page.views.append(
                ft.View(
                    "/draw_square",
                    [
                        ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        matrix_input,
                        process_button,
                        content
                    ]
                )
            )
        if page.route == "/color_rows_by_index":
            def process_matrix(e):
                try:
                    content.controls.clear()
                    matrix = [[int(x) for x in line.split()] for line in matrix_input.value.split("\n")]
                    offset = int(offset_input.value)
                    table = ft.DataTable(
                        columns=[ft.DataColumn(ft.Text(str(i))) for i in range(len(matrix[0]))],
                        rows=[
                            ft.DataRow(
                                cells=[ft.DataCell(ft.Text(str(cell))) for cell in row],
                                color=f"#{(row_index + offset) % 256:02x}00{256 - (row_index + offset) % 256:02x}",
                            )
                            for row_index, row in enumerate(matrix)
                        ],
                    )
                    content.controls.append(table)
                    page.update()

                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
                    page.snack_bar.open = True
                    page.update()

            # Поле для ввода матрицы
            matrix_input = ft.TextField(label="Введите матрицу построчно (через пробел)", multiline=True, width=400)
            offset_input = ft.TextField(label="Введите смещение", width=300)
            page.views.append(
                ft.View(
                    "/draw_square",
                    [
                        ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        ft.ElevatedButton("Обработать", on_click=process_matrix),
                        matrix_input,
                        offset_input,
                        content
                    ]
                )
            )
        if page.route == "/color_columns_by_reverse_index":
            def process_matrix(e):
                try:
                    content.controls.clear()
                    # Считываем матрицу из текстового поля
                    matrix = [[int(x) for x in line.split()] for line in matrix_input.value.split("\n")]

                    # Проверяем, что матрица не пустая
                    if not matrix or not matrix[0]:
                        raise ValueError("Матрица не должна быть пустой.")

                    # Генерируем цвета
                    num_columns = len(matrix[0])
                    colors = [f"#{(255 - (i % 256)):02x}{(i % 256):02x}00" for i in range(num_columns)]

                    # Используем первый элемент матрицы как смещение
                    base_offset = matrix[0][0]
                    table = ft.DataTable(
                        columns=[ft.DataColumn(ft.Text(f"Кол-{i}")) for i in range(num_columns)],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Container(
                                            content=ft.Text(str(cell)),
                                            bgcolor=colors[(num_columns - col_index - 1 - base_offset) % num_columns],
                                            padding=5
                                        )
                                    )
                                    for col_index, cell in enumerate(row)
                                ]
                            )
                            for row in matrix
                        ],
                    )
                    content.controls.append(table)
                    page.update()

                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
                    page.snack_bar.open = True
                    page.update()

            # Поле для ввода матрицы
            matrix_input = ft.TextField(label="Введите матрицу построчно (через пробел)", multiline=True, width=400)
            process_button = ft.ElevatedButton("Обработать", on_click=process_matrix)
            page.views.append(
                ft.View(
                    "/draw_square",
                    [
                        ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        matrix_input,
                        process_button,
                        content
                    ]
                )
            )
        if page.route == "/gradient_sort_matrix":
            # Функция для генерации случайного цвета
            def gradient_color(row_idx, col_idx, max_rows, max_cols):
                r = int(255 * row_idx / max_rows)  # Увеличение красного по строкам
                g = int(255 * col_idx / max_cols)  # Увеличение зелёного по столбцам
                b = int(255 * (row_idx + col_idx) / (max_rows + max_cols))  # Смешанный эффект
                return f"#{r:02x}{g:02x}{b:02x}"

            def display_matrix(e):
                # Очищаем старое содержимое
                content.controls.clear()

                # Считываем матрицу из текстового поля
                matrix = [[int(x) for x in line.split()] for line in matrix_input.value.split("\n")]

                # Проверяем, что матрица квадратная
                if any(len(row) != len(matrix) for row in matrix):
                    raise ValueError("Матрица должна быть квадратной.")
                # Считываем матрицу из текстового поля
                input_text = matrix_input.value.strip()
                rows = input_text.split("\n")  # Делим на строки
                try:
                    max_rows = len(rows)
                    max_cols = max(len(row.split()) for row in rows)

                    # Генерация элементов матрицы
                    for row_idx, row in enumerate(rows):
                        numbers = row.split()  # Делим строку на элементы
                        content.controls.append(
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(num, color="white"),
                                        bgcolor=gradient_color(row_idx, col_idx, max_rows, max_cols),
                                        padding=10,
                                        alignment=ft.alignment.center,
                                        width=50,
                                        height=50,
                                        border_radius=5,
                                    )
                                    for col_idx, num in enumerate(numbers)
                                ],
                                spacing=5,
                            )
                        )
                    page.update()
                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
                    page.snack_bar.open = True
                    page.update()

            # Поле ввода матрицы
            matrix_input = ft.TextField(
                label="Введите матрицу (числа через пробел, строки через Enter):",
                multiline=True,
                width=400,
                height=200,
            )

            # Кнопка для отображения матрицы
            display_button = ft.ElevatedButton("Показать матрицу", on_click=display_matrix)

            # Добавляем элементы на страницу
            page.views.append(
                ft.View(
                    "/gradient_sort_matrix",
                    [
                        matrix_input,
                        display_button,
                        ft.Divider(),
                        ft.Text("Отображение матрицы:", size=18),
                        content,
                    ]
                )
            )
        if page.route == "/draw_square":
            page.views.append(
                ft.View(
                    "/draw_square",
                    [
                        ft.AppBar(title=ft.Text("Show table"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        ft.Container(
                            width=100,
                            height=100,
                            bgcolor="blue",  # Цвет квадрата
                            alignment=ft.alignment.center
                        )]
                )
            )
        if page.route == "/draw_triangle_with_circle":
            def calculate_and_draw(e):
                try:
                    # Получаем радиус из текстового поля
                    R = float(radius_input.value)
                    if R <= 0:
                        raise ValueError("Радиус должен быть положительным числом.")

                    # Вычисляем координаты вершин равностороннего треугольника
                    side = R * sqrt(3)
                    triangle_points = [
                        (200 + R, 200),  # Вершина 1
                        (200 - R / 2, 200 + side / 2),  # Вершина 2
                        (200 - R / 2, 200 - side / 2),  # Вершина 3
                    ]

                    # Случайный выбор вершины треугольника как центра круга
                    center = random.choice(triangle_points)

                    # Радиус внутреннего круга (четверть основного радиуса)
                    inner_circle_radius = R / 4

                    # Очищаем содержимое перед рисованием
                    canvas_shapes = []
                    # Рисуем фон (белый прямоугольник)
                    canvas_shapes.append(
                        cv.Rect(
                            x=0,
                            y=0,
                            width=400,
                            height=400,
                            paint=ft.Paint(color=ft.colors.WHITE),
                        )
                    )

                    # Рисуем треугольник
                    canvas_shapes.append(
                        cv.Path(
                            [
                                cv.Path.MoveTo(triangle_points[0][0], triangle_points[0][1]),
                                cv.Path.LineTo(triangle_points[1][0], triangle_points[1][1]),
                                cv.Path.LineTo(triangle_points[2][0], triangle_points[2][1]),
                                cv.Path.Close(),
                            ],
                            ft.Paint(color=ft.colors.GREEN),
                        )
                    )
                    center_x, center_y = center[0], center[1]

                    # Рисуем круг
                    canvas_shapes.append(
                        cv.Circle(
                            center_x,
                            center_y,
                            inner_circle_radius,
                            ft.Paint(color=ft.colors.RED)  # Цвет заливки круга
                        )
                    )
                    canvas.content = cv.Canvas(shapes=canvas_shapes)
                    page.update()
                except ValueError as ve:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ve}"))
                    page.snack_bar.open = True
                    page.update()

            # Поле для ввода радиуса
            radius_input = ft.TextField(label="Введите радиус окружности (вписывающей треугольник)", width=400)
            draw_button = ft.ElevatedButton("Построить", on_click=calculate_and_draw)

            # Элемент Canvas для рисования
            canvas = ft.Container(
                width=400,
                height=400,
                content=cv.Canvas()
            )

            # Текст для вывода ошибок
            error_text = ft.Text(color=ft.colors.RED)

            page.views.append(
                ft.View(
                    "/draw_triangle_in_circle",
                    [
                        ft.AppBar(title=ft.Text("Draw triangle in circle"), bgcolor=ft.colors.SURFACE_VARIANT),
                        radius_input,
                        draw_button,
                        canvas,
                        error_text
                    ]
                )
            )
        page.update()
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)