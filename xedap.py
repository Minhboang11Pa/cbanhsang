import time
import RPi.GPIO as GPIO
import threading

# Khai báo chân GPIO kết nối với cảm biến ánh sáng, cảm biến khoảng cách, và relay
LIGHT_SENSOR_PIN = 18
DISTANCE_SENSOR_PIN = 24
RELAY_PIN = 23

# Ngưỡng độ sáng để quyết định gửi xe
LIGHT_THRESHOLD = 500  # Tuỳ chỉnh ngưỡng độ sáng tùy ý
DISTANCE_THRESHOLD = 20  # Khoảng cách dưới đây sẽ được coi là có xe

class LightSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)

    def measure_light_intensity(self):
        return GPIO.input(LIGHT_SENSOR_PIN) == GPIO.LOW

class DistanceSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DISTANCE_SENSOR_PIN, GPIO.IN)

    def measure_distance(self):
        # Giả lập đo khoảng cách (có thể thay thế bằng cảm biến khoảng cách thực tế)
        # Ở đây, chúng ta giả định khoảng cách lớn hơn ngưỡng là không có xe
        return GPIO.input(DISTANCE_SENSOR_PIN) == GPIO.LOW

class ParkingLot:
    def __init__(self):
        self.available_spots = 10
        self.lock = threading.Lock()

    def check_available_spots(self):
        with self.lock:
            return self.available_spots

    def occupy_spot(self):
        with self.lock:
            if self.available_spots > 0:
                self.available_spots -= 1
                return True
            else:
                return False

    def release_spot(self):
        with self.lock:
            self.available_spots += 1

class ParkingSystem:
    def __init__(self, light_sensor, distance_sensor, parking_lot):
        self.light_sensor = light_sensor
        self.distance_sensor = distance_sensor
        self.parking_lot = parking_lot

        GPIO.setup(RELAY_PIN, GPIO.OUT)
        self.relay_lock = threading.Lock()

    def toggle_relay(self, state):
        with self.relay_lock:
            GPIO.output(RELAY_PIN, state)

    def process_parking(self):
        while True:
            light_intensity = self.light_sensor.measure_light_intensity()
            distance = self.distance_sensor.measure_distance()

            if light_intensity and distance:
                if self.parking_lot.check_available_spots():
                    print("Đang gửi xe vào chỗ đỗ...")
                    if self.parking_lot.occupy_spot():
                        self.toggle_relay(GPIO.HIGH)  # Bật relay để mở cổng gửi xe
                        time.sleep(3)  # Đợi 3 giây để cho xe vào chỗ đỗ
                        self.toggle_relay(GPIO.LOW)  # Tắt relay sau khi đỗ xe
                        print("Xe đã được đỗ vào chỗ.")
                    else:
                        print("Không có chỗ đỗ trống.")
                else:
                    print("Không có chỗ đỗ trống.")
            else:
                print("Độ sáng đủ hoặc khoảng cách quá gần, không gửi xe.")

            time.sleep(5)

    def run(self):
        parking_thread = threading.Thread(target=self.process_parking)
        parking_thread.start()
        parking_thread.join()

if __name__ == "__main__":
    light_sensor = LightSensor()
    distance_sensor = DistanceSensor()
    parking_lot = ParkingLot()
    parking_system = ParkingSystem(light_sensor, distance_sensor, parking_lot)
    parking_system.run()
