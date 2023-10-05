import time
import RPi.GPIO as GPIO

# Khai báo chân GPIO kết nối với cảm biến ánh sáng và relay điều khiển cổng gửi xe
LIGHT_SENSOR_PIN = 18
RELAY_PIN = 23

class LightSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)

    def measure_light_intensity(self):
        # Đọc giá trị từ cảm biến ánh sáng (ví dụ: giá trị HIGH/LOW)
        # Giả sử độ sáng cao khi giá trị LOW và ngược lại
        return GPIO.input(LIGHT_SENSOR_PIN) == GPIO.LOW

class ParkingLot:
    def __init__(self):
        self.available_spots = 10

    def check_available_spots(self):
        return self.available_spots

    def occupy_spot(self):
        if self.available_spots > 0:
            self.available_spots -= 1
            return True
        else:
            return False

    def release_spot(self):
        self.available_spots += 1

class ParkingSystem:
    def __init__(self, light_sensor, parking_lot):
        self.light_sensor = light_sensor
        self.parking_lot = parking_lot

        # Khởi tạo chân GPIO cho relay
        GPIO.setup(RELAY_PIN, GPIO.OUT)

    def run(self):
        while True:
            self.light_sensor.measure_light_intensity()
            light_intensity = self.light_sensor.measure_light_intensity()

            # Kiểm tra độ sáng và quyết định tự động gửi xe hoặc không
            if light_intensity:
                if self.parking_lot.check_available_spots():
                    print("Đang gửi xe vào chỗ đỗ...")
                    if self.parking_lot.occupy_spot():
                        print("Xe đã được đỗ vào chỗ.")
                        # Bật relay để mở cổng gửi xe
                        GPIO.output(RELAY_PIN, GPIO.HIGH)
                        time.sleep(3)  # Đợi 3 giây để cho xe vào chỗ đỗ
                        # Tắt relay sau khi đỗ xe
                        GPIO.output(RELAY_PIN, GPIO.LOW)
                    else:
                        print("Không có chỗ đỗ trống.")
                else:
                    print("Không có chỗ đỗ trống.")
            else:
                print("Độ sáng đủ, không gửi xe.")

            time.sleep(5)

if __name__ == "__main__":
    light_sensor = LightSensor()
    parking_lot = ParkingLot()
    parking_system = ParkingSystem(light_sensor, parking_lot)
    parking_system.run()
