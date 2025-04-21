from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

def calculate_cumulative_average(values):
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
        images = []

        for item in data:
            plt.figure(figsize=(10, 4))

            # Основные данные
            plt.plot(item['n'], item['keff'], 'o-', markersize=3, label='Данные', alpha=0.7)

            # Среднее значение
            avg_keff = calculate_cumulative_average(item['keff'])
            plt.plot(item['n'], avg_keff, '--', linewidth=1.5, label='Среднее')

            # Настройки графика
            plt.title(item['name'])
            plt.xlabel('Номер поколения (N)')
            plt.ylabel('Keff')
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.legend()

            # Сохранение в буфер
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()

            images.append({
                'image': base64.b64encode(buf.getvalue()).decode('utf-8')
            })

        return jsonify({'images': images})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
