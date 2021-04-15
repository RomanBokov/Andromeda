"""
Модуль содержит класс Checker, который содержит методы для проверки карточки и КО.

:author: Andrei Ursaki.
"""
import allure


class Checker:

    @staticmethod
    @allure.step("Проверка карточки")
    def check_card(sensor_code_full, adapter, rf_name, sensor_info_dict=None, is_existent_sensor=True):
        """
        Метод для проверки создания карточки и подготовки данных для этого

        :param sensor_code_full: "полный" код датчика/объекта
        :param adapter: объект класса Adapter
        :param event_code: код события
        :param event_title: описание события
        :param sensor_info_dict: словарь с аттрибутами КО
        :param is_existent_sensor: присутствует ли датчик/объект в БД
        :return: словарь с ошибками см. https://gitlab.sphaera.ru/coordcom/testers-projects/coordcom-card-checker
        """
        # допустимая ошибка при проверка карточки
        case_index_comment_positive_error = "значения различаются в"
        # подготовка данных для отправки в CoordCom Card Checker
        card_data = {
            "CaseIndex1Name": "Пожары и задымления", "CaseIndex2Name": "Пожарные сигнализации",
            "CaseIndex3Name": "Андромеда"}
        if is_existent_sensor:
            card_data.update(
                {
                    "CaseIndexComment": f"Тревога на объекте {sensor_info_dict.get('caption')}. "
                                        f"телефон объекта {sensor_info_dict.get('phone1')} "
                                        f"наименование реагирующей организации {rf_name}",
                    "XCoordinate": float(sensor_info_dict.get("location_lat")),
                    "YCoordinate": float(sensor_info_dict.get("location_long")),
                    "MunicipalityName": sensor_info_dict.get("municipality_region"),
                    "CaseTypeArea": sensor_info_dict.get("case_type_area"),
                    "Notices": []})
        #   else:
        # card_data.update({
        #  "CaseIndexComment": "Тревога на объекте <Name> телефон объекта <Phone> наименование реагирующей организации <ReactionFirmName> Информация о датчике отсутствует в БД",
        # "Notices": [{"OrderNo": 1,
        #       "NoteText": f"В АПК «Безопасный город» поступил сигнал от системы ОКО по объекту, отсутствующему в БД. Код события = {event_code} - «{event_title}» в "}]})
        # выполняем проверку карточки
        card_check_result = adapter.check_card(sensor_code_full, card_data)
        if not card_check_result.get("error"):
            # получаем ошибки для поля CaseIndexComment
            case_index_comment = card_check_result.get("CaseIndexComment")
            if case_index_comment and case_index_comment.find(case_index_comment_positive_error) != -1:
                # если ошибка для поля CaseIndexComment допустима удаляем ее
                card_check_result.pop("CaseIndexComment")
        return card_check_result

    @staticmethod
    @allure.step("Проверка нотиса карточки")
    def check_notice(sensor_code_full, order_no, card_data, adapter, event_code, event_title, is_existent_sensor=True):
        # допустимая ошибка при проверка карточки
        case_index_comment_positive_error = "значения различаются в"
        # подготовка данных для отправки в CoordCom Card Checker
        card_data.pop("ExternalSystemReference")
        card_data.pop("CardCreated")
        notice_dict = {"OrderNo": order_no}
        if is_existent_sensor:
            notice_dict.update({
                "NoteText": f"Поступило сообщение об изменении статуса тревоги {TypeNumber} Объект отсутствует в БД. Обратитесь в службу Тех поддержки"})
        else:
            notice_dict.update({
                "NoteText": f"Время действия: <AlarmDateTime>Поступило общение об изменении статуса тревоги - <AlarmTypeName>Описание действия: <AlarmDescription>Исполнитель действия: <AlarmUserName>Объект отсутствует в БД. Обратитесь в службу Тех поддержки"})
        card_data.update({"Notices": [notice_dict]})
        # выполняем проверку карточки
        card_check_result = adapter.check_card(sensor_code_full, card_data)
        return card_check_result

    @staticmethod
    @allure.step("Проверка каcтомного объекта")
    def check_layer_object(sensor_code_full, adapter, event_type, ico, object_status):
        """
        Метод для проверки создания карточки и подготовки данных для этого

        :param sensor_code_full: "полный" код датчика/объекта
        :param adapter: объект класса Adapter
        :param event_code: код события
        :param event_title: описание события
        :return: словарь с ошибками см. https://gitlab.sphaera.ru/coordcom/testers-projects/coordcom-card-checker
        """
        # подготовка данных для отправки в CoordCom Card Checker
        custom_object_data = {"event_type": event_type}

        custom_object_data.update({"ico": ico})

        custom_object_data.update({"object_status": object_status})
        # выполняем проверку КО
        layer_object_check_result = adapter.check_co(sensor_code_full, custom_object_data,
                                                     header={"server": "10.100.122.5", "database": "LayerObjectRostov"})
        return layer_object_check_result
