namespace UDDummy.Domain;

/// <summary>
/// Represents a physical or logical place where a delivery can be left unattended.
/// </summary>
public class DeliverySpace
{
    public Guid SpaceId { get; private set; }
    public Guid OwnerUserId { get; private set; }
    public string LocationDescription { get; private set; }
    public SpaceType SpaceType { get; private set; }
    public int CapacityUnits { get; private set; }
    public bool IsAvailable { get; private set; }
    public Guid? LinkedSmartLockId { get; private set; }

    public DeliverySpace(Guid ownerUserId, string locationDescription, SpaceType spaceType, int capacityUnits)
    {
        SpaceId = Guid.NewGuid();
        OwnerUserId = ownerUserId;
        LocationDescription = locationDescription;
        SpaceType = spaceType;
        CapacityUnits = capacityUnits;
        IsAvailable = true;
    }

    public void LinkSmartLock(Guid smartLockId)
    {
        LinkedSmartLockId = smartLockId;
    }

    public void Reserve()
    {
        IsAvailable = false;
    }

    public void Release()
    {
        IsAvailable = true;
    }
}
