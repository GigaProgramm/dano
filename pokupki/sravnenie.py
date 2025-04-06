import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
from statsmodels.stats.power import TTestIndPower

def analyze_purchases(employee_data_path, purchase_data_path):
    """Загружает и анализирует данные о сотрудниках и покупках"""
    try:
        employee_data = pd.read_csv(employee_data_path)
        purchase_data = pd.read_csv(purchase_data_path, sep=';', on_bad_lines='skip')
        
        # Проверка необходимых столбцов
        required_employee_cols = {'Код сотрудника', 'Эффективность'}
        required_purchase_cols = {'Код сотрудника', 'Категория'}
        
        if not required_employee_cols.issubset(employee_data.columns):
            missing = required_employee_cols - set(employee_data.columns)
            raise KeyError(f"В данных сотрудников отсутствуют столбцы: {missing}")
            
        if not required_purchase_cols.issubset(purchase_data.columns):
            missing = required_purchase_cols - set(purchase_data.columns)
            raise KeyError(f"В данных покупок отсутствуют столбцы: {missing}")

        return employee_data, purchase_data

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Не удалось найти файл: {e.filename}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке данных: {str(e)}")

def plot_employee_effectiveness(employee_data):
    """Визуализирует распределение эффективности сотрудников"""
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Эффективность', data=employee_data, palette=['#ff6b6b', '#51cf66'])
    plt.title('Распределение эффективности сотрудников', pad=20)
    plt.xlabel('Эффективность')
    plt.ylabel('Количество сотрудников')
    
    # Добавление процентов
    total = len(employee_data)
    for p in plt.gca().patches:
        percentage = f'{100 * p.get_height()/total:.1f}%'
        plt.gca().annotate(percentage, 
                          (p.get_x() + p.get_width()/2., p.get_height()), 
                          ha='center', va='center', 
                          xytext=(0, 5), 
                          textcoords='offset points')
    
    plt.tight_layout()
    plt.show()

def plot_purchase_comparison(effective_counts, ineffective_counts):
    """Визуализирует сравнение покупок между группами"""
    plt.figure(figsize=(12, 6))
    
    # Boxplot
    plt.subplot(1, 2, 1)
    sns.boxplot(y=effective_counts, color='#51cf66', label='Эффективные')
    sns.boxplot(y=ineffective_counts, color='#ff6b6b', label='Неэффективные')
    plt.title('Распределение количества покупок (Boxplot)')
    plt.ylabel('Количество покупок')
    plt.legend()
    
    # Гистограмма
    plt.subplot(1, 2, 2)
    sns.histplot(effective_counts, color='#51cf66', label='Эффективные', kde=True, alpha=0.6)
    sns.histplot(ineffective_counts, color='#ff6b6b', label='Неэффективные', kde=True, alpha=0.6)
    plt.title('Гистограмма количества покупок')
    plt.xlabel('Количество покупок')
    plt.ylabel('Частота')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def perform_statistical_analysis(effective_counts, ineffective_counts):
    """Выполняет статистический анализ"""
    print("\n" + "="*50)
    print("Статистический анализ различий между группами")
    print("="*50)
    
    # Проверка нормальности распределения
    _, p_normal_effective = stats.shapiro(effective_counts)
    _, p_normal_ineffective = stats.shapiro(ineffective_counts)
    print(f"\nТест Шапиро-Уилка на нормальность:")
    print(f"Эффективные сотрудники: p-value = {p_normal_effective:.4f}")
    print(f"Неэффективные сотрудники: p-value = {p_normal_ineffective:.4f}")
    
    # Выбор теста в зависимости от нормальности распределения
    if p_normal_effective > 0.05 and p_normal_ineffective > 0.05:
        print("\nДанные распределены нормально, используем t-тест")
        stat, p_value = stats.ttest_ind(effective_counts, ineffective_counts)
        test_name = "t-тест"
    elif len(effective_counts) < 2 or len(ineffective_counts) < 2:
        print("\nНедостаточно данных для проведения теста Манна-Уитни")
        stat, p_value = np.nan, np.nan
        test_name = "Нет теста"
    
    # Mann-Whitney test
    stat_mann, p_value_mann = stats.mannwhitneyu(effective_counts, ineffective_counts)
    test_name_mann = "Тест Манна-Уитни"
    print(f"\nРезультаты {test_name_mann}:")
    print(f"Статистика: {stat_mann:.3f}, p-value: {p_value_mann:.4f}")
    if p_value_mann < 0.05:
        print("\np < 0.05")
    else:
        print("\np ≥ 0.05")
    
    print(f"\nРезультаты {test_name}:")
    print(f"Статистика: {stat:.3f}, p-value: {p_value:.4f}")
    
    if test_name != "Нет теста" and p_value < 0.05:
        print("\nВывод: Существуют статистически значимые различия между группами (p < 0.05)")
    elif test_name != "Нет теста":
        print("\nВывод: Нет статистически значимых различий между группами (p ≥ 0.05)")
    else:
        print("\nВывод: Невозможно сделать вывод из-за недостатка данных.")
    
    # Анализ мощности теста
    effect_size = (np.mean(effective_counts) - np.mean(ineffective_counts)) / np.std(np.concatenate([effective_counts, ineffective_counts]))
    power = TTestIndPower().solve_power(effect_size=effect_size, 
                                      nobs1=len(effective_counts), 
                                      alpha=0.05)
    print(f"\nАнализ мощности теста:")
    print(f"Размер эффекта: {effect_size:.3f}")
    print(f"Мощность теста: {power:.3f}")



if __name__ == "__main__":
    # Пути к файлам данных
    employee_data_path = 'pokupki/tps.csv'
    purchase_data_path = 'pokupki/p.csv'
    
    try:
        # Загрузка данных
        employee_data, purchase_data = analyze_purchases(employee_data_path, purchase_data_path)
        
        # Визуализация распределения эффективности
        plot_employee_effectiveness(employee_data)
        
        # Разделение сотрудников на группы
        effective_employees = employee_data[employee_data['Эффективность'] == True]['Код сотрудника']
        ineffective_employees = employee_data[employee_data['Эффективность'] == False]['Код сотрудника']
        
        # Подсчет количества покупок для каждого сотрудника
        effective_counts = purchase_data[purchase_data['Код сотрудника'].isin(effective_employees)]['Код сотрудника'].value_counts()
        ineffective_counts = purchase_data[purchase_data['Код сотрудника'].isin(ineffective_employees)]['Код сотрудника'].value_counts()
        
        # Заполнение нулями для сотрудников без покупок
        all_effective = pd.Series(0, index=effective_employees)
        all_ineffective = pd.Series(0, index=ineffective_employees)
        
        effective_counts = all_effective.add(effective_counts, fill_value=0).values
        ineffective_counts = all_ineffective.add(ineffective_counts, fill_value=0).values
        
        # Основные метрики
        print("\nОсновные метрики:")
        print(f"Эффективные сотрудники (n={len(effective_counts)}):")
        print(f"Среднее количество покупок: {np.mean(effective_counts):.2f}")
        print(f"Медиана: {np.median(effective_counts):.2f}")
        
        print(f"\nНеэффективные сотрудники (n={len(ineffective_counts)}):")
        print(f"Среднее количество покупок: {np.mean(ineffective_counts):.2f}")
        print(f"Медиана: {np.median(ineffective_counts):.2f}")
        
        # Статистический анализ
        perform_statistical_analysis(effective_counts, ineffective_counts)

        # Визуализация сравнения покупок
        plot_purchase_comparison(effective_counts, ineffective_counts)

    except Exception as e:
        print(f"Ошибка при выполнении программы: {str(e)}")
