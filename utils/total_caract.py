import os

folder_path = './output'

def contar_caracteres(folder_path):
    """Contar la cantidad total de caracteres en todos los archivos .txt de una carpeta"""
    total_characters = 0
    for archive in os.listdir(folder_path):
        if archive.endswith(".txt"):
            archivo_path = os.path.join(folder_path, archive)
            with open(archivo_path, "r", encoding="utf-8") as f:
                contenido = f.read()
                total_characters += len(contenido)
    return total_characters

total_caracteres = contar_caracteres(folder_path)
print(f"Cantidad total de caracteres en los textos: {total_caracteres}")

# Verificar si se supera el umbral
umbral = 100000
if total_caracteres >= umbral:
    print(f"¡Superaste el umbral de {umbral} caracteres! 🚀")
else:
    print(f"No alcanzaste el umbral. Faltan {umbral - total_caracteres} caracteres.")


#print(total_caracteres)
#Cantidad total de caracteres en los textos: 136409 ¡Superaste el umbral de 100000 caracteres! 🚀136409