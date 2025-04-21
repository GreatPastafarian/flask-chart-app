from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

app = Flask(__name__)

# Устанавливаем стандартный стиль Matplotlib
plt.style.use('default')

def calculate_cumulative_average(values):
    """Рассчет кумулятивного среднего по поколениям"""
    averages = []
    total = 0.0
    for i, val in enumerate(values):
        total += val
        averages.append(total / (i + 1))
    return averages

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    try:
        data = request.json.get('data', [])

        if not data:
            return jsonify({"error": "Нет данных для построения"}), 400

        images = []

        for program in data:
            n = program.get('n', [])
            keff = program.get('keff', [])
            name = program.get('name', 'Unknown')

            if not n or not keff:
                continue

            # Рассчет средних значений
            avg_keff = calculate_cumulative_average(keff)

            # Уменьшаем размер фигуры и разрешение
            plt.figure(figsize=(6, 4))

            # Построение графиков
            plt.plot(n, keff, 'o-',
                     markersize=3,
                     linewidth=1.0,
                     label=f'{name} - данные')

            plt.plot(n, avg_keff, '--',
                     linewidth=1.2,
                     alpha=0.7,
                     label=f'{name} - среднее')

            # Оформление графика
            plt.xlabel('Номер поколения (N)', fontsize=9)
            plt.ylabel('Keff', fontsize=9)
            plt.title(f'Зависимость Keff от номера поколения для {name}', fontsize=11)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend(fontsize=7, loc='upper right')
            plt.tight_layout()

            # Сохранение в буфер с уменьшенным разрешением
            img_buffer = BytesIO()
            plt.savefig(img_buffer,
                         format='png',
                         dpi=75,  # Уменьшаем разрешение
                         bbox_inches='tight')
            plt.close()
            img_buffer.seek(0)

            images.append(img_buffer)

        return jsonify({"images": [img_buffer.getvalue().hex() for img_buffer in images]})

    except Exception as e:
        app.logger.error(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
