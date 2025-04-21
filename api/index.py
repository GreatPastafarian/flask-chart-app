function updateChart() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var programsData = [];

  // Настройки строк (проверьте индексы!)
  var PROGRAM_NAME_ROW = 9;    // Строка 10 (индекс 9)
  var DATA_START_ROW = 12;     // Строка 13 (индекс 12)

  for (var col = 0; col < data[0].length; col += 2) {
    var programName = data[PROGRAM_NAME_ROW][col];
    if (!programName) continue;

    var nValues = [];
    var keffValues = [];
    var row = DATA_START_ROW;

    while (row < data.length) {
      var nCell = data[row][col];
      var keffCell = data[row][col + 1];

      if (nCell === "" && keffCell === "") break;

      var n = parseNumber(nCell);
      var keff = parseNumber(keffCell);

      if (isNaN(n) || isNaN(keff)) {
        Logger.log(`Некорректные данные в строке ${row + 1}: N=${nCell}, Keff=${keffCell}`);
        break;
      }

      nValues.push(n);
      keffValues.push(keff);
      row++;
    }

    if (nValues.length !== keffValues.length) {
      Logger.log(`Ошибка для ${programName}: разные длины N(${nValues.length}) и Keff(${keffValues.length})`);
      continue;
    }

    if (nValues.length > 0) {
      programsData.push({
        name: programName.trim(),
        n: nValues,
        keff: keffValues
      });
      Logger.log(`${programName}: собрано ${nValues.length} точек`);
    }
  }

  if (programsData.length === 0) {
    Logger.log("Нет данных для построения");
    return;
  }

  // Отправка данных
  var payload = { data: programsData };
  var url = 'https://flask-chart-app.onrender.com/generate-chart';

  var options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    var response = UrlFetchApp.fetch(url, options);

    if (response.getResponseCode() === 200) {
      var blob = response.getBlob();

      // Найти пустую ячейку для вставки графика
      var lastRow = sheet.getLastRow();
      var lastColumn = sheet.getLastColumn();
      var insertRow = lastRow + 1;
      var insertColumn = lastColumn + 1;

      // Удаление старых изображений в ячейке, если они есть
      var images = sheet.getImages();
      for (var i = 0; i < images.length; i++) {
        var image = images[i];
        if (image.getAnchorCell().getRow() === insertRow && image.getAnchorCell().getColumn() === insertColumn) {
          sheet.removeImage(image);
        }
      }

      // Логирование номера ячейки
      Logger.log(`Inserting image into cell: ${String.fromCharCode(64 + insertColumn)}, ${insertRow}`);

      // Вставка изображения в следующую пустую ячейку
      sheet.insertImage(blob, insertColumn, insertRow);
      Logger.log("График успешно обновлен");
    } else {
      Logger.log("Ошибка сервера: " + response.getContentText());
    }
  } catch (e) {
    Logger.log("Критическая ошибка: " + e.toString());
  }
}

function parseNumber(value) {
  if (typeof value === 'string') {
    const cleaned = value
      .replace(/,/g, '.')
      .replace(/[^0-9.eE-]/g, '');
    return parseFloat(cleaned) || NaN;
  }
  return Number(value);
}
