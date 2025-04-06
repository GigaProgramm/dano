import pandas as pd
import matplotlib.pyplot as plt

def analyze_purchases(employee_data_path, purchase_data_path):
    try:
        employee_data = pd.read_csv(employee_data_path)
        purchase_data = pd.read_csv(purchase_data_path, sep=';', on_bad_lines='skip')
        print(purchase_data.columns)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Не удалось найти файл: {e.filename}")

    # Предполагается, что в employee_data есть столбец 'Эффективный сотрудник' с булевыми значениями (True/False)
    # Фильтруем только эффективных сотрудников
    effective_employees = employee_data[employee_data['Эффективность'] == True]['Код сотрудника']

    print("Effective employees:", effective_employees)
    print("Purchase data head:", purchase_data.head())

    high_productivity_purchases = purchase_data['Код сотрудника'].isin(effective_employees)

    print("Is high_productivity_purchases empty?", high_productivity_purchases.empty)

    category_distribution = purchase_data[high_productivity_purchases]['Категория'].value_counts()

    category_distribution_df = pd.DataFrame({'Категория': category_distribution.index, 'count': category_distribution.values})

    return category_distribution_df, purchase_data, employee_data

def compare_store_popularity(employee_data, purchase_data):
    """
    Сравнивает популярность магазинов среди эффективных и неэффективных сотрудников,
    учитывая разницу в их количестве.
    """
    effective_employees = employee_data[employee_data['Эффективность'] == True]['Код сотрудника']
    ineffective_employees = employee_data[employee_data['Эффективность'] == False]['Код сотрудника']

    # Фильтруем покупки, сделанные эффективными и неэффективными сотрудниками
    effective_purchases = purchase_data[purchase_data['Код сотрудника'].isin(effective_employees)]
    ineffective_purchases = purchase_data[purchase_data['Код сотрудника'].isin(ineffective_employees)]

    # Считаем количество покупок в каждом магазине для каждой группы
    effective_store_counts = effective_purchases['Категория'].value_counts()
    ineffective_store_counts = ineffective_purchases['Категория'].value_counts()

    # Нормализуем данные, чтобы учесть разницу в количестве сотрудников
    effective_count = len(effective_employees)
    ineffective_count = len(ineffective_employees)

    effective_store_normalized = effective_store_counts / effective_count
    ineffective_store_normalized = ineffective_store_counts / ineffective_count

    # Объединяем данные в один DataFrame для сравнения
    comparison_df = pd.DataFrame({
        'Эффективные': effective_store_normalized,
        'Неэффективные': ineffective_store_normalized
    }).fillna(0)

    # Сортируем по популярности среди эффективных сотрудников
    comparison_df = comparison_df.sort_values(by='Эффективные', ascending=False)

    return comparison_df

def compare_average_purchases(employee_data, purchase_data):
    """
    Сравнивает среднее количество покупок эффективных и неэффективных сотрудников.
    """
    effective_employees = employee_data[employee_data['Эффективность'] == True]['Код сотрудника']
    ineffective_employees = employee_data[employee_data['Эффективность'] == False]['Код сотрудника']

    # Фильтруем покупки, сделанные эффективными и неэффективными сотрудниками
    effective_purchases = purchase_data[purchase_data['Код сотрудника'].isin(effective_employees)]
    ineffective_purchases = purchase_data[purchase_data['Код сотрудника'].isin(ineffective_employees)]

    # Считаем количество покупок для каждой группы
    effective_count = len(effective_purchases)
    ineffective_count = len(ineffective_purchases)

    # Считаем количество сотрудников в каждой группе
    num_effective_employees = len(effective_employees)
    num_ineffective_employees = len(ineffective_employees)

    # Вычисляем среднее количество покупок на сотрудника
    avg_effective_purchases = effective_count / num_effective_employees if num_effective_employees > 0 else 0
    avg_ineffective_purchases = ineffective_count / num_ineffective_employees if num_ineffective_employees > 0 else 0

    return avg_effective_purchases, avg_ineffective_purchases

def plot_employee_effectiveness(employee_data):
    """
    Строит график соотношения эффективных и неэффективных сотрудников.
    """
    effectiveness_counts = employee_data['Эффективность'].value_counts()

    plt.figure(figsize=(8, 6))
    effectiveness_counts.plot(kind='bar', color=['salmon', '#90EE90'])
    plt.title('Соотношение эффективных и неэффективных сотрудников')
    plt.xlabel('Эффективность (True/False)')
    plt.ylabel('Количество сотрудников')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()



 

if __name__ == "__main__":

    employee_data_path = 'pokupki/tps.csv'  # Замените на актуальный путь
    purchase_data_path = 'pokupki/p.csv'  # Замените на актуальный путь

    try:
        category_distribution, purchase_data, employee_data = analyze_purchases(employee_data_path, purchase_data_path)
        print(category_distribution)
        plot_employee_effectiveness(employee_data)

        # Сравниваем популярность магазинов
        store_comparison = compare_store_popularity(employee_data, purchase_data)
        print("\nСравнение популярности магазинов:")
        print(store_comparison)

        # Сравниваем среднее количество покупок
        avg_effective, avg_ineffective = compare_average_purchases(employee_data, purchase_data)
        print(f"\nСреднее количество покупок на эффективного сотрудника: {avg_effective:.2f}")
        print(f"Среднее количество покупок на неэффективного сотрудника: {avg_ineffective:.2f}")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except KeyError as e:
        print(f"Ошибка: Отсутствует столбец: {e}")

        # Попытка построить матрицу корреляций
