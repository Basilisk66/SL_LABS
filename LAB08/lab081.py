import requests
import json

def get_asian_countries():
    try:
        url = "https://restcountries.com/v3.1/region/asia"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return None

def filter_countries(countries):
    filtered_countries = []    
    for country in countries:
        try:
            population = country.get('population', 0)
            if population <= 30000000:
                continue
            
            country_data = {
                'name': country.get('name', {}).get('common', 'Unknown'),
                'capital': country.get('capital', ['Unknown'])[0] if country.get('capital') else 'Unknown',
                'area': country.get('area', 0),
                'population': population,
                'flag_url': country.get('flags', {}).get('png', '')
            }            
            if country_data['area'] > 0:
                country_data['population_density'] = round(country_data['population'] / country_data['area'], 2)
            else:
                country_data['population_density'] = 0   
            filtered_countries.append(country_data)
        except Exception as e:
            print(f"Ошибка при обработке страны {country.get('name', {}).get('common', 'Unknown')}: {e}")
            continue
    return filtered_countries

def save_to_json(data, filename='results.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nДанные сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в JSON: {e}")

def download_flag(flag_url, country_name):
    try:
        if not flag_url:
            print(f"URL флага для {country_name} не найден")
            return False
        response = requests.get(flag_url)
        response.raise_for_status()
        filename = f"flag_{country_name.replace(' ', '_').replace('/', '_')}.png"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Флаг сохранен: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при скачивании флага для {country_name}: {e}")
        return False

def main():
    print("АНАЛИЗ АЗИАТСКИХ СТРАН")
    print("Критерии: население > 30 миллионов человек\n")
    countries_data = get_asian_countries()
    if not countries_data:
        print("Не удалось получить данные о странах")
        return    
    print(f"1. Получены данные о {len(countries_data)} азиатских странах\n")
    filtered_countries = filter_countries(countries_data)
    if not filtered_countries:
        print("Не найдено стран, соответствующих критериям")
        return   
    print(f"2. Найдено стран с населением более 30 млн человек: {len(filtered_countries)}")
    save_to_json(filtered_countries, 'results.json')
    print("\n3. Топ-5 стран по плотности населения:")
    print("-" * 60)
    sorted_countries = sorted(filtered_countries, 
                            key=lambda x: x['population_density'], 
                            reverse=True)
    top_5_countries = sorted_countries[:5]
    for i, country in enumerate(top_5_countries, 1):
        print(f"{i}. {country['name']:20} | Плотность: {country['population_density']:8.2f} чел/км²")
    print("\n4. Скачивание флагов топ-5 стран")
    print("-" * 40)
    for country in top_5_countries:
        success = download_flag(country['flag_url'], country['name'])
        if not success:
            print(f"Не удалось скачать флаг для {country['name']}")
    
if __name__ == "__main__":
    main()