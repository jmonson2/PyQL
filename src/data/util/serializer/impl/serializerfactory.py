from typing import Any

from data.util.serializer.impl.floatserializer import FloatSerializer
from data.util.serializer.impl.integerpacker import IntegerSerializer
from data.util.serializer.impl.stringpacker import StringSerializer
from data.util.serializer.serializer import Serializer


class SerializerFactory:
    
    @staticmethod
    def get_serializer(val: Any) -> Serializer:
            match val:
                case int():
                    return IntegerSerializer()
                case float():
                    return FloatSerializer()
                case str():
                    return StringSerializer()

            raise ValueError("Invalid data type")



