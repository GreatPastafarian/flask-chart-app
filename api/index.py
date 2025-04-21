from flask import Flask, request, send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    data = request.get_json()
    program_name = data['program']
    calculations = data['calculations']
    avg_keff_data = data['avgKeff']

    plt.figure(figsize=(12, 6))

    # Построение данных каждого расчета
    for calc in calculations:
        n = calc['N']
        keff = calc['Keff']
        plt.plot(n, keff, 'o-', label=f'Расчет {calculations.index(calc) + 1}')

    # Построение среднего Keff
    n_avg = [item['N'] for item in avg_keff_data]
    keff_avg = [item['avgKeff'] for item in avg_keff_data]
    plt.plot(n_avg, keff_avg, '--', color='red', label='Среднее Keff')

    plt.xlabel('Номер поколения')
    plt.ylabel('Keff')
    plt.title(f'Зависимость Keff от номера поколений ({program_name})')
    plt.legend()
    plt.grid(True)

    # Сохранение графика в память
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run()
