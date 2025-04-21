from flask import Flask, request, send_file
import matplotlib.pyplot as plt
import pandas as pd
import io

app = Flask(__name__)

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    data = request.json['data']
    df = pd.DataFrame(data[1:], columns=data[0])

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

if __name__ == '__main__':
    app.run(debug=True)
