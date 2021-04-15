"""
Модуль содержит класс BasicAdapter.

:author: Andrei Ursaki.
"""
import json

import xmltodict

from basic import db_config
from basic.basic_adapter import BasicAdapter
from config import Config
from select_AlarmID import AndromedaSqlHelper


class Adapter(BasicAdapter):
    #Выбираем Telemetry id из SphaeraTelemetryReference02.dbo.t_telemetry_system
    telemetry_system_id = 14

    def __init__(self, telemetry_system_id, endpoint, content_type):
        super().__init__(telemetry_system_id, endpoint, content_type)
        self.config_dict = self.get_config_dict()
        self.sh = AndromedaSqlHelper(telemetry_system_id, db_config.db_sensors_conn_122, db_config.db_layer_obj_conn_122)

    @staticmethod
    def get_config_dict():
        """
        Метод для чтения файла конфишурации

        :return: словарь в данными из файла конфигурации
        """
        # читаем файл конфигурации
        config_file = open(Config.config_path, "r", encoding='utf-8-sig')
        config_str = config_file.read()
        config_file.close()
        # преобразуем xml из файла конфигурации в словарь
        config_str = json.dumps(xmltodict.parse(config_str), ensure_ascii=False, indent=4)
        return json.loads(config_str)

    def get_andromeda_systems(self):
        """
        Метод для получания информации по системам (пультам)
        :return: словарь с информацией о системе в виде {SystemCode: Url}
        """
        systems = self.config_dict.get("configuration").get("sphaera.integration").get("systems").get("AndromedaSystem")
        systems= [systems] if isinstance(systems,dict) else systems
        systems_url_dict = {system.get("SystemCode"): system.get("Url") for system in systems}

        return systems_url_dict

    def get_system_url_for_sensor(self, sensor_code_full):
        """
        Метод для получания кода датчика/объекта и url системы по полному коду (с префиксом системы)

        :param sensor_code_full: код датчика/объекта с префиксом системы
        :return: код датчика/объекта и url системы
        """
        # получаем параметры пультов из файла конфигурации
        systems = self.get_andromeda_systems()
        # из "полного" кода датчика извлекаем код системы (пульта)
        system_code = sensor_code_full.split(':')[0]
        # из параметров пультов получаем Url для выбранной системы
        system_url = systems.get(system_code)
        print("\nВыбран объект с кодом: ", sensor_code_full)
        print(f"Выбрана система с SystemCode {int(sensor_code_full.split(':')[0])} и Url {system_url}")
        # извлекаем код датчика
        sensor_code = int(sensor_code_full.split(':')[1])
        return sensor_code, system_url
