import csv
import json
import os

def analyze_csv_file():
    try:
        possible_paths = [
            'D://Учеба/СЯП/files/files/csv/5.csv',
            '5.csv',
            './5.csv',
            'D:/Учеба/СЯП/files/files/csv/5.csv'
        ]
        
        data = None
        used_path = ""
        
        for file_path in possible_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file, delimiter=';')
                    data = list(csv_reader)
                    used_path = file_path
                    break
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Ошибка при чтении {file_path}: {e}")
                continue
        
        if data is None:
            print("Ошибка: Файл 5.csv не найден ни по одному из путей!")
            print("Проверьте наличие файла в следующих директориях:")
            for path in possible_paths:
                print(f"  - {path}")
            return None
        
        print(f"\nСОДЕРЖИМОЕ ФАЙЛА 5.csv:")
        print("-" * 80)
        for i, row in enumerate(data, 1):
            print(f"Запись #{i}:")
            for key, value in row.items():
                print(f"  {key} → {value}")
            print("-" * 80)
        
        min_max_result = find_min_max_impressions(data)
        cost_result = calculate_total_cost(data)
        conversion_result = calculate_avg_conversion(data)
        ctr_result = calculate_ctr_by_platform(data)
        
        return {
            'data': data,
            'min_max': min_max_result,
            'cost': cost_result,
            'conversion': conversion_result,
            'ctr': ctr_result
        }
        
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return None

def find_min_max_impressions(data):
    min_impressions = float('inf')
    max_impressions = float('-inf')
    min_campaign = None
    max_campaign = None
    valid_campaigns = 0
    
    for campaign in data:
        try:
            impressions = int(campaign['Impressions'])
            if impressions < min_impressions:
                min_impressions = impressions
                min_campaign = campaign
            if impressions > max_impressions:
                max_impressions = impressions
                max_campaign = campaign
            valid_campaigns += 1
        except (ValueError, KeyError):
            continue
    
    if min_campaign is None or max_campaign is None:
        print("МИНИМАЛЬНОЕ И МАКСИМАЛЬНОЕ КОЛИЧЕСТВО ПОКАЗОВ:")
        print("  Нет данных о показах в файле")
        return None
    
    print(f"МИНИМАЛЬНОЕ КОЛИЧЕСТВО ПОКАЗОВ:")
    print(f"  Кампания: {min_campaign.get('Campaign', 'N/A')}")
    print(f"  Показы: {min_impressions:,}")
    print(f"  Платформа: {min_campaign.get('Platform', 'N/A')}")
    print(f"\nМАКСИМАЛЬНОЕ КОЛИЧЕСТВО ПОКАЗОВ:")
    print(f"  Кампания: {max_campaign.get('Campaign', 'N/A')}")
    print(f"  Показы: {max_impressions:,}")
    print(f"  Платформа: {max_campaign.get('Platform', 'N/A')}") 
    
    return {
        'min_campaign': min_campaign,
        'max_campaign': max_campaign,
        'min_impressions': min_impressions,
        'max_impressions': max_impressions,
        'valid_campaigns': valid_campaigns
    }

def calculate_total_cost(data):    
    total_cost = 0
    valid_campaigns = 0    
    
    for campaign in data:
        try:
            cost = float(campaign['Cost'])
            total_cost += cost
            valid_campaigns += 1
        except (ValueError, KeyError):
            continue    
    
    if valid_campaigns == 0:
        print("ОБЩИЕ ЗАТРАТЫ: Нет данных о затратах")
        return None
    
    avg_cost = total_cost / valid_campaigns if valid_campaigns > 0 else 0
    
    print(f"\nОБЩИЕ ЗАТРАТЫ: {total_cost:,.2f} у.е.")
    print(f"Количество кампаний: {valid_campaigns}")
    if valid_campaigns > 0:
        print(f"Средние затраты на кампанию: {avg_cost:,.2f} у.е.")
    
    return {
        'total_cost': total_cost,
        'valid_campaigns': valid_campaigns,
        'avg_cost': avg_cost
    }

def calculate_avg_conversion(data):
    conversions = []    
    
    for campaign in data:
        try:
            conversion = float(campaign['Conversions'])
            conversions.append(conversion)
        except (ValueError, KeyError):
            continue    
    
    if conversions:
        avg_conversion = sum(conversions) / len(conversions)
        min_conv = min(conversions)
        max_conv = max(conversions)        
        
        print(f"СРЕДНИЙ ПРОЦЕНТ КОНВЕРСИИ: {avg_conversion:.2f}%")
        print(f"Диапазон конверсии: {min_conv:.2f}% - {max_conv:.2f}%")
        print(f"Количество кампаний с данными: {len(conversions)}")
        
        return {
            'avg_conversion': avg_conversion,
            'min_conversion': min_conv,
            'max_conversion': max_conv,
            'campaigns_with_data': len(conversions)
        }
    else:
        print("Нет данных о конверсии")
        return None

def calculate_ctr_by_platform(data):    
    platform_stats = {}    
    
    for campaign in data:
        try:
            platform = campaign['Platform']
            clicks = int(campaign['Clicks'])
            impressions = int(campaign['Impressions'])            
            
            if platform not in platform_stats:
                platform_stats[platform] = {'clicks': 0, 'impressions': 0, 'campaigns': 0}            
            
            platform_stats[platform]['clicks'] += clicks
            platform_stats[platform]['impressions'] += impressions
            platform_stats[platform]['campaigns'] += 1
        except (ValueError, KeyError):
            continue
    
    ctr_results = {}
    for platform, stats in platform_stats.items():
        if stats['impressions'] > 0:
            ctr = (stats['clicks'] / stats['impressions']) * 100
            efficiency = stats['clicks'] / stats['campaigns'] if stats['campaigns'] > 0 else 0
            ctr_results[platform] = {
                'ctr': ctr,
                'clicks': stats['clicks'],
                'impressions': stats['impressions'],
                'campaigns': stats['campaigns'],
                'efficiency': efficiency
            }    
    
    if ctr_results:
        print("CTR ПО ПЛАТФОРМАМ:")
        for platform, stats in ctr_results.items():
            print(f"     {platform}:")
            print(f"     CTR: {stats['ctr']:.2f}%")
            print(f"     Клики: {stats['clicks']:,}")
            print(f"     Показы: {stats['impressions']:,}")
            print(f"     Кампании: {stats['campaigns']}")
            print(f"     Общая эффективность: {stats['efficiency']:.1f} кликов/кампанию\n")
    else:
        print("Нет данных по платформам")
    
    return ctr_results

def analyze_json_file():
    try:
        possible_paths = [
            'D://Учеба/СЯП/files/files/json/5.json',
            '5.json',
            './5.json',
            'D:/Учеба/СЯП/files/files/json/5.json'
        ]
        
        data = None
        used_path = ""
        
        for file_path in possible_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    used_path = file_path
                    break
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Ошибка при чтении {file_path}: {e}")
                continue
        
        if data is None:
            print("Ошибка: Файл 5.json не найден ни по одному из путей!")
            print("Проверьте наличие файла в следующих директориях:")
            for path in possible_paths:
                print(f"  - {path}")
            return None
       
        print("\n" + "-"*80)
        print(f"СОДЕРЖИМОЕ ФАЙЛА 5.json")
        print("-"*80)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
        students = data.get('students', [])
        if not students:
            print("В файле нет данных о студентах или ключ 'students' отсутствует")
            return None
        
        print(f"\nВсего студентов в базе: {len(students)}")
        
        search_result = find_students_by_name_prefix(students)
        grade_result = count_students_by_grade(students)
        gpa_result = calculate_avg_gpa(students)
        save_analysis_results(students, search_result, grade_result, gpa_result)        
        
        return {
            'data': data,
            'search_result': search_result,
            'grade_result': grade_result,
            'gpa_result': gpa_result
        }
        
    except FileNotFoundError:
        print("Ошибка: Файл 5.json не найден!")
        return None
    except json.JSONDecodeError:
        print("Ошибка: Файл 5.json содержит некорректный JSON!")
        return None
    except Exception as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return None

def find_students_by_name_prefix(students):
    print("ПОИСК СТУДЕНТОВ ПО ПЕРВЫМ 3 БУКВАМ ИМЕНИ")
    if not students:
        print("Нет данных о студентах для поиска")
        return {'found_students': [], 'search_prefix': '', 'count': 0}    
    try:
        prefix = input("Введите первые буквы имени для поиска: ").strip()    
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван пользователем")
        return {'found_students': [], 'search_prefix': '', 'count': 0}    
    if not prefix:
        print("Не введены буквы для поиска")
        return {'found_students': [], 'search_prefix': '', 'count': 0}
    
    search_prefix = prefix[:3].lower()
    
    found_students = []
    for student in students:
        first_name = student.get('first_name', '').lower()
        if first_name.startswith(search_prefix):
            found_students.append(student)
    
    if found_students:
        print(f"Найдено студентов с именем начинающимся на '{prefix[:3]}': {len(found_students)}")
        print("_" * 60)
        for i, student in enumerate(found_students, 1):
            print(f"{i}. ID студента: {student.get('student_id', 'N/A')}")
            print(f"   Полное имя: {student.get('first_name', 'N/A')} {student.get('last_name', 'N/A')}")
            print(f"   Оценка: {student.get('grade', 'N/A')}")
            print(f"   GPA: {student.get('gpa', 'N/A')}")
            print(f"   Предметы: {', '.join(student.get('subjects', []))}")
            print(f"   Посещаемость: {student.get('attendance', 'N/A')}%")
        print("-" * 60)
    else:
        print(f"\nСтудентов с именем начинающимся на '{prefix[:3]}' не найдено")
    
    return {
        'found_students': found_students,
        'search_prefix': prefix[:3],
        'count': len(found_students),
        'search_details': {
            'total_students_searched': len(students),
        }
    }

def count_students_by_grade(students):
    print("КОЛИЧЕСТВО СТУДЕНТОВ ПО ОЦЕНКАМ")     
    if not students:
        print("Нет данных о студентах")
        return {}        
    grade_count = {}    
    for student in students:
        grade = student.get('grade', 'Не указана')
        grade_count[grade] = grade_count.get(grade, 0) + 1    
    grade_percentage = {}
    for grade, count in grade_count.items():
        percentage = (count / len(students)) * 100
        grade_percentage[grade] = round(percentage, 1)    
    
    if grade_count:
        print("Распределение студентов по оценкам:")
        for grade, count in sorted(grade_count.items()):
            percentage = grade_percentage[grade]
            print(f"  • {grade}: {count} студент(ов) ({percentage:.1f}%)")
    else:
        print("Нет данных об оценках")
    
    return {
        'grade_distribution': grade_count,
        'grade_percentage': grade_percentage,
        'total_students': len(students)
    }

def calculate_avg_gpa(students):
    print("СРЕДНИЙ GPA")     
    if not students:
        print("Нет данных о студентах")
        return {'avg_gpa': 0.0, 'valid_students': 0, 'total_students': 0}    
    
    total_gpa = 0
    valid_students = 0        
    for student in students:
        try:
            gpa = float(student.get('gpa', 0))
            total_gpa += gpa
            valid_students += 1
        except (ValueError, TypeError):
            continue   
    
    if valid_students > 0:
        avg_gpa = total_gpa / valid_students
        print(f"Средний GPA всех студентов: {avg_gpa:.2f}")
        print(f"Обработано записей: {valid_students} из {len(students)}")        
        
        return {
            'avg_gpa': round(avg_gpa, 2),
            'valid_students': valid_students,
            'total_students': len(students)
        }
    else:
        print("Нет валидных данных о GPA")
        return {'avg_gpa': 0.0, 'valid_students': 0, 'total_students': len(students)}

def save_analysis_results(students, search_result, grade_result, gpa_result):    
    if not students:
        print("Нет данных для сохранения")
        return
    
    output_data = {
        "analysis_summary": {
            "total_students": len(students),
        },
        "search_by_name_prefix": {
            "search_prefix": search_result.get('search_prefix', ''),
            "found_count": search_result.get('count', 0),
            "found_students": search_result.get('found_students', [])
        },
        "grade_statistics": {
            "total_students": grade_result.get('total_students', 0),
            "distribution": grade_result.get('grade_distribution', {}),
            "percentage": grade_result.get('grade_percentage', {})
        },
        "gpa_analysis": {
            "average_gpa": gpa_result.get('avg_gpa', 0.0),
            "students_with_valid_gpa": gpa_result.get('valid_students', 0),
            "total_students_analyzed": gpa_result.get('total_students', 0)
        },
        "all_students": students
    }
    
    try:
        os.makedirs('D://Учеба/СЯП/Laba7Python', exist_ok=True)
        
        with open('D://Учеба/СЯП/Laba7Python/out.json', 'w', encoding='utf-8') as file:
            json.dump(output_data, file, ensure_ascii=False, indent=2)                
        print(f"Результаты анализа сохранены в файл out.json")
        print(f"Всего студентов: {len(students)}")
        print(f"Найдено по префиксу '{search_result.get('search_prefix', '')}': {search_result.get('count', 0)}")
        print(f"Средний GPA: {gpa_result.get('avg_gpa', 0.0):.2f}")
        print(f"Распределение по оценкам: {grade_result.get('grade_distribution', {})}")
        
    except Exception as e:
        print(f"Ошибка при сохранении файла out.json: {e}")

def main():    
    csv_results = analyze_csv_file()
    json_results = analyze_json_file()    

if __name__ == "__main__":
    main()