original_string = "Hello, World!"

print(type(original_string))
# another way to endode the string:
# encoded_bytes = str.encode(original_string)
encoded_bytes = bytes.encode(original_string)

print(type(encoded_bytes))
print(encoded_bytes)

decoded_string = bytes.decode(encoded_bytes)

# Another way to decode:
# decoded_string = str.decode(encoded_bytes)

print(type(decoded_string))
print(decoded_string)
