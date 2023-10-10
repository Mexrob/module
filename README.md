#Control de cambios

<h3> Agregar campos de factura en ticket de pos</h3>

1. En clase "PaymentScreen" agregamos metodo "_get_hks_vals" para extrar la informacion de la factura desde el js. pos_fel.js
2. En clase "PaymentScreen" sobreescribimos metodo "_finalizeValidation", despues de crear pedido extraemos los datos de la factura y guardamos en la cache de la orden de venta. pos_fel.js 
3. En clase "OrderReceipt" agregamos "hks_vals" para extraer los valores de la orden de venta previamente guardado. pos_fel.js
4. En account_move.py agregamos "get_hks_vals", esto regresa la lista de campos de la factura que nos interesan.
5. Modificamos pos_receipt.xml agregando el elemento "hks_values", dentro esta la lista de campos a renderizar.
6. Ajustamos manifest, modificamos 'point_of_sale.assets' los assets del punto de venta.

<h4>Modo de uso </h4>

1. Reiniciar servicio
2. Ejecutar accion "Actualizar lista de aplicaciones", dentro del modulo de aplicaciones, esto para asegurar que carguen los cambios del manifest
3. Actualizar modulo.