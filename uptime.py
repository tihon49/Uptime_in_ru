import re
import subprocess



year_reg = r'[0-9]+ year'
month_reg = r'[0-9]+ month'
week_reg = r'[0-9]+ week'
day_reg = r'[0-9]+ day'
hour_reg = r'[0-9]+ hour'
minute_reg = r'[0-9]+ minute'



def uptime_to_web(value, words_list) -> str:
    """
    value: число
    words_list: словарь типа ['день', 'дня', 'дней']

    возвращает число и лет/месяцев/недель/дней/часов/минут с учетом склонения
    примеры: 1 год / 2 месяца / 3 недели / 4 дня / 15 часов / 45 минут
    """
    value = int(value)
    if all((value % 10 == 1, value % 100 != 11)):
        return f'{value} {words_list[0]}'
    elif all((2 <= value % 10 <= 4,any((value % 100 < 10, value % 100 >= 20)))):
        return f'{value} {words_list[1]}'
    
    return f'{value} {words_list[2]}'



def create_string(reg_exp, uptime, words_list) -> str:
    """возвращает строку для добавления к строке вывода uptime на русском"""
    if re.search(reg_exp, uptime):
        data = re.search(reg_exp, uptime).group().split()[0]
        return uptime_to_web(data, words_list) + " "
    return ""



def parse_uptime(uptime) -> str:
    """
    uptime: строка полученная из команды 'uptime -p'

    парсит uptime и выводит его на русском в правильном склонении
    возвращает полную строку uptime'а
    """
    date_to_web = ''

    years_list = ['год', 'года', 'лет']
    months_list = ['месяц', 'месяца', 'месяцев']
    weeks_list = ['неделя', 'недели', 'недель']
    days_list = ['день', 'дня', 'дней']
    hours_list = ['час', 'часа', 'часов']
    minutes_list = ['минута', 'минуты', 'минут']

    date_to_web += create_string(year_reg, uptime, years_list)
    date_to_web += create_string(month_reg, uptime, months_list)
    date_to_web += create_string(week_reg, uptime, weeks_list)
    date_to_web += create_string(day_reg, uptime, days_list)
    date_to_web += create_string(hour_reg, uptime, hours_list)
    date_to_web += create_string(minute_reg, uptime, minutes_list)

    return date_to_web.strip()


def _shell(cmd):
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        result = proc.communicate()
        out = result[0].decode('utf-8')
        error = result[1].decode('utf-8')
    except Exception as e:
        raise ValueError(f'Error: {e}')
    if proc.returncode == 0:
        return True, out
    return False, error


def days_count_from_uptime() -> int:
    """возвращает кол-во дней из uptime"""
    cmd = "uptime | awk -F'( |,|:)+' " + "'{print $6}'"
    state, res = _shell(cmd)
    if state:
        return int(res)



# print(parse_uptime('up 4 years, 1 month, 3 weeks, 21 days, 15 hours, 45 minutes'))
# Out: '4 года 1 месяц 3 недели 21 день 15 часов 45 минут'

