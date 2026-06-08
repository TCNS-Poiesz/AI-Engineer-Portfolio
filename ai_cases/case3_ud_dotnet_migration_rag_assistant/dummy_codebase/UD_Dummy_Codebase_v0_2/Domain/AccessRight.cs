namespace UDDummy.Domain;

/// <summary>
/// Represents permission to open a smart lock. Receiver/owner access can be permanent.
/// Deliverer access is temporary and linked to one delivery.
/// </summary>
public class AccessRight
{
    public Guid AccessRightId { get; private set; }
    public Guid UserId { get; private set; }
    public Guid SmartLockId { get; private set; }
    public Guid? DeliveryId { get; private set; }
    public AccessRightType AccessRightType { get; private set; }
    public AccessRightStatus Status { get; private set; }
    public DateTime ValidFrom { get; private set; }
    public DateTime? ValidUntil { get; private set; }
    public bool IsPermanent { get; private set; }
    public DateTime? UsedAt { get; private set; }
    public DateTime? RevokedAt { get; private set; }

    private AccessRight(
        Guid userId,
        Guid smartLockId,
        Guid? deliveryId,
        AccessRightType accessRightType,
        DateTime validFrom,
        DateTime? validUntil,
        bool isPermanent)
    {
        AccessRightId = Guid.NewGuid();
        UserId = userId;
        SmartLockId = smartLockId;
        DeliveryId = deliveryId;
        AccessRightType = accessRightType;
        ValidFrom = validFrom;
        ValidUntil = validUntil;
        IsPermanent = isPermanent;
        Status = AccessRightStatus.Active;
    }

    public static AccessRight CreateOwnerPermanentAccess(Guid receiverUserId, Guid smartLockId)
    {
        return new AccessRight(
            receiverUserId,
            smartLockId,
            deliveryId: null,
            AccessRightType.OwnerPermanentAccess,
            DateTime.UtcNow,
            validUntil: null,
            isPermanent: true);
    }

    public static AccessRight CreateDelivererTemporaryAccess(
        Guid delivererUserId,
        Guid smartLockId,
        Guid deliveryId,
        DateTime validFrom,
        DateTime validUntil)
    {
        return new AccessRight(
            delivererUserId,
            smartLockId,
            deliveryId,
            AccessRightType.DelivererTemporaryAccess,
            validFrom,
            validUntil,
            isPermanent: false);
    }

    public bool IsValidAt(DateTime moment)
    {
        if (Status != AccessRightStatus.Active)
        {
            return false;
        }

        if (moment < ValidFrom)
        {
            return false;
        }

        if (!IsPermanent && ValidUntil.HasValue && moment > ValidUntil.Value)
        {
            return false;
        }

        return true;
    }

    public void MarkUsed()
    {
        UsedAt = DateTime.UtcNow;

        if (!IsPermanent)
        {
            Status = AccessRightStatus.Used;
        }
    }

    public void Revoke()
    {
        RevokedAt = DateTime.UtcNow;
        Status = AccessRightStatus.Revoked;
    }
}
