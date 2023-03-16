def encode_utf8(values):
	encoded_values = list()
	for value in values:
		encoded_values.append(unicode(value).encode('utf-8'))
	return encoded_values