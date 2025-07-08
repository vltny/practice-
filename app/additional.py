import openpyxl

men = ''
def updateMenu():
    global men
    if men == '':
        wb = openpyxl.load_workbook('data/menu.xlsx')
        ws = wb.active
        for col in ws['A1:C33']:
            men = men + '  ' + (str(col[1].value))
        men = men.replace('None', '')
    return men