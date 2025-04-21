from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    data = request.json['data']

    for calculation_name, values in data.items():
        N = values['N']
        keff = values['keff']

        # Вычисление среднего keff
        avg_keff = [sum(keff[:i+1]) / (i+1) for i in range(len(keff))]

        # Построение графика
        plt.figure(figsize=(12, 6))
        plt.plot(N, keff, 'o-', label='keff')
        plt.plot(N, avg_keff, '--', label='Среднее keff')
        plt.xlabel('N')
        plt.ylabel('keff')
        plt.title(f'Зависимость keff от N для {calculation_name}')
        plt.legend()
        plt.grid(True)

        # Сохранение графика в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()

        # Возвращение изображения в ответе
        return jsonify({'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True)
