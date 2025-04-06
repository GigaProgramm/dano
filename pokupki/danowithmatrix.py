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

    return category_distribution_df, purchase_data

def plot_category_distribution(category_distribution_df, title="Распределение категорий покупок среди эффективных сотрудников"):
    
    plt.figure(figsize=(12, 6))
    plt.bar(category_distribution_df['Категория'], category_distribution_df['count'], color='#90EE90')
    plt.xlabel("Категория")
    plt.ylabel("Количество покупок")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(df):
    """
    Строит матрицу корреляций для числовых столбцов DataFrame.
    """
    numeric_df = df.select_dtypes(include=['number'])
    corr_matrix = numeric_df.corr()

    print(corr_matrix)

    plt.figure(figsize=(10, 8))
    plt.matshow(corr_matrix, fignum=1, cmap='coolwarm')
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar()
    plt.title('Матрица корреляций', fontsize=16)

    # Добавление значений на блоки
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                     ha="center", va="center", color="black")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    employee_data_path = 'pokupki/tps.csv'  # Замените на актуальный путь
    purchase_data_path = 'pokupki/p.csv'  # Замените на актуальный путь

    try:
        category_distribution, purchase_data = analyze_purchases(employee_data_path, purchase_data_path)
        print(category_distribution)
        plot_category_distribution(category_distribution)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except KeyError as e:
        print(f"Ошибка: Отсутствует столбец: {e}")

        # Попытка построить матрицу корреляций
