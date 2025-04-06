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
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except KeyError as e:
        print(f"Ошибка: Отсутствует столбец: {e}")

        # Попытка построить матрицу корреляций
