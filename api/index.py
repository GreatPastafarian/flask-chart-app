from flask import Flask, request, send_file
import matplotlib.pyplot as plt
import pandas as pd
import io

app = Flask(__name__)

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    try:
        # Логирование входных данных
        data = request.json['data']
        print("Received data:", data)

        # Проверка данных
        if not data or not isinstance(data, list) or not isinstance(data[0], list):
            raise ValueError("Invalid data format")

        # Создание DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        print("DataFrame created successfully:", df)

        # Проверка наличия столбцов 'A' и 'B'
        if 'A' not in df.columns or 'B' not in df.columns:
            raise KeyError("Missing required columns 'A' or 'B'")

        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(df['A'], df['B'], label='Data Line')
        plt.xlabel('A')
        plt.ylabel('B')
        plt.title('A vs B')
        plt.legend()
        plt.grid(True)

        # Сохранение графика в буфер
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        return send_file(img_buf, mimetype='image/png')
    except Exception as e:
        # Логирование ошибки
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
