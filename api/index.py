from flask import Flask, request, jsonify, send_file
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    try:
        data = request.json['data']

        plt.figure(figsize=(12, 6))

        for program in data:
            n = program['n']
            keff = program['keff']

            # Рассчет скользящего среднего
            window_size = 5
            cumsum = np.cumsum(np.insert(keff, 0, 0))
            avg_keff = (cumsum[window_size:] - cumsum[:-window_size]) / window_size

            plt.plot(n, keff, 'o-', label=f'{program["name"]} (данные)')
            plt.plot(n[window_size-1:], avg_keff, '--', label=f'{program["name"]} (среднее)')

        plt.xlabel('N')
        plt.ylabel('Keff')
        plt.title('Зависимость Keff от N')
        plt.legend()
        plt.grid(True)

        # Сохранение в буфер
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)

        return send_file(img_buffer, mimetype='image/png')

    except Exception as e:
        app.logger.error(f"Ошибка: {str(e)}")
        return jsonify({'error': str(e)}), 500
