import openpyxl
import shutil
import os

def load_wb():
    wb = openpyxl.load_workbook("base.xlsx")
    return wb

def get_ws():
    return load_wb().active

def clear_col():
    wb = load_wb()
    ws = wb.active
    ws.delete_cols(0)
    ws.delete_cols(2,3)
    ws.delete_cols(3)
    ws.delete_cols(3)
    print(ws)
    # wb.save(filename = "base.xlsx")
    return ws


# def test_clearing(s):
#     # shutil.copyfile("base copy.xlsx", "base.xlsx")
#     data = list(clear_col().iter_rows(values_only=True, min_row=3, max_row=20))
#     pers = [x for x in data if s in x[0]]
#     print(pers)
#     # os.remove('base.xlsx')

# test_clearing('Мусаев')
# test_clearing('Хусиева')