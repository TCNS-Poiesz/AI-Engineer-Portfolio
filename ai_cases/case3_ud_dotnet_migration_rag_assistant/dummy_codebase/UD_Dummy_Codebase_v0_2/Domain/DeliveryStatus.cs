namespace UDDummy.Domain;

/// <summary>
/// Describes the lifecycle status of a delivery in the UD dummy model.
/// Delivered means the deliverer placed the delivery in the authorized space.
/// Received means the receiver retrieved it from the space.
/// </summary>
public enum DeliveryStatus
{
    Created,
    AssignedToLsp,
    AcceptedByLsp,
    Planned,
    SpaceMatched,
    AccessGranted,
    OutForDelivery,
    Delivered,
    Received,
    DeliveryFailed,
    DeliveryCancelled
}
