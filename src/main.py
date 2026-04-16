from data.util.bytes_schema import BytesSchema
from data.util.typed_schema import TypedSchema


def main() -> None:
   schema = {"id": 1, "temperature": 20.0, "day": "tuesday"}
   typed_schema = TypedSchema(schema)
   bytes_schema = typed_schema.convert()
   print(bytes_schema)
   typed_schema = BytesSchema(bytes_schema).convert()
   print(typed_schema)
main()
