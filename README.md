# Brazilian E-commerce Pipeline

## Descripción

Este proyecto implementa un pipeline de integración de datos utilizando **Python** y **Pandas** sobre el conjunto de datos público de **Olist Brazilian E-commerce**.

El objetivo es consolidar la información distribuida en múltiples tablas relacionales en una única **tabla analítica**, lista para realizar análisis exploratorios, construir visualizaciones y generar indicadores de negocio.

Durante el proceso se aplican validaciones de cardinalidad mediante `pandas.merge(validate=...)`, garantizando que las relaciones entre las tablas respeten el modelo de datos original y ayudando a detectar inconsistencias durante la integración.

## Objetivos

* Integrar la información del dataset de Olist en una tabla analítica centralizada.
* Aplicar buenas prácticas de organización y modularización del código.
* Validar las relaciones entre tablas durante el proceso de integración utilizando `pandas.merge(validate=...)`.
* Documentar el modelo de datos y el flujo del pipeline mediante diagramas técnicos.
* Preparar una base de datos lista para posteriores análisis y visualizaciones.

## Dataset

El proyecto utiliza el conjunto de datos **Brazilian E-commerce Public Dataset by Olist**, que contiene información sobre pedidos realizados entre 2016 y 2018 en la plataforma de comercio electrónico Olist.

Las tablas empleadas en este proyecto incluyen:

* `customers`
* `orders`
* `order_items`
* `products`
* `order_payments`
* `order_reviews`
* `sellers`

Cada una de ellas se integra progresivamente para construir una tabla analítica única.

---

## Próximas mejoras

- Incorporar reportes analíticos con Matplotlib.
- Añadir visualizaciones directamente al README.
- Implementar pruebas automatizadas.
- Optimizar el pipeline para facilitar su reutilización con nuevos datasets.