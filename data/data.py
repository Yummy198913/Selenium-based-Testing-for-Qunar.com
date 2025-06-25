from colorama.ansi import clear_line
from openpyxl import *
from pathlib import Path

data_dir = Path(__file__).parent

def read_excel(path):
    file_path = data_dir / path

    wb = load_workbook(file_path)

    wb = wb.active

    # 转换excel里面空单元格的元素为 '' （空字符串）
    for row in wb.iter_rows(min_row=2, max_col=3, values_only=True):
        converted_row = [cell_value if cell_value is not None else '' for cell_value in row]
        yield converted_row


if __name__ == '__main__':
    for d in read_excel('login_data.xlsx'):
        print(d)