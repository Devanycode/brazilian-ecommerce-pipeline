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

# Relación 

Orders (1) -> Order_items (N)

## Observaciones
- Un solo pedido puede contener varios producto.
- Cada fila corresponde a un producto dentro de un pedido.
- La tabla contiene el precio del producto.
- Contiene el valor del envío.
- Contiene la fecha límite de envío del vendedor.


-- 

#