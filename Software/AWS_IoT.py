import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import bme680
import csv
from datetime import datetime
import RPi.GPIO as GPIO

# Control Variables
AWS_SEND_CONTROL = True
SENSOR_READING_SAVE = True
LED_CONTROL = False
BURN_IN_TIME = 5
TIME_CONTROL = 1
AWS_TOPIC = "iot/topic"
ENDPOINT = "a1j3xj5kj0hu9b-ats.iot.us-east-1.amazonaws.com"

#a1j3xj5kj0hu9b-ats.iot.us-east-1.amazonaws.com

# Suppress GPIO warnings
GPIO.setwarnings(False)

# LED Setup
LED_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Initially turn off the LED



def write_to_csv(temperature, gas_resistance, humidity, air_quality):
    if SENSOR_READING_SAVE:
        with open('sensor_readings.csv', 'a', newline='') as csvfile:
            fieldnames = ['Temperature', 'Gas Resistance', 'Humidity', 'Air Quality', 'Date Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvfile.seek(0, 2)
            if csvfile.tell() == 0:
                writer.writeheader()
            current_datetime = datetime.now().strftime('%d/%m/%Y , %H:%M:%S')
            writer.writerow({
                'Temperature': temperature, 
                'Gas Resistance': gas_resistance, 
                'Humidity': humidity, 
                'Air Quality': air_quality,
                'Date Time': current_datetime
            })

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./certs/rootCA.pem', certfile='./certs/certificate.pem.crt', keyfile='./certs/private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect(ENDPOINT, 8883, 60)

def calibrate_sensor():
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except (RuntimeError, IOError):
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

    start_time = time.time()
    curr_time = time.time()
    burn_in_time = BURN_IN_TIME
    burn_in_data = []

    print('Starting gas resistance burn-in data collection for 5 mins\n')
    burn_in_time_remaining = burn_in_time
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            minutes, seconds = divmod(burn_in_time_remaining, 60)
            print('Burn-in time remaining: {:02d}:{:02d}'.format(int(minutes), int(seconds)))
            burn_in_time_remaining -= 1
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0
    hum_baseline = 40.0
    hum_weighting = 0.25

    print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(gas_baseline, hum_baseline))

    return sensor, gas_baseline, hum_baseline, hum_weighting

def publishData(txt, sensor, gas_baseline, hum_baseline, hum_weighting):
    print(txt)
    while True:
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            hum = sensor.data.humidity
            temp = sensor.data.temperature
            gas_offset = gas_baseline - gas
            hum_offset = hum - hum_baseline
            if hum_offset > 0:
                hum_score = (100 - hum_baseline - hum_offset)
                hum_score /= (100 - hum_baseline)
                hum_score *= (hum_weighting * 100)
            else:
                hum_score = (hum_baseline + hum_offset)
                hum_score /= hum_baseline
                hum_score *= (hum_weighting * 100)
            if gas_offset > 0:
                gas_score = (gas / gas_baseline)
                gas_score *= (100 - (hum_weighting * 100))
            else:
                gas_score = 100 - (hum_weighting * 100)
            air_quality_score = hum_score + gas_score
            print('Temperature: {0:.2f} C, Gas: {1:.2f} Ohms, Humidity: {2:.2f} %RH, Air Quality: {3:.2f}'.format(temp, gas, hum, air_quality_score))
            
            if AWS_SEND_CONTROL:
                client.publish(AWS_TOPIC, payload=json.dumps({
                    "temperature": int(temp),
                    "humidity": int(hum),
                    "air_quality": int(air_quality_score),
                    "device_id":"sensor_1"
#                     "air_quality": int(air_quality_score)
                }), qos=0, retain=False)
                
                if LED_CONTROL:
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    
            if SENSOR_READING_SAVE:
                write_to_csv(temp, int(gas), int(hum), int(air_quality_score))
                    
            time.sleep(TIME_CONTROL)

def main():
    sensor, gas_baseline, hum_baseline, hum_weighting = calibrate_sensor()

    _thread.start_new_thread(publishData, ("Sending sensor data to AWS IoT...", sensor, gas_baseline, hum_baseline, hum_weighting))

    client.loop_forever()

    GPIO.cleanup()

if __name__ == "__main__":
    main()
