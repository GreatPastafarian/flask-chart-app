from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

def calculate_cumulative_average(values):
    """Рассчитывает кумулятивное среднее значение."""
    averages = []
    total = 0.0
    for i, val in enumerate(values):
        total += val
        averages.append(total / (i + 1))
    return averages

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    try:
        # Получаем данные из запроса
        data = request.json.get('data', [])
        print("Received data:", data)  # Логирование полученных данных

        images = []
        for item in data:
            print(f"Processing item: {item}")  # Логирование обрабатываемого элемента

            # Создаем график
            plt.figure(figsize=(6, 3))

            # Основные данные
            plt.plot(item['n'], item['values'], 'o-', markersize=3, label='Данные', alpha=0.7)

            # Среднее значение
            avg_values = calculate_cumulative_average(item['values'])
            plt.plot(item['n'], avg_values, '--', linewidth=1.5, label='Среднее')

            # Настройки графика
            plt.title(item['name'])
            if item['xAxisLabel'] == 'N':
                plt.xlabel("Число частиц " + item['xAxisLabel'])  # Используем подпись для оси X
            else :
                plt.xlabel(item['xAxisLabel'])  # Используем подпись для оси X
            if item['yAxisLabel'] == "H":
              plt.ylabel("Энтропия Шеннона" + item['yAxisLabel'])  # Используем подпись для оси Y
            elif item['yAxisLabel'] == "Keff":
              plt.ylabel("Коэффициент размножения" + item['yAxisLabel'])  # Используем подпись для оси Y
            else :
              plt.ylabel(item['yAxisLabel'])  # Используем подпись для оси Y
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.legend()

            # Сохранение графика в буфер
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()

            # Кодируем изображение в base64
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            images.append({
                'image': image_base64
            })

        # Возвращаем сгенерированные изображения в формате JSON
        return jsonify({'images': images})

    except Exception as e:
        print(f"Error: {str(e)}")  # Логирование ошибки
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
