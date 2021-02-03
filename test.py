import openpyxl


# class Person():
#     def __init__(self, fio=None, saldo=None):
#         self.fio = fio
#         self.saldo = saldo

# people = []

wb = openpyxl.load_workbook("base.xlsx")
ws = wb.active

data = list(ws.iter_rows(values_only=True))


pers = [x for x in data if 'Ибрагим' in x[0]]

print(pers)