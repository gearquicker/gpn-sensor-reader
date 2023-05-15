from mpu6050 import mpu6050
import serial
import time
import datetime
import requests

url = "http://146.185.240.141:8080/dataPack/put"

mpu = mpu6050(0x68)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()


def current_milli_time():
    return round(time.time() * 1000)


def read_mic():
    ser.write(b"get\n")
    time.sleep(0.001)
    if ser.in_waiting > 0:
        return ser.readline().decode('utf-8').rstrip()
    return -1.0


def send_data(data):
    start_time = data[0].get("time")
    end_time = data[-1].get("time")
    res = requests.post(url, json={"startTime": start_time, "endTime": end_time, "data": data})
    print(str(datetime.datetime.now()) + ":\t" + str(res))


counter = 0
data_list = []

while True:
    if counter > 20:
        send_data(data_list)
        counter = 0
        data_list.clear()

    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()

    data_map = {
        "time": current_milli_time(),
        "ax": accel_data['x'],
        "ay": accel_data['y'],
        "az": accel_data['z'],
        "gx": gyro_data['x'],
        "gy": gyro_data['y'],
        "gz": gyro_data['z'],
        "mic": read_mic()
    }
    data_list.append(data_map)

    time.sleep(1)
    counter += 1
