# UD Dummy Codebase v0.2 - Business Process

This dummy codebase models a simplified Unattended Delivery flow.

## Successful flow

1. Shipper creates a delivery request.
2. Delivery is assigned to an LSP.
3. LSP accepts and plans the delivery.
4. System matches the delivery to an available delivery space.
5. System grants temporary access to the deliverer.
6. Deliverer goes out for delivery.
7. Deliverer places the delivery in the authorized delivery space.
8. Delivery status becomes Delivered.
9. Receiver later retrieves the delivery.
10. Delivery status becomes Received.

## Important status distinction

Delivered means the deliverer has successfully placed the delivery in the authorized box or space.

Received means the receiver has retrieved the delivery from the box or space.

## Access-right distinction

The receiver or owner of the delivery box/space has permanent owner access.

The deliverer receives temporary access for one delivery and one time window.
