import pymysql
import serial
import time
from datetime import datetime


def serial_to_db():
    timeout = 10
    db = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-1afa3931-jatin8200240603-5614.h.aivencloud.com",
        password="AVNS_VzhdCGLVyQxhZNlI7GO",
        read_timeout=timeout,
        port=11147,
        user="avnadmin",
        write_timeout=timeout,
    )
    cursor = db.cursor()

    # Connect to Arduino Serial Port
    ser = serial.Serial('COM7', 9600)  # Make sure COM7 is correct
    time.sleep(1)

    print("Listening to Sensor Data from COM7...")

    try:
        while True:
            line = ser.readline().decode().strip()
            print("Data from sensors: ",ser.readline())
            if not line:
                continue

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if "IRSensorValue:" in line:
                print("data: ",line)

            if "Smoke Sensor Value: " in line:
                value = line.split(":")[1].strip()
                cursor.execute("INSERT INTO AGRICULTURE_APP_smokesensor (ppm, timestamp) VALUES (%s, %s)",
                               (value, current_time))
                print(f"[Inserted] Smoke: {value} | {current_time}")

            elif "Fire Sensor Value: " in line:
                value = line.split(":")[1].strip()
                cursor.execute("INSERT INTO AGRICULTURE_APP_firelevelsensor (level, timestamp) VALUES (%s, %s)",
                               (value, current_time))
                print(f"[Inserted] Fire: {value} | {current_time}")

            elif "Water Level Sensor Value: " in line:
                value = line.split(":")[1].strip()
                cursor.execute("INSERT INTO AGRICULTURE_APP_waterlevelsensor (level, timestamp) VALUES (%s, %s)",
                               (value, current_time))
                print(f"[Inserted] Water Level: {value} | {current_time}")

            elif "Soil Moisture Sensor Value: " in line:
                value = line.split(":")[1].strip()
                cursor.execute("INSERT INTO AGRICULTURE_APP_soilmoisturesensor (moisture_percent, timestamp) VALUES (%s, %s)",
                               (value, current_time))
                print(f"[Inserted] Soil Moisture: {value} | {current_time}")

            elif "IR Sensor Value: " in line:
                value = line.split(":")[1].strip()
                print("IR sensor: ",value)
                cursor.execute("INSERT INTO AGRICULTURE_APP_irsensor (value, timestamp) VALUES (%s, %s)",
                               (value, current_time))
                print(f"[Inserted] IR: {value} | {current_time}")

            db.commit()
            time.sleep(1)

    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        db.close()
        ser.close()
