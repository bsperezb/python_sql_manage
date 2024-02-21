from fuzzywuzzy import process

def find_matching_tuple(tuples, target_name):
    # Lista para almacenar resultados de coincidencia
    matches = []

    # Itera sobre las tuplas y calcula la similitud con el nombre objetivo
    for tup in tuples:
        name = tup[1]
        similarity = process.extractOne(target_name, [name])[1]
        matches.append((tup, similarity))

    # Ordena las coincidencias por similitud descendente
    matches.sort(key=lambda x: x[1], reverse=True)

    # Retorna la tupla con mayor similitud y su valor de similitud
    return matches[0] if matches else None

def clean_string(input_string, words_to_remove):
    # Remove words from the array
    for word in words_to_remove:
        input_string = input_string.replace(word, '')

    # Remove commas
    input_string = input_string.replace(',', '')
    input_string = input_string.replace('.', '')
    input_string = input_string.strip()

    return input_string
# Ejemplo de uso
# data = [(1, 'AGUAS FRIAS', 507, None), (2, 'ALTAVISTA CENTRAL', 507, None), (2, 'ALTAVISTA CENTR', 507, None),(3, 'BARRO BLANCO', 507, None)]
# target_name = 'ALTAVISTA CENTRA'
#
# result = find_matching_tuple(data, target_name)
# print(result)
#
