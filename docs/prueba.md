# Modelo de Datos — Olist E-Commerce

## 1. Diagrama del Esquema

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   customers     │     │     orders      │     │  order_items    │
│   (Dimensión)   │◄────┤   (Hecho)       │◄────┤   (Hecho)       │
│                 │ 1:N │                 │ 1:N │                 │
│  customer_id (PK)│     │  order_id (PK)  │     │order_id+item(PK)│
│  customer_unique │     │  customer_id(FK)│     │  order_id (FK)  │
│  customer_state  │     │  order_status   │     │  product_id(FK) │
│  customer_city   │     │  order_purchase │     │  seller_id (FK) │
└─────────────────┘     │  order_delivered│     │  price          │
└─────────────────┘     │  freight_value  │
│               └─────────────────┘
│                        │
▼                        ▼
┌─────────────────┐     ┌─────────────────┐
│ order_payments  │     │    products     │
│   (Hecho)       │     │   (Dimensión)   │
│                 │     │                 │
│  order_id (FK)  │     │ product_id (PK) │
│  payment_type   │     │ product_category│
│  payment_value  │     │ product_name_len│
└─────────────────┘     └─────────────────┘
┌─────────────────┐     ┌─────────────────┐
│    sellers      │     │   geolocation   │
│   (Dimensión)   │     │   (Dimensión)   │
│                 │     │                 │
│  seller_id (PK) │     │ zip_code (PK)   │
│  seller_state   │     │ lat / lng       │
│  seller_city    │     │ city / state    │
└─────────────────┘     └─────────────────┘


## 2. Clasificación de Tablas

| Tabla | Tipo | Rol |
|-------|------|-----|
| `customers` | Dimensión | Quién compra |
| `orders` | Hecho | Qué se ordenó y cuándo |
| `order_items` | Hecho | Qué productos en cada orden |
| `order_payments` | Hecho | Cómo y cuánto se pagó |
| `products` | Dimensión | Qué se vende |
| `sellers` | Dimensión | Quién vende |
| `geolocation` | Dimensión | Dónde ocurre |

## 3. Diccionario de Datos (Tablas Principales)

### customers
| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| customer_id | string | `9ef432eb...` | ID único por compra |
| customer_unique_id | string | `7c396fd5...` | ID real del cliente |
| customer_zip_code | int | `14409` | Código postal |
| customer_city | string | `Sao Paulo` | Ciudad |
| customer_state | string | `SP` | Estado (sigla) |

### orders
| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| order_id | string | `e481f51b...` | ID único del pedido |
| customer_id | string | FK → customers | Cliente que compró |
| order_status | string | `delivered` | Estado: delivered, shipped... |
| order_purchase_timestamp | datetime | `2017-10-02 10:56:33` | Fecha de compra |
| order_delivered_timestamp | datetime | `2017-10-10 21:58:58` | Fecha de entrega |

### order_items
| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| order_id | string | FK → orders | Pedido al que pertenece |
| order_item_id | int | `1` | Secuencia del ítem en el pedido |
| product_id | string | FK → products | Producto vendido |
| seller_id | string | FK → sellers | Vendedor del producto |
| price | float | `29.99` | Precio del producto |
| freight_value | float | `8.72` | Costo de envío |

## 4. Métricas de Negocio Derivables

Con este modelo se pueden calcular:

| Métrica | Tablas necesarias | Granularidad |
|---------|-------------------|--------------|
| Ventas totales | order_items + orders | Mensual / Estado |
| Ticket promedio | order_items + orders | Por estado / Por cliente |
| Tiempo de entrega | orders | Por estado / Mensual |
| Productos más vendidos | order_items + products | Por categoría |
| Métodos de pago preferidos | order_payments | Global / Temporal |
| Concentración de vendedores | order_items + sellers | Por estado |
| Tasa de cancelación | orders | Mensual |

## 5. Notas de Modelado

- **Un cliente real** (`customer_unique_id`) puede tener múltiples `customer_id` (uno por compra).
- **Un pedido** puede tener múltiples ítems, múltiples pagos (ej: tarjeta + voucher) y múltiples envíos.
- **La PK de order_items es compuesta**: (`order_id`, `order_item_id`).
- **Geolocation** no tiene FK directa; se une por `zip_code` con customers y sellers.