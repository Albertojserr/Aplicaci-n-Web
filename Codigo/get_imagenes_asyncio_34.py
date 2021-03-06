#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from os import sep
from sys import stderr

import asyncio

from http.client import HTTPConnection
from contextlib import closing
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from timeit import timeit


def wget(uri):
    """
    Devuelve el contenido indicado por una URI

    Parámetro:
    > uri (str, por ejemplo 'http://inspyration.org')

    Retorno:
    > contenido de un archivo (bytes, archivo de texto o binario)
    """
    # Análisis de la URI
    parsed = urlparse(uri)
    # apertura de la conexión
    with closing(HTTPConnection(parsed.netloc)) as conn:
        # Ruta en el servidor
        path = parsed.path
        if parsed.query:
            path += '?' + parsed.query
        # Envío de la consulta al servidor
        conn.request('GET', path)
        # Recuperación de la respuesta
        response = conn.getresponse()
        # Análisis de la respuesta
        if response.status != 200:
            # 200 = Ok, 3xx = redireccion, 4xx = error cliente, 5xx = error servidor
            return
        # Reenvío de la respuesta si todo está OK.
        return response.read()


@asyncio.coroutine
def download(uri):
    """
    Guarda en el disco duro un archivo indicado por una URI

    Parámetro:
    > uri (str, por ejemplo 'http://www.inspyration.org/logo.png')

    Retorno:
    > contenido de un archivo (bytes, archivo de texto o binario)
    """
    content = wget(uri)
    if content is None:
        return None
    with open(uri.split(sep)[-1], 'wb') as f:
        yield from f.write(content)
        return uri


def get_images_src_from_html(html_doc):
    """Recupera todos los contenidos de los atributos src de las etiquetas img"""
    soup = BeautifulSoup(html_doc, "html.parser")
    return (img.get('src') for img in soup.find_all('img'))


def get_uri_from_images_src(base_uri, images_src):
    """Devuelve una a una cada URI de imagen a descargar"""
    parsed_base = urlparse(base_uri)
    for src in images_src:
        parsed = urlparse(src)
        if parsed.netloc == '':
            path = parsed.path
            if parsed.query:
                path += '?' + parsed.query
            if path[0] != '/':
                if parsed_base.path == '/':
                    path = '/' + path
                else:
                    path = '/' + '/'.join(parsed_base.path.split('/')[:-1]) + '/' + path
            yield parsed_base.scheme + '://' + parsed_base.netloc + path
        else:
            yield parsed.geturl()


def get_images_uri(page_uri):
    #
    # Recuperación de las URI de todas las imágenes de una página
    #
    html = wget(page_uri)
    if not html:
        print("Error: La página web no se ha encontrado o analizado", sys.stderr)
        return None
    images_src_gen = get_images_src_from_html(html)
    images_uri_gen = get_uri_from_images_src(page_uri, images_src_gen)

    return images_uri_gen

def parse_html_page_and_get_all_images(page_uri):
    images_uri = get_images_uri(page_uri)
    #
    # Recuperación de las imágenes
    #
    for image_uri in images_uri:
        print('Téléchargement de %s' % image_uri)
        download(image_uri)


if __name__ == '__main__':
    print('--- Starting standard download ---')
    web_page_uri = 'http://www.formation-python.com/'
    print(timeit('parse_html_page_and_get_all_images(web_page_uri)',
                number=10,
                setup="from __main__ import parse_html_page_and_get_all_images, web_page_uri"))

# Tiempo evaluado: 4.75s

