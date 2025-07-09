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

    for row in ws.iter_rows(min_row=2):
        name = row[1].value
        price = row[2].value

        if str(name).isupper() and price is None:
            menu_lines.append(f"|<b>{name.strip()}</b>\n")
            continue

        if str(name).islower() and price is None:
            menu_lines.append(f"{name.strip()}")
            continue

        price_str = f"💰 {int(price)} ₽" if price else ""
        menu_lines.append(f"\n<blockquote>{str(name)}\t{price_str}</blockquote>")

    cached_menu = "\n".join(menu_lines)
    cached_day = today
    return cached_menu
