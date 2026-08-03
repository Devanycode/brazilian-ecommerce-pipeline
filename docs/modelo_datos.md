# Modelo de Datos - Olist

---

# Customers

## Descripción

Contiene la información de los clientes.

## Llave primaria (PK)

customer_id

## Llaves foráneas (FK)

Ninguna.

## Relaciones

Customers (1)
    │
    └────────────► Orders (N)
                  mediante customer_id

## Observaciones

- `customer_unique_id` identifica al cliente real.
- `customer_id` identifica al cliente dentro del contexto de una compra.
- Un mismo `customer_unique_id` puede aparecer asociado a varios `customer_id`.


---

# Orders

## Descripción

Contiene la información de cada pedido realizado.

## Llave primaria (PK)

order_id

## Llaves foráneas (FK)

customer_id → Customers.customer_id

## Relaciones

Customers (1)
    │
    └────────────► Orders (N)
                  mediante customer_id

## Observaciones

- Cada pedido pertenece a un único cliente.
- Un cliente puede realizar varios pedidos.
- La tabla almacena estados y fechas del pedido.


---

# Order_items

## Descripción

Contiene los items(productos) incluidos de cada pedido.

## ¿Qué representa una fila?

un item individual perteneciente a un pedido 

## Llave primaria (PK)

Llave compuesta: (order_id + order_item_id)

## Llave Foránea (FK)

order_id   ->  Orders.order_id

## Relación 

Orders (1) -> Order_items (N)

## Observaciones
- Un solo pedido puede contener varios producto.
- Cada fila corresponde a un producto dentro de un pedido.
- La tabla contiene el precio del producto.
- Contiene el valor del envío.
- Contiene la fecha límite de envío del vendedor.


-- 

# Products

## Descripción 
Contiene la información de los productos 

## ¿Qué representa una fila?
La descripción de un producto 

## Llave primaria (PK)
product_id 

## Relación
order_items (N) -> Products (1)

## Observaciones 
- Contiene el nombre de la categoría, se puede analizar las más vendidas
- Tiene la información de las dimensiones del producto
- Tiene el nomre y la descripción del producto


---

# Order_payments

## Descripción 
Contiene la información del proceso de pago de un pedido

## ¿Qué representa una fila?
El proceso de pago de un pedido

## Llave primaria (PK)
Llave_compuesta: (order_id + payment_sequential)

## Llave foránea (FK)
order_id -> Orders.order_id

## Relación 
Orders (1) -> Order_payments (N)

## Descripción
- Contiene la categoría del producto.
- Tiene dimensiones físicas (peso, largo, alto, ancho).
- Contiene la información del medio de pago 
- Hay productos en `order_items` que no existen en esta tabla
