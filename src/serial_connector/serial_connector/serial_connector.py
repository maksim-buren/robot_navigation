import json

import serial

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SerialConnector(Node):
    def __init__(self):
        super().__init__('serial_test')
        self.serial = serial.Serial('/dev/ttyUSB0', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        self.subscription = self.create_subscription(
            String,
            'camera/info',
            self.send_data,
            10
        )
        self.subscription

    # Функция для захвата и публикации изображения
    def send_data(self, msg):
        info = json.loads(msg.data)
        objects = info['objects']
        print(objects)
        peron = any([obj == 'person' for obj in objects])
        if peron:
            data = b'$\100\0#'
            self.serial.write(data)
        else:
            data = b'$\0\0#'
            self.serial.write(data)


def main(args=None):
    # Инициализируем ROS
    rclpy.init(args=args)
    # Создаем объект нашей ноды
    serial_connector = SerialConnector()
    # Запускаем цикл обработки ROS
    rclpy.spin(serial_connector)


if __name__ == '__main__':
    main()
