namespace UDDummy.Domain;

/// <summary>
/// Explains why a delivery failed operationally.
/// </summary>
public enum FailureReason
{
    SmartLockOffline,
    AccessDenied,
    BoxUnavailable,
    AddressMismatch,
    DeliveryDamaged,
    DelivererCouldNotComplete,
    Other
}
