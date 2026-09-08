def sumatoria_positivos(nums):
    total = 0
    for n in nums:
        if n >= 0:
            total += n
    return total


def es_palindromo(s: str) -> bool:
    s = s.lower().replace(' ', '')
    return s == s[::-1]


def maximo_seguro(nums):
    if not nums:
        raise ValueError('lista vacía')
    maximo = nums[0]
    for n in nums[1:]:
        if n > maximo:
            maximo = n
    return maximo


def contar_palabras(texto: str) -> dict:
    conteo = {}
    for palabra in texto.lower().split():
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


def filtrar_aprobados(pares):
    resultado = []
    for nombre, nota in pares:
        if nota >= 5:
            resultado.append(nombre)
    return resultado


def normalizar_email(email: str):
    if email.count('@') != 1:
        raise ValueError('email inválido')
    usuario, dominio = email.split('@')
    return usuario.lower(), dominio.lower()


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError('n negativo')
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def media(nums):
    if not nums:
        raise ValueError('lista vacía')
    return sum(nums) / len(nums)