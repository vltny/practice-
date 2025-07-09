import openpyxl
from datetime import datetime

cached_menu = ''
cached_day = None

def updateMenu():
    global cached_menu, cached_day

    weekday_map = {
        0: "пн",
        1: "вт",
        2: "ср",
        3: "чт",
        4: "пт",
        5: "Суббота",
        6: "Воскресенье"
    }
    today = weekday_map[datetime.now().weekday()]

    if cached_menu and cached_day == today:
        return cached_menu

    wb = openpyxl.load_workbook('data/menu.xlsx')
    ws = wb[today]

    menu_lines = []

    isFood = False
    cnt = 0
    for row in ws.rows:
        if cnt < 1:
            cnt += 1
            menu_lines.append(row[1].value)
            continue

        item = (row[1], row[2])

        if item[1].value:
            # Блюдо
            if isFood:
                menu_lines.append(f"</blockquote>\n<blockquote><b>{item[0].value} 💰 {str(item[1].value)}₽</b>\n")
            else:
                menu_lines.append(f"<blockquote><b>{item[0].value} 💰 {str(item[1].value)}₽</b>\n")
            isFood = True
            pass
        elif item[0].fill.start_color.theme == 9:
            # Заголовок
            if isFood:
                menu_lines.append(f"</blockquote>\n\n|<u><b>{item[0].value}</b></u>\n\n")
            else:
                menu_lines.append(f"|<u><b>{item[0].value}</b></u>\n\n")
            isFood = False
        else:
            # Состав
            if not isFood:
                menu_lines.append(f"<i>({item[0].value})</i>")
            else:
                menu_lines.append(f"<i>({item[0].value})</i></blockquote>\n\n")
            isFood = False

    print(cached_menu)
    cached_menu = ''.join(menu_lines) + '</blockquote>'
    print(cached_menu)
    cached_day = today
    return cached_menu
