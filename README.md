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
## Instalación y uso

### 1. Clonar el repositorio
\`\`\`bash
git clone https://github.com/Devanycode/brazilian-ecommerce-pipeline.git
cd brazilian-ecommerce-pipeline
\`\`\`

### 2. Crear entorno virtual e instalar dependencias
\`\`\`bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

### 3. Descargar el dataset
Este proyecto usa el dataset público **Brazilian E-Commerce Public Dataset by Olist**:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Descarga el ZIP y coloca los siguientes archivos dentro de la carpeta `data/`:
- olist_customers_dataset.csv
- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_products_dataset.csv
- olist_order_payments_dataset.csv
- olist_order_reviews_dataset.csv
- olist_sellers_dataset.csv

### 4. Configurar variables de entorno
\`\`\`bash
cp .env.example .env
\`\`\`
Y completa tus credenciales de MySQL en `.env`.

### 5. Ejecutar el pipeline
\`\`\`ejecutar src
python main.py
\`\`\`


---
## Próximas mejoras

- Incorporar reportes analíticos con Matplotlib.
- Añadir visualizaciones directamente al README.
- Implementar pruebas automatizadas.
- Optimizar el pipeline para facilitar su reutilización con nuevos datasets.