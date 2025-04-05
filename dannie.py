import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Чтение данных с указанием разделителя и обработкой ошибок
try:
    data = pd.read_csv('how.csv', sep=';', encoding='utf-8', header=0)
except UnicodeDecodeError:
    data = pd.read_csv('how.csv', sep=';', encoding='latin1', header=0)

# Вывод информации о данных
print("Доступные колонки в файле:", data.columns.tolist())
print("\nПервые 5 строк данных:")
print(data.head())

# Определение правильных названий колонок
mission_column = 'Название миссии'
reward_column = 'Сумма вознаграждения'

# Проверка наличия колонок
if mission_column not in data.columns or reward_column not in data.columns:
    print("\nНе удалось найти нужные колонки. Пожалуйста, укажите правильные названия колонок:")
    print("1. Колонка с названием миссии:", mission_column)
    print("2. Колонка с вознаграждением:", reward_column)
    raise ValueError("Необходимо указать правильные названия колонок")

# Преобразование колонки с вознаграждением в числовой формат
data[reward_column] = pd.to_numeric(data[reward_column], errors='coerce')

# Группировка данных по названию миссии и суммирование вознаграждений
mission_rewards = data.groupby(mission_column)[reward_column].sum().reset_index()

# Сортировка данных по сумме вознаграждений и выбор топ-10
mission_rewards = mission_rewards.sort_values(reward_column, ascending=False).head(10)

# Настройка стиля графика
plt.figure(figsize=(15, 8))
sns.set_style("whitegrid")

# Создание горизонтальной столбчатой диаграммы
ax = sns.barplot(x=reward_column, y=mission_column, data=mission_rewards, orient='h', color='lightgreen')

# Настройка заголовка и меток
plt.title('Топ-10 миссий по сумме вознаграждений', fontsize=16, pad=20)
plt.xlabel('Общая сумма вознаграждений', fontsize=12)
plt.ylabel('Название миссии', fontsize=12)

# Поворот подписей по оси X для лучшей читаемости
plt.xticks(rotation=45, ha='right')

# Добавление значений на столбцы
for p in ax.patches:
    width = p.get_width()
    ax.annotate(f'{width:,.0f}'.replace(',', ' '),
                (width, p.get_y() + p.get_height()/2),
                ha='left', va='center',
                xytext=(5, 0),
                textcoords='offset points',
                fontsize=10, color='black')

# Автоматическая настройка макета
plt.tight_layout()

# Сохранение графика
plt.savefig('top_10_mission_rewards.png', dpi=300, bbox_inches='tight')

# Показать график
plt.show()

# Вывод топ-10 миссий в консоль
print("\nТоп-10 миссий по сумме вознаграждений:")
print(mission_rewards.to_string(index=False))
