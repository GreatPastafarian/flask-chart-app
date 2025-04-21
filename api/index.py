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
        images = []

        for program in data:
            plt.figure(figsize=(10, 4))  # Размер для одного графика
            n = program.get('n', [])
            keff = program.get('keff', [])
            name = program.get('name', 'Unknown')

            # Рассчет среднего
            avg_keff = []
            total = 0.0
            for i, val in enumerate(keff):
                total += val
                avg_keff.append(total / (i + 1))

            # Построение графика
            plt.plot(n, keff, 'o-', markersize=3, label='Данные')
            plt.plot(n, avg_keff, '--', linewidth=1.5, label='Среднее')

            plt.title(f'{name}: Зависимость Keff от N')
            plt.xlabel('Номер поколения (N)')
            plt.ylabel('Keff')
            plt.grid(True, alpha=0.3)
            plt.legend()

            # Сохранение в буфер
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            img_buffer.seek(0)

            images.append({
                'name': name,
                'image': base64.b64encode(img_buffer.read()).decode('utf-8')
            })

        return jsonify({'images': images})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
