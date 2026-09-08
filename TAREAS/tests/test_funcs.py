# tests/test_funcs.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from funcs import (
    sumatoria_positivos,
    es_palindromo,
    maximo_seguro,
    contar_palabras,
    filtrar_aprobados,
    normalizar_email,
    factorial,
    media,
)


# ── 1. sumatoria_positivos ────────────────────────────────────────────────────

@pytest.mark.parametrize("nums, esperado", [
    ([], 0),                          # lista vacía
    ([-3, -1, -10], 0),               # solo negativos
    ([-2, 3, -1, 4], 7),              # mixta
    ([1, 2, 3, 4], 10),               # solo positivos
    ([0, -5, 5], 5),                  # incluye cero (cuenta como no negativo)
])
def test_sumatoria_positivos(nums, esperado):
    assert sumatoria_positivos(nums) == esperado


# ── 2. es_palindromo ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("entrada, esperado", [
    ("ana",           True,  ),
    ("racecar",       True,  ),
    ("A man a plan a canal Panama", True),   # con espacios y mayúsculas
    ("",              True,  ),              # cadena vacía (caso borde)
    ("a",             True,  ),              # un solo carácter
    ("hola",          False, ),
    ("Python",        False, ),
    ("Anita lava la tina", True),
], ids=[
    "simple-palindromo",
    "racecar",
    "frase-con-espacios",
    "cadena-vacia",
    "un-caracter",
    "no-palindromo-hola",
    "no-palindromo-python",
    "frase-espanol",
])
def test_es_palindromo(entrada, esperado):
    assert es_palindromo(entrada) == esperado


# ── 3. maximo_seguro ──────────────────────────────────────────────────────────

def test_maximo_enteros():
    assert maximo_seguro([3, 1, 7, 2]) == 7

def test_maximo_un_elemento():
    assert maximo_seguro([42]) == 42

def test_maximo_negativos():
    assert maximo_seguro([-5, -1, -3]) == -1

def test_maximo_floats():
    assert maximo_seguro([1.5, 3.2, 2.8]) == 3.2

def test_maximo_lista_vacia():
    with pytest.raises(ValueError):
        maximo_seguro([])


# ── 4. contar_palabras ────────────────────────────────────────────────────────

def test_contar_texto_vacio():
    assert contar_palabras("") == {}

def test_contar_palabras_repetidas():
    assert contar_palabras("Hola hola") == {"hola": 2}

def test_contar_varias_palabras():
    resultado = contar_palabras("el gato y el perro")
    assert resultado["el"] == 2
    assert resultado["gato"] == 1
    assert resultado["perro"] == 1

def test_contar_una_palabra():
    assert contar_palabras("hola") == {"hola": 1}


# ── 5. filtrar_aprobados ──────────────────────────────────────────────────────

@pytest.mark.parametrize("pares, esperado", [
    ([("Ana", 7), ("Luis", 4), ("Mia", 5)], ["Ana", "Mia"]),   # mixto
    ([("Tom", 3), ("Eva", 2)],              []),                 # ninguno aprueba
    ([("Juan", 10), ("Rosa", 8)],           ["Juan", "Rosa"]),  # todos aprueban
    ([("Leo", 5)],                          ["Leo"]),            # exactamente 5
], ids=[
    "mixto",
    "nadie-aprueba",
    "todos-aprueban",
    "nota-exacta-cinco",
])
def test_filtrar_aprobados(pares, esperado):
    assert filtrar_aprobados(pares) == esperado

def test_filtrar_aprobados_orden():
    # verifica que el orden original se mantiene
    pares = [("C", 9), ("A", 6), ("B", 8)]
    assert filtrar_aprobados(pares) == ["C", "A", "B"]


# ── 6. normalizar_email ───────────────────────────────────────────────────────

def test_email_valido():
    assert normalizar_email("Usuario@Dominio.COM") == ("usuario", "dominio.com")

def test_email_ya_minusculas():
    assert normalizar_email("hola@mundo.es") == ("hola", "mundo.es")

def test_email_sin_arroba():
    with pytest.raises(ValueError):
        normalizar_email("correo-sin-arroba.com")

def test_email_dos_arrobas():
    with pytest.raises(ValueError):
        normalizar_email("a@b@c.com")


# ── 7. factorial ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, esperado", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
])
def test_factorial(n, esperado):
    assert factorial(n) == esperado

def test_factorial_negativo():
    with pytest.raises(ValueError):
        factorial(-1)


# ── 8. media ──────────────────────────────────────────────────────────────────

def test_media_enteros():
    assert media([1, 2, 3, 4, 5]) == pytest.approx(3.0)

def test_media_floats():
    assert media([1.5, 2.5]) == pytest.approx(2.0)

def test_media_un_elemento():
    assert media([7]) == pytest.approx(7.0)

def test_media_resultado_no_exacto():
    assert media([1, 2]) == pytest.approx(1.5)

def test_media_lista_vacia():
    with pytest.raises(ValueError):
        media([])