import pandas as pd
import matplotlib.pyplot as plt

def analyze_purchases(employee_data_path, purchase_data_path):

    try:
        employee_data = pd.read_csv(employee_data_path)
        purchase_data = pd.read_csv(purchase_data_path, sep=';', on_bad_lines='skip')
        print(purchase_data.columns)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Не удалось найти файл: {e.filename}")

    productivity_threshold = employee_data['Продуктивность сотрудника'].quantile(0.65)  
    high_productivity_employees = employee_data[employee_data['Продуктивность сотрудника'] >= productivity_threshold]['Код сотрудника']

    print("High productivity employees:", high_productivity_employees)
    print("Purchase data head:", purchase_data.head())

    high_productivity_purchases = purchase_data['Код сотрудника'].isin(high_productivity_employees)

    print("Is high_productivity_purchases empty?", high_productivity_purchases.empty)

    category_distribution = purchase_data[high_productivity_purchases]['Категория'].value_counts()

    category_distribution_df = pd.DataFrame({'Категория': category_distribution.index, 'count': category_distribution.values})

    return category_distribution_df

def plot_category_distribution(category_distribution_df, title="Распределение категорий покупок среди высокопродуктивных сотрудников"):
    
    plt.figure(figsize=(12, 6))
    plt.bar(category_distribution_df['Категория'], category_distribution_df['count'], color='#90EE90')
    plt.xlabel("Категория")
    plt.ylabel("Количество покупок")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    employee_data_path = 'pokupki/tps.csv'  # Замените на актуальный путь
    purchase_data_path = 'pokupki/p.csv'  # Замените на актуальный путь

    try:
        category_distribution = analyze_purchases(employee_data_path, purchase_data_path)
        print(category_distribution)
        plot_category_distribution(category_distribution)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except KeyError as e:
        print(f"Ошибка: Отсутствует столбец: {e}")
