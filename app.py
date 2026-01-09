import adafruit_dht as dht_sensor
import adafruit_hcsr04 as sonar_sensor
import time
import board
from flask import Flask, Response
from prometheus_client import Counter, Gauge, start_http_server, generate_latest

content_type = str('text/plain; version=0.0.4; charset=utf-8')
dhtDevice = dht_sensor.DHT22(board.D4)
sonar = sonar_sensor.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

def get_sonar_readings():
    try:
        distance = sonar.distance
        distance = format(distance, ".3f")
        response = {"distance": distance}
        return response
    except:
        return {"distance": 0}

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

current_distance = Gauge(
        'current_distance',
        'the current distance in cm, tih is a gauge as the value can increase or decrease',
        ['room']
)

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
    distance = get_sonar_readings()
    metrics = metrics | distance
    print(metrics)
    current_humidity.labels('study').set(metrics['humidity'])
    current_temperature.labels('study').set(metrics['temperature'])
    current_distance.labels('study').set(metrics['distance'])
    return Response(generate_latest(), mimetype=content_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
