# Импортируем необходимые библиотеки
import json

import rclpy
from rclpy.node import Node
from ultralytics import YOLO
from std_msgs.msg import String
import cv2
import time
import os
import glob


# Определяем класс CaptureCameraNode, который является ROS2-нодой для захвата изображений с камеры
class CaptureCameraNode(Node):
    def __init__(self):
        # Инициализируем родительский класс Node с именем 'capture_camera'
        super().__init__('capture_camera')

        # Создаем издателя для публикации текстовых сообщений
        self.text_publisher = self.create_publisher(String, 'camera/info', 10)

        # Инициализируем объект VideoCapture для захвата видео с камеры
        self.cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
        self.model = YOLO("yolov8n.pt")
        # Создаем таймер, который вызывает функцию capture_and_publish каждую секунду
        self.timer = self.create_timer(1.0, self.capture_and_publish)

    # Функция для захвата и публикации изображения
    def capture_and_publish(self):
        # Захватываем изображение с камеры
        ret, frame = self.cap.read()
        if ret:
            # Подготавливаем и публикуем текстовое сообщение с временем захвата изображения
            result = self.model.predict(frame)
            data = result[0].names
            objects = result[0].boxes.cls
            message = json.dumps({'objects': [data.get(int(obj)) for obj in objects]})
            msg = String()
            msg.data = message
            self.text_publisher.publish(msg)


def main(args=None):
    # Инициализируем ROS
    rclpy.init(args=args)
    # Создаем объект нашей ноды
    capture_camera = CaptureCameraNode()
    # Запускаем цикл обработки ROS
    rclpy.spin(capture_camera)


if __name__ == '__main__':
    main()