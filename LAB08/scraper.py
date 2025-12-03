import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import re

BASE_URL = "https://worldathletics.org/records/toplists/sprints"
def get_page_data(year, gender, event_code):
    url = f"{BASE_URL}/{event_code}/outdoor/{gender}/senior/{year}?regionType=world&page=1&bestResultsOnly=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при получении страницы {year}-{gender}-{event_code}: {e}")
        return None

def parse_top_result(html, year, gender, event_code):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    results_table = soup.find('table', class_='records-table')
    if not results_table:
        print(f"Не найдена таблица для {year}-{gender}-{event_code}")
        return None
    first_row = results_table.find('tbody').find('tr') if results_table.find('tbody') else None    
    if not first_row:
        print(f"Нет результатов для {year}-{gender}-{event_code}")
        return None
    cells = first_row.find_all('td')
    if len(cells) < 10:
        return None    
    try:
        mark = cells[4].get_text(strip=True)
        name_cell = cells[2]
        name = name_cell.get_text(strip=True)
        name = re.sub(r'[^\w\s\-\.]', '', name)
        country_cell = cells[3]
        country_span = country_cell.find('span', class_='country')
        country = country_span.get_text(strip=True) if country_span else ''
        date = cells[8].get_text(strip=True)
        mark = mark.replace('A', '').replace('M', '').replace('=', '').strip()
        date = date.replace('.', '-')
        return {
            'year': year,
            'gender': gender,
            'event': event_code,
            'name': name,
            'country': country,
            'mark': mark,
            'date': date
        }
    except Exception as e:
        print(f"Ошибка при парсинге строки для {year}-{gender}-{event_code}: {e}")
        return None

def get_event_code(event_name):
    event_codes = {
        '60m': '60-metres',
        '100m': '100-metres',
        '200m': '200-metres',
        '400m': '400-metres'
    }
    return event_codes.get(event_name, event_name)

def main():
    years = range(2001, 2025)
    genders = ['men', 'women']
    events = ['60m', '100m', '200m', '400m']
    top_results = []
    print("Начинаем сбор данных...")
    print("=" * 50)
    total_requests = len(years) * len(genders) * len(events)
    current_request = 0
    for year in years:
        for gender in genders:
            for event in events:
                current_request += 1
                event_code = get_event_code(event)
                print(f"Обработка: {current_request}/{total_requests} - {year} {gender} {event}")
                html = get_page_data(year, gender, event_code)
                if html:
                    result = parse_top_result(html, year, gender, event)
                    if result:
                        top_results.append(result)
                        print(f"  Найден результат: {result['name']} - {result['mark']}")
                    else:
                        print(f"  Результат не найден")
                else:
                    print(f"  Не удалось получить данные")
                sleep(1)
    save_to_csv(top_results)
    print("\n" + "=" * 50)
    print(f"Сбор данных завершен. Всего собрано результатов: {len(top_results)}")

def save_to_csv(data):
    if not data:
        print("Нет данных для сохранения")
        return
    filename = 'top_results.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['year', 'gender', 'event', 'name', 'country', 'mark', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Данные сохранены в файл: {filename}")
    print("\nСтатистика по собранным данным:")
    print(f"Всего записей: {len(data)}")
    years_count = {}
    for item in data:
        year = item['year']
        years_count[year] = years_count.get(year, 0) + 1
    print(f"Количество лет с данными: {len(years_count)}")

def analyze_url_patterns():
    print("Анализ закономерностей изменения URL:")
    print("-" * 50)
    examples = [
        "https://worldathletics.org/records/toplists/sprints/100-metres/outdoor/men/senior/2024",
        "https://worldathletics.org/records/toplists/sprints/100-metres/outdoor/women/senior/2023",
        "https://worldathletics.org/records/toplists/sprints/200-metres/outdoor/men/senior/2022",
        "https://worldathletics.org/records/toplists/sprints/400-metres/indoor/women/senior/2021"
    ]
    print("Структура URL:")
    print("BASE_URL + /{discipline}/outdoor/{gender}/senior/{year}?parameters")
    print("\nГде:")
    print("- BASE_URL: https://worldathletics.org/records/toplists/sprints")
    print("- discipline: 60-metres, 100-metres, 200-metres, 400-metres")
    print("- gender: men или women")
    print("- year: 2001-2024")
    print("- parameters: параметры фильтрации (страница, регион и т.д.)")
    return {
        'base': 'https://worldathletics.org/records/toplists/sprints',
        'pattern': '/{event}/outdoor/{gender}/senior/{year}?regionType=world&page=1&bestResultsOnly=true',
        'events': {
            '60m': '60-metres',
            '100m': '100-metres', 
            '200m': '200-metres',
            '400m': '400-metres'
        },
        'genders': ['men', 'women']
    }

def analyze_page_structure():
    print("\nАнализ структуры страницы:")
    print("=" * 50)   
    print("Основные элементы для парсинга:")
    print("1. Таблица результатов: <table class='records-table'>")
    print("2. Строки результатов: <tr> внутри <tbody>")
    print("3. Столбцы в строке: <td>")
    print("   - Столбец 2: Имя спортсмена")
    print("   - Столбец 3: Страна (внутри <span class='country'>)")
    print("   - Столбец 4: Результат (время)")
    print("   - Столбец 8: Дата соревнования")
    print("4. Страна: <span class='country'> с текстом и data-code")
    return {
        'table_class': 'records-table',
        'country_span_class': 'country',
        'columns': {
            'name': 2,
            'country': 3, 
            'mark': 4,
            'date': 8
        }
    }

if __name__ == "__main__":
    url_patterns = analyze_url_patterns()
    page_structure = analyze_page_structure()
    main()