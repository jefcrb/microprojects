def string_to_long(str):
    b = str.encode('utf-8')
    return int.from_bytes(b, byteorder='big')

print(string_to_long("test"))
