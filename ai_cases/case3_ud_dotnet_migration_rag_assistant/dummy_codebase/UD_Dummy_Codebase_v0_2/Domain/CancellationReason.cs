namespace UDDummy.Domain;

/// <summary>
/// Explains why a delivery was cancelled without cluttering the main delivery status flow.
/// </summary>
public enum CancellationReason
{
    ReceiverCancelled,
    ShipperCancelled,
    WrongDelivery,
    DeliveryDamaged,
    ReturnToShipper,
    OperationalException,
    Other
}
