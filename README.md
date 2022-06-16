# python_architectures

We are building an order allocation system.

SKU: product identifier, 
Customers place Orders
An Order is identified by Order Reference.
An Order can contain multiple Order lines.
An Order line has an SKU and it's Quantity.

Batches are ordered by the Purchasing Department
A Batch has a unique-id called the reference, and sku, and the quantity


We need to allocate Order Lines to Batches.
When we allocated X units of stock to a batch, the available quantity is reduced by X.


Order Lines cannot be allocated to Batches that have lesser quantity of that SKU.
We cannot allocated the same Order Line twice.

Batches have an ETA if they are currently shipping, or are in stock.
We allocate to Warehouse Stock, and then only to Shipment Stock.
We allocate Shipment Batches with the earliest ETA.
