from unidecode import unidecode

def only_ascii(text: str):
	return unidecode(text).replace("'", "")
