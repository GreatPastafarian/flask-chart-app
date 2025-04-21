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

        plt.figure(figsize=(15, 8))

        # Цветовая палитра для разных программ
        colors = plt.cm.tab10(np.linspace(0, 1, len(data)))

        for idx, program in enumerate(data):
            n = program.get('n', [])
            keff = program.get('keff', [])
            name = program.get('name', 'Unknown')

            if not n or not keff:
                continue

            # Рассчет средних значений
            avg_keff = calculate_cumulative_average(keff)

            # Построение графиков
            color = colors[idx]
            plt.plot(n, keff, 'o-',
                    color=color,
                    markersize=5,
                    linewidth=1.5,
                    label=f'{name} - данные')

            plt.plot(n, avg_keff, '--',
                    color=color,
                    linewidth=2,
                    alpha=0.7,
                    label=f'{name} - среднее')

        # Оформление графика
        plt.xlabel('Номер поколения (N)', fontsize=12)
        plt.ylabel('Keff', fontsize=12)
        plt.title('Зависимость Keff от номера поколения', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10, loc='upper right')
        plt.tight_layout()

        # Сохранение в буфер
        img_buffer = BytesIO()
        plt.savefig(img_buffer,
                  format='png',
                  dpi=300,
                  bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)

        return send_file(img_buffer, mimetype='image/png')

    except Exception as e:
        app.logger.error(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
