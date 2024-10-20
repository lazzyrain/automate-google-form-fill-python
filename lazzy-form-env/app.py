# FLASK_APP=app.py flask run
# python3 -m flask run

from flask import Flask, jsonify, request
from googleForm import GoogleForm
import concurrent.futures
import time

gform = GoogleForm()

def sendRespond(status: int, message: str, data: any):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    })

def createApp():
    app = Flask(__name__)

    @app.get('/')
    def index():
        return "Welcome to python flask!"
    
    @app.post('/identify')
    def identify():
        data = request.json
        url = data.get('url')
        response = gform.identify(url=url)
        return sendRespond(200, 'Identifikasi selesai', response)

    @app.post('/form-fill')
    def formFill():
        jsonData = request.json
        url = jsonData.get('url')
        data = jsonData.get('data')
        count = jsonData.get('count')

        def filling_task(indexCount):
            print(f'Running generate ({indexCount})')
            resultFill = gform.filling(url=url, data=data, count=indexCount)
            indexCount += 1
            return resultFill

        results = []
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(filling_task, i): i for i in range(int(count))}
            for future in concurrent.futures.as_completed(futures):
                end_time = time.time()
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(str(e))
        elapsed_time = end_time - start_time

        return sendRespond(200, f'Berhasil melakukan pengisian: {elapsed_time:.2f} detik', [results, [data]])

    @app.post('/form-fill-generate')
    def formFillGenerate():
        jsonData = request.json
        url = jsonData.get('url')
        data = jsonData.get('data')

        def filling_task(indexCount):
            print(f'Running generate ({indexCount})')
            resultFill = gform.filling(url=url, data=data[indexCount], count=indexCount)
            indexCount += 1
            return resultFill

        results = []
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(filling_task, i): i for i in range(len(data))}
            for future in concurrent.futures.as_completed(futures):
                end_time = time.time()
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(str(e))
        elapsed_time = end_time - start_time

        return sendRespond(200, f'Berhasil melakukan pengisian (Generated): {elapsed_time:.2f} detik', [results, data])

    return app

APP = createApp()

if __name__ == '__main__':
    APP.run(debug=True)