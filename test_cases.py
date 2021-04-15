"""
Модуль содержит класс TestCases, который выполняет основной алгоритм обработки.

:author: Bokov Roman.
"""
import random
import time
from datetime import datetime, timedelta

from andromeda_adapter import Adapter
from checker import Checker
from config import Config
from messages import AndromedaMessage
from andromeda_log_reader import AndromedaLogReader


class TestCases:
    wait_time = 10
    # примерная разница во времени между АРМом, на котором запущен тест и ИП
    delta = timedelta(minutes=1, seconds=5)
    # создаем объект класса адаптер
    adapter = Adapter(14, Config.end_point, Config.content_type)
    # словарь с иконками
    ico_dict = {"alarm": '\\\\coordcom.local\\filegroup\\Icons\\LayerObjects\\andromeda_alarmset_icon.png',
                "default": '\\\\coordcom.local\\filegroup\\Icons\\LayerObjects\\andromeda_default_icon.png',
                "disable": '\\\\coordcom.local\\filegroup\\Icons\\LayerObjects\\andromeda_malfunction_icon.png'
                }

    def get_correct_sensor(self, sensors):
        """
        Метод для получения случайного объекта/датчика 44 пульта(пока заглушка)

        :param sensors: список объектов/датчиков
        :return: случайный объект/датчик в названии которого нет двойных кавычек
        """
        is_sensor_caption_correct = False
        while not is_sensor_caption_correct:
            # выбираем случайный
            sensor_code_full = random.choice(sensors)
            # получаем словарь в аттрибутами КО
            sensor_info_dict = self.adapter.sh.get_sensor_attributes(sensor_code_full)
            # проверяем чтобы регион был 44, иначе невозможно будет прочитать лог
            if sensor_info_dict:
                if sensor_info_dict.get("caption").find("\"") == -1:
                    is_sensor_caption_correct = True
            else:
                is_sensor_caption_correct = True
        return sensor_code_full, sensor_info_dict

    def get_check_open_card(self, sensors, sensor_code_full):
        """
        Метод для проверки открытой карточки

        :param sensors: список объектов/датчиков
        :sensor_code_full: полный номер датчика
        :return: True/False
        """
        if sensors in sensor_code_full:
            print("По датчику " + sensors + " создана карточка")
            check_return_rezalt = True
        else:
            print("По датчику " + sensors + " не создана карточка")
            check_return_rezalt = False
        return check_return_rezalt

    def prepare_data_and_send_msg(self, sensors, event_iso_time, message_id):
        """
        Метод для подготовки данных и отправки сообщения в адаптер

        :param sensors: cписок датчиков/объектов
        :param events: список событий
        :param event_iso_time: время в iso формате
        :param message_id: номер сообщения для око
        :return: код датчика, его атрибуты, выбранное событие
        """
        # выбираем случайный
        sensor_code_full, sensor_info_dict = self.get_correct_sensor(sensors)
        print("Аттрибуты объекта:")
        for attribute in sensor_info_dict.items():
            print(attribute)
        # получаем код датчика и url системы
        sensor_code, system_url = self.adapter.get_system_url_for_sensor(sensor_code_full)

        # получаем сообщение на основе подготовленных данных
        adromeda_message = AndromedaMessage(message_id)
        msg = adromeda_message.get_event_msg(event_iso_time, sensor_code, 1)
        # отправляем сообщение в адаптер
        self.adapter.r.send(msg, andromeda_url=system_url, print_msg=True)
        return sensor_code_full, sensor_info_dict

    def get_alarm_groupid(self,state,sensor_code_full):
        if state == 1:
            AlarmGroupID = random.choice(self.adapter.sh.get_all_alarmid_with_open_card(sensor_code_full))
        else:
            AlarmGroupID = random.randint(100000, 999999)
        return AlarmGroupID

    def get_attribute_custom_object(self,event_type,sensors_check):
        event_type1 = 'status ' + str(event_type)
        # на основе подготовленных данных проверяем изменение аттрибутов КО
        if sensors_check and event_type1 != 'status 3':
            ico = self.ico_dict.get("alarm")
            object_status = 'Исправен'
        if sensors_check and event_type1 == 'status 3':
            ico = self.ico_dict.get("alarm")
            object_status = 'Неисправен'
        if event_type1 == 'status 3' and not sensors_check:
            ico = self.ico_dict.get("disable")
            object_status = 'Неисправен'
        if event_type1 != 'status 3' and not sensors_check and event_type1 != 'status 1':
            ico = self.ico_dict.get("default")
            object_status = 'Исправен'
            return event_type1,ico,object_status

    def case_all(self, event_type, state):
        """
        Тесткейс для случая Тревога. Объект есть в БД. Нет карточки КК в статусе «Открыта»
        """
        errors = {}
        # получаем список объектов/датчиков, для которых нет открытых карточек в КК
        sensors = self.adapter.get_sensors(state)
        system_number_list = list(self.adapter.get_andromeda_systems().keys())
        # Проверка на датчик сущетвующий в бд
        if state == 1:
            sensors_all_t_statmen = self.adapter.get_sensors(0)
            sensors_open_card = [sensor for sensor in sensors if sensor.split(':')[0] in system_number_list]
            sensors = list(set(sensors_open_card) & set(sensors_all_t_statmen))
        else:
            sensors = [sensor for sensor in sensors if sensor.split(':')[0] in system_number_list]
        # выбираем случайный
        sensor_code_full, sensor_info_dict = self.get_correct_sensor(sensors)
        #      print("Аттрибуты объекта:")
        #       for attribute in sensor_info_dict.items():
        #            print(attribute)
        # получаем код датчика и url системы
        sensor_code, system_url = self.adapter.get_system_url_for_sensor(sensor_code_full)

        # получаем список объектов/датчиков, для которых нет открытых карточек в КК
        sensors_check_new_card = self.adapter.get_sensors(1)
        sensors_check = self.get_check_open_card(sensor_code_full, sensors_check_new_card)

        # фиксируем текущее время
        event_dt = datetime.now()
        # преобразуем время в iso формат
        event_iso_time = event_dt.isoformat(timespec='seconds')

        #Если первое сообщение то берем случайный номер ,  если повторное выбираем из списка существующих
        AlarmGroupID = self.get_alarm_groupid(state,sensor_code_full)


        # получаем сообщение на основе подготовленных данных
        Andromeda_message = AndromedaMessage(AlarmGroupID)
        msg = Andromeda_message.get_event_msg(event_iso_time, sensor_code, event_type, sensor_info_dict)

        # отправляем сообщение в адаптер
        andromeda_header = {'AndromedaSystemUrl': system_url}
        self.adapter.r.send(msg, header=andromeda_header, print_msg=True)
        # пауза выполнения, чтобы быть уверенными что адаптер успел все сделать
        time.sleep(self.wait_time)

        # на основе подготовленных данных проверяем создание карточки
        # card_check_result = Checker.check_card(sensor_code_full, self.adapter, sensor_info_dict)
        # получаем список объектов/датчиков, для которых нет открытых карточек в КК
        sensors_check_new_card = self.adapter.get_sensors(1)
        sensors_check = self.get_check_open_card(sensor_code_full, sensors_check_new_card)
        # подготавливаем данные для сравнения
        event_type1,ico,object_status = self.get_attribute_custom_object(event_type,sensors_check)
        #сравниваем данные
        layer_object_check_result = Checker.check_layer_object(sensor_code_full, self.adapter, event_type1,
                                                               ico, object_status)
        # print(
        #     'Результат сравнения:' + 'Датчик обновился корректно' if layer_object_check_result is None else 'Ошибка значений в поле' + str(
        #        layer_object_check_result))
        assert not layer_object_check_result, 'Ошибка значений в поле' + str(layer_object_check_result)
