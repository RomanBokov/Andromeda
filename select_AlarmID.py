from basic import db_config
from basic.sql_helper import SqlHelper
import re
import pyodbc

from basic import db_config


class AndromedaSqlHelper(SqlHelper):
    def __init__(self,*params):
        super().__init__(*params)

    def get_all_alarmid_with_open_card(self,sensorcode):
        """
        Метод для получения дентификаторов объектов, для которых есть открытая карточка.
        :param: sensorcode полный номер датчика
        :return: список идентификаторов объектов
        """
        alarm_id_list = []
        query = f"""select ExternalSystemReference from [cse_CaseExternalSystemReference_tab]
                    where ExternalSystemReference like '{self.telemetry_system_id}-<{sensorcode}>%'"""
        cursor = self.execute_query(self.omnidata_conn, query)
        for row in cursor.fetchall():
            alarm_id = re.findall(r">->>[0-9]+", row[0])[0][4:]
            alarm_id_list.append(alarm_id)
        return list(set(alarm_id_list))









