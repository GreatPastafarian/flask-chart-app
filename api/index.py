from flask import Flask, request, send_file, jsonify
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
        if not data or not isinstance(data, list):
            raise ValueError("Invalid data format")

        # Преобразование данных в DataFrame
        df_list = []
        for dataset in data:
            df_temp = pd.DataFrame(dataset)
            df_list.append(df_temp)

        df = pd.concat(df_list, ignore_index=True)
        df = df.apply(pd.to_numeric, errors='coerce')  # Преобразование в числовой формат
        print("DataFrame after conversion:", df)

        # Проверка наличия столбцов 'N', 'Keff' и 'avgKeff'
        if 'N' not in df.columns or 'Keff' not in df.columns or 'avgKeff' not in df.columns:
            raise KeyError("Missing required columns 'N', 'Keff' or 'avgKeff'")

        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(df['N'], df['Keff'], label='Keff', marker='o')
        plt.plot(df['N'], df['avgKeff'], label='Average Keff', linestyle='--', marker='x')
        plt.xlabel('N')
        plt.ylabel('Keff')
        plt.title('Keff vs N')
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
