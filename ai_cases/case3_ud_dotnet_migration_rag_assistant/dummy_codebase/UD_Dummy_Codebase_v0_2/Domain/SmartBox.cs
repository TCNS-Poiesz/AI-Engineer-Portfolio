namespace UDDummy.Domain;

/// <summary>
/// Represents a specific smart delivery box. It may be linked to a delivery space and a smart lock.
/// </summary>
public class SmartBox
{
    public Guid SmartBoxId { get; private set; }
    public Guid OwnerUserId { get; private set; }
    public string Location { get; private set; }
    public int CapacityUnits { get; private set; }
    public SmartBoxStatus CurrentAvailabilityStatus { get; private set; }
    public Guid? SmartLockId { get; private set; }

    public SmartBox(Guid ownerUserId, string location, int capacityUnits)
    {
        SmartBoxId = Guid.NewGuid();
        OwnerUserId = ownerUserId;
        Location = location;
        CapacityUnits = capacityUnits;
        CurrentAvailabilityStatus = SmartBoxStatus.Available;
    }

    public void LinkSmartLock(Guid smartLockId)
    {
        SmartLockId = smartLockId;
    }

    public void Reserve()
    {
        CurrentAvailabilityStatus = SmartBoxStatus.Reserved;
    }

    public void MarkOccupied()
    {
        CurrentAvailabilityStatus = SmartBoxStatus.Occupied;
    }

    public void MarkAvailable()
    {
        CurrentAvailabilityStatus = SmartBoxStatus.Available;
    }

    public void MarkOutOfService()
    {
        CurrentAvailabilityStatus = SmartBoxStatus.OutOfService;
    }
}
