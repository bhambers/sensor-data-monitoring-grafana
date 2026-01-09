import adafruit_dht as dht_sensor
import time
import board
from flask import Flask, Response
from prometheus_client import Counter, Gauge, start_http_server, generate_latest

content_type = str('text/plain; version=0.0.4; charset=utf-8')
dhtDevice = dht_sensor.DHT22(board.D4)

def get_temperature_readings():
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity

    humidity = format(humidity, ".2f")
    temperature = format(temperature, ".2f")
    if all(v is not None for v in [humidity, temperature]):
        response = {"temperature": temperature, "humidity": humidity}
        return response
    else:
        time.sleep(0.2)
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        humidity = format(humidity, ".2f")
        temperature = format(temperature, ".2f")
        response = {"temperature": temperature, "humidity": humidity}
        return response

app = Flask(__name__)

current_humidity = Gauge(
        'current_humidity',
        'the current humidity percentage, this is a gauge as the value can increase or decrease',
        ['room']
)

current_temperature = Gauge(
        'current_temperature',
        'the current temperature in celsius, this is a gauge as the value can increase or decrease',
        ['room']
)

@app.route('/metrics')
def metrics():
    metrics = get_temperature_readings()
    print(metrics)
    current_humidity.labels('study').set(metrics['humidity'])
    current_temperature.labels('study').set(metrics['temperature'])
    return Response(generate_latest(), mimetype=content_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
