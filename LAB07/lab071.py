import pickle

countries = {
    "Россия": {
        "Москва": 12678079,
        "Санкт-Петербург": 5384342,
        "Новосибирск": 1625631,
        "Екатеринбург": 1493749,
        "Казань": 1257391
        },
    "Китай": {
        "Шанхай": 26317104, 
        "Пекин": 21893095, 
        "Гуанчжоу": 14904400,
        "Шэньчжэнь": 12528300, 
        "Чэнду": 11648000
        },
    "Парагвай":{
        "Асунсьон": 542023,
        "Луке": 362862,
        "Капиата":198553,
        "Ламбаре":119795,
        "Каагуасу": 435357,
    },
    "Канада":{
        "Торонто": 2794356,
        "Монреаль": 1762949	,
        "Калгари":1306784,
        "Оттава":1017449,
        "Эдмонтон": 1010899,
    },
    "Ямайка":{
        "Йоханнесбург":4434827,
        "Кейптаун":3995539,
        "Дурбан":3920953,
        "Соуэто":2495921,
        "Претория":1815889,
    },
    "Египет":{
        "Каир":8105071,
        "Александрия":4388219,
        "Гиза":3438401,
        "Суэц":547359,
        "Заказик":314331,
    },
    "Казахстан":{
        "Алматы": 2292333,
        "Астана": 1528887,
        "Шымкент":1256263,
        "Атырау":401669,
        "Павлодар": 336547,
    }
}

print("СРЕДНЯЯ ЧИСЛЕННОСТЬ НАСЕЛЕНИЯ")
average_populations = {}
for country, cities in countries.items():
    avg_population = sum(cities.values()) / len(cities)
    average_populations[country] = avg_population
    print(f"{country}: {avg_population:,.0f} чел.")

print("\nМАКСИМАЛЬНОЕ и МИНИМАЛЬНОЕ СРЕДНЕЕ НАСЕЛЕНИЕ")
max_country = max(average_populations, key=average_populations.get)
min_country = min(average_populations, key=average_populations.get)
print(f"Максимальное среднее население: {max_country} ({average_populations[max_country]:,.0f} чел.)")
print(f"Минимальное среднее население: {min_country} ({average_populations[min_country]:,.0f} чел.)")

print(f"\nГОРОДА С НАСЕЛЕНИЕМ МЕНЬШЕ 500,000")
for country, cities in countries.items():
    smallcities = {city: pop for city, pop in cities.items() if pop < 500000}
    if smallcities:
        print(f"{country}: {', '.join(smallcities.keys())}")

print(f"\n3 САМЫХ КРУПНЫХ ГОРОДА")
all_cities = []
for country, cities in countries.items():
    for city, population in cities.items():
        all_cities.append((city, country, population))
top3 = sorted(all_cities, key=lambda x: x[2], reverse=True)[:3]

for i, (city, country, population) in enumerate(top3, 1):
    print(f"{i}. {city}: {population:,} чел.")

with open('data.pickle', 'wb') as f:
    pickle.dump(countries, f)
print("\n\n\n\n\nЧАСТЬ 2")

def analyze_text_file():
    try:
        with open('input.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Файл 'input.txt' не найден. Создайте файл для анализа.")
        return
    
    total_words = 0
    line_word_counts = []    
    for line in lines:
        words = [word for word in line.strip().split() if word]
        word_count = len(words)
        line_word_counts.append(word_count)
        total_words += word_count
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        output_file.write("АНАЛИЗ ТЕКСТОВОГО ФАЙЛА\n")
        output_file.write(f"Общее количество слов в файле: {total_words}\n\n")        
        output_file.write("АНАЛИЗ ПО СТРОКАМ:\n")
        
        for i, (line, word_count) in enumerate(zip(lines, line_word_counts), 1):
            if total_words > 0:
                percentage = (word_count / total_words) * 100
            else:
                percentage = 0
                
            output_file.write(f"Строка {i}: {word_count} слов ({percentage:.2f}% от общего количества)\n")
            output_file.write(f"Текст: {line.strip()}\n")
            output_file.write("-" * 30 + "\n")
    
    print(f"Результаты записаны в файл 'output.txt'")
    print(f"Общее количество слов: {total_words}")

analyze_text_file()
