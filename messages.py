"""
Модуль содержит класс AndromedaMessage, который содержит методы для создания сообщений.

:author: Bokov Roman.
"""


class AndromedaMessage:

    def __init__(self, AlarmGroupID=123121):
        self.AlarmGroupID = AlarmGroupID

    def get_event_msg(self, event_time, ObjectNumber, TypeNumber, sensor_info_dict) -> str:
        """
        Метод для получения сообщения о событии(Type = 2)

        :param event_time: время события
        :param ObjectNumber: код дотчика/объекта
        :param TypeNumber: код события
        :param sensor_info_dict: писок параметров из Db
        :return: сообщение для отправки
        """



        msg = str(f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <Envelope>
                        <Header>
                        <DateTime>{event_time}</DateTime>
                        <Number>222947</Number>
                        <Type>2</Type>
                        </Header>
                    <Event>
                <Description>Sobbitie</Description>
                <ObjectNumber>{ObjectNumber}</ObjectNumber>
                <AlarmGroupID>{self.AlarmGroupID}</AlarmGroupID>
                <DateTime>{event_time}</DateTime>
                <Code>ZZX</Code>
                <ChannelTypeNumber>8</ChannelTypeNumber>
                <ChannelNumber>2</ChannelNumber>
                <PartNumber>0</PartNumber>
                <ZoneUserNumber>3</ZoneUserNumber>
                <TypeNumber>{TypeNumber}</TypeNumber>
                <TypeName>status {TypeNumber}</TypeName>
                    </Event>
                    <Object>
                <ID>9AD0E758-1255-4C5D-A127-1D8669666C1D</ID>
                <Number>{ObjectNumber}</Number>
                <TypeName>{sensor_info_dict.get('type')}</TypeName>
                <Name>{sensor_info_dict.get('caption')}</Name>
                <Contract>+</Contract>
                <Password/>
                <Phone1>{sensor_info_dict.get('phone1')}</Phone1>
                <Phone2>{sensor_info_dict.get('phone2')}</Phone2>
                <Phone3>{sensor_info_dict.get('phone3')}</Phone3>
                <Address>{sensor_info_dict.get('object_adress')}</Address>
                <PoliceDepartment/>
                <Site/>
                <WeakSpots/>
                <ArmStateNumber>1</ArmStateNumber>
                <MakeDateTime>1899-12-30T00:00:00.000+03:00</MakeDateTime>
                <ActivateDateTime>{event_time}</ActivateDateTime>
                <ArmTypes>
                    <ArmType>
                        <Number>2</Number>
                    </ArmType>
                </ArmTypes>
                <DeviceTypeName>{sensor_info_dict.get('device_type')}</DeviceTypeName>
                <ReactionFirmName>{sensor_info_dict.get("caption")}</ReactionFirmName>
                <MakeFirmName/>
                <ServiceFirmName/>
                <Latitude>{sensor_info_dict.get("location_lat")}</Latitude>
                <Longitude>{sensor_info_dict.get("location_lon")}</Longitude>
                <CommentForOperator/>
                <CommentForGuard/>
                <CustomersComment/>
                <ChannelTypes/>
                <Customers>
                    <Customer>
                        <ID>1327</ID>
                        <CodeNumber>5448</CodeNumber>
                        <Title>zam A4h</Title>
                        <Name>Jrsana</Name>
                        <MobilePhone/>
                        <HomePhone>8-928-183-43-28</HomePhone>
                        <Address/>
                        <Comment/>
                    </Customer>
                </Customers>
                <Parts/>
                <Zones>
                    <Zone>
                        <ID>1237</ID>
                        <Number>1</Number>
                        <PartNumber>0</PartNumber>
                        <Name>P</Name>
                        <DeviceTypeName/>
                    </Zone>
                    <Zone>
                        <ID>1238</ID>
                        <Number>2</Number>
                        <PartNumber>0</PartNumber>
                        <Name>P</Name>
                        <DeviceTypeName/>
                    </Zone>
                    <Zone>
                        <ID>1239</ID>
                        <Number>3</Number>
                        <PartNumber>0</PartNumber>
                        <Name>P</Name>
                        <DeviceTypeName/>
                        </Zone>
                        </Zones>
                    </Object>
                    </Envelope>""")

        return msg
