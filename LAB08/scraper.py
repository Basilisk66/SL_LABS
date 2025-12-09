import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import re

BASE_URL = "https://worldathletics.org/records/toplists/sprints"

def get_page_data(year, gender, event_code):
    url = f"{BASE_URL}/{event_code}/outdoor/{gender}/senior/{year}?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://worldathletics.org/',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        if "No results found" in response.text:
            print(f"Нет результатов для {year}-{gender}-{event_code}")
            return None            
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при получении страницы {year}-{gender}-{event_code}: {e}")
        return None

def parse_top_result(html, year, gender, event_code):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    results_tables = soup.find_all('table', class_='records-table')
    if not results_tables:
        results_tables = soup.find_all('table')
        if not results_tables:
            print(f"Не найдено таблиц для {year}-{gender}-{event_code}")
            return None
    results_table = results_tables[0]
    tbody = results_table.find('tbody')
    if not tbody:
        tbody = results_table
    rows = tbody.find_all('tr')
    if not rows:
        print(f"Нет строк в таблице для {year}-{gender}-{event_code}")
        return None
    first_row = rows[0]
    cells = first_row.find_all('td')
    try:
        if len(cells) >= 8:
            name_cell = cells[3]
            name_link = name_cell.find('a')
            if name_link:
                name = name_link.get_text(strip=True)
            else:
                name = name_cell.get_text(strip=True)
            country_cell = cells[5]
            country_img = country_cell.find('img')
            if country_img:
                country = country_img.get('title', '') or country_img.get('alt', '')
            else:
                country_span = country_cell.find('span', class_='country')
                if country_span:
                    country = country_span.get_text(strip=True)
                else:
                    country = country_cell.get_text(strip=True)
            
            mark_cell = cells[1]
            mark = mark_cell.get_text(strip=True)
            
            date_cell = cells[9]
            date = date_cell.get_text(strip = True)

        name = re.sub(r'\s+', ' ', name).strip() if name else ""
        country = re.sub(r'\s+', ' ', country).strip() if country else ""
        mark = re.sub(r'[^\d\.:]', '', mark).strip() if mark else ""
        date = date.replace('.', '-').replace('/', '-').strip() if date else ""
        if not name or not mark:
            print(f"  Недостаточно данных: имя='{name}', результат='{mark}'")
            return None        
        print(f"  Парсинг успешен: {name} из {country} - {mark} ({date})")        
        return {
            'year': year,
            'gender': gender,
            'event': event_code.replace('-metres', 'm'),
            'name': name,
            'country': country,
            'mark': mark,
            'date': date
        }
        
    except Exception as e:
        print(f"Ошибка при парсинге строки для {year}-{gender}-{event_code}: {e}")
        print("Содержимое ячеек для отладки:")
        for i, cell in enumerate(cells[:10]):
            text = cell.get_text(strip=True)
            print(f"  Ячейка {i}: '{text[:50]}'")
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
    years = range(2024, 2025)
    genders = ['men', 'women']
    events = ['60m', '100m', '200m', '400m']    
    top_results = []
    print("НАЧАЛО СБОРА ДАННЫХ")
    print(f"Период: {years[0]}-{years[-1]}")
    print(f"Дисциплины: {', '.join(events)}")
    print(f"Пол: мужчины и женщины")
    total_requests = len(years) * len(genders) * len(events)
    current_request = 0
    successful_requests = 0
    for year in years:
        for gender in genders:
            for event in events:
                current_request += 1
                event_code = get_event_code(event)
                sleep(2)
                print(f"\n[{current_request}/{total_requests}] Обработка: {year} {gender} {event}")
                print(f"URL: {BASE_URL}/{event_code}/outdoor/{gender}/senior/{year}")
                html = get_page_data(year, gender, event_code)
                if html:
                    sleep(1)
                    result = parse_top_result(html, year, gender, event_code)
                    if result:
                        top_results.append(result)
                        successful_requests += 1
                        print(f"✓ Успешно сохранен результат")
                    else:
                        print(f"✗ Не удалось извлечь данные из страницы")
                else:
                    print(f"✗ Не удалось получить данные с сайта")
                
                sleep(1)
    save_to_csv(top_results)
    print("СБОР ДАННЫХ ЗАВЕРШЕН")
    return top_results

def save_to_csv(data):
    if not data:
        print("Нет данных для сохранения")
        return
    filename = 'top_results.csv'
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['year', 'gender', 'event', 'name', 'country', 'mark', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            data_sorted = sorted(data, key=lambda x: (x['year'], x['gender'], x['event']))
            for row in data_sorted:
                writer.writerow(row)
        print(f"\n✓ Данные успешно сохранены в файл: {filename}")
        
        
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")

def analyze_site_structure():
    print("АНАЛИЗ СТРУКТУРЫ САЙТА")
    try:
        test_url = "https://worldathletics.org/records/toplists/sprints/100-metres/outdoor/men/senior/2023"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(test_url, headers=headers, timeout=10)    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            print(f"Найдено таблиц на странице: {len(tables)}")
            for i, table in enumerate(tables[:2]):
                print(f"\nТаблица {i+1}:")
                print(f"  Классы: {table.get('class', ['нет классов'])}")
                rows = table.find_all('tr')
                print(f"  Строк: {len(rows)}")
                if rows:
                    cols = rows[0].find_all(['td', 'th'])
                    print(f"  Столбцов в первой строке: {len(cols)}")
                    print("  Заголовки столбцов:")
                    for j, col in enumerate(cols[:5]): 
                        text = col.get_text(strip=True)
                        print(f"    Колонка {j}: '{text[:30]}'")
            
        else:
            print(f"Сайт недоступен (код: {response.status_code})")
            
    except Exception as e:
        print(f"✗ Ошибка при проверке сайта: {e}")

    return True

if __name__ == "__main__":
    analyze_site_structure()
    sleep(2)
    results = main()
    print("\n" + "=" * 60)
    if results:
        print(f"ИТОГ: Успешно собрано {len(results)} записей")
        print("Данные сохранены в файл: top_results.csv")
    else:
        print("ИТОГ: Не удалось собрать данные")
    print("=" * 60)