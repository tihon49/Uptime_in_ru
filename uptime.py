import re



def uptime_to_web(value, words_list):
    """
    value: число
    words_list: словарь типа ['день', 'дня', 'дней']

    выводит число и лет/месяцев/недель/дней/часов/минут с учетом склонения
    примеры: 1 год / 2 месяца / 3 недели / 4 дня / 15 часов / 45 минут
    """
    value = int(value)
    if all((value % 10 == 1, value % 100 != 11)):
        return f'{value} {words_list[0]}'
    elif all((2 <= value % 10 <= 4,any((value % 100 < 10, value % 100 >= 20)))):
        return f'{value} {words_list[1]}'
    
    return f'{value} {words_list[2]}'


def parse_uptime(uptime):
    """
    uptime: строка полученная из команды 'uptime -p'

    парсит uptime и выводит его на русском в правильном склонении
    """
    date_to_web = ''

    years_list = ['год', 'года', 'лет']
    months_list = ['месяц', 'месяца', 'месяцев']
    weeks_list = ['неделя', 'недели', 'недель']
    days_list = ['день', 'дня', 'дней']
    hours_list = ['час', 'часа', 'часов']
    minutes_list = ['минута', 'минуты', 'минут']

    year_reg = r'[0-9]+ year'
    month_reg = r'[0-9]+ month'
    week_reg = r'[0-9]+ week'
    day_reg = r'[0-9]+ day'
    hour_reg = r'[0-9]+ hour'
    minute_reg = r'[0-9]+ minute'

    if re.search(year_reg, uptime):
        year = re.search(year_reg, uptime).group().split()[0]
        date_to_web += uptime_to_web(year, years_list) + " "
    if re.search(month_reg, uptime):
        month = re.search(month_reg, uptime).group().split()[0]
        date_to_web += uptime_to_web(month, months_list) + " "
    if re.search(week_reg, uptime):
        week = re.search(week_reg, uptime).group().split()[0]
        date_to_web += uptime_to_web(week, weeks_list) + " "
    if re.search(day_reg, uptime):
        day = re.search(day_reg, uptime).group().split()[0]
        date_to_web += uptime_to_web(day, days_list) + " "
    if re.search(hour_reg, uptime):
        hour = re.search(hour_reg, uptime).group().split()[0]
        date_to_web += uptime_to_web(hour, hours_list) + " "
    if re.search(minute_reg, uptime):
        minute = re.search(minute_reg, uptime).group().split()[0]
        date_to_web += uptime_to_web(minute, minutes_list)

    return date_to_web.strip()


