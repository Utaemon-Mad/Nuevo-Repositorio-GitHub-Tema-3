nombre = 'Enzo'
edad = 0
alergias = ['Coco']
if edad < 18:
    print('Eres mayor de edad')
if alergias and alergias[0] == 'Coco':
    print('pobrecito')
mensaje = f'Hola, mi nombre es {nombre} tengo {edad} años y soy alérgico a {alergias[0]}'
print(mensaje)
