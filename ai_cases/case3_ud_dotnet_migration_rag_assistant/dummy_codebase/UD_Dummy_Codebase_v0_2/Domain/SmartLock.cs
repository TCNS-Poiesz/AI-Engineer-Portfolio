namespace UDDummy.Domain;

/// <summary>
/// Represents the digital lock that protects a delivery space or smart box.
/// </summary>
public class SmartLock
{
    public Guid SmartLockId { get; private set; }
    public string ProviderName { get; private set; }
    public string ExternalLockReference { get; private set; }
    public Guid? LinkedSpaceId { get; private set; }
    public SmartLockStatus LockStatus { get; private set; }
    public DateTime? LastOpenedAt { get; private set; }

    public SmartLock(string providerName, string externalLockReference)
    {
        SmartLockId = Guid.NewGuid();
        ProviderName = providerName;
        ExternalLockReference = externalLockReference;
        LockStatus = SmartLockStatus.Locked;
    }

    public void LinkToSpace(Guid spaceId)
    {
        LinkedSpaceId = spaceId;
    }

    public void MarkUnlocked()
    {
        LockStatus = SmartLockStatus.Unlocked;
        LastOpenedAt = DateTime.UtcNow;
    }

    public void MarkLocked()
    {
        LockStatus = SmartLockStatus.Locked;
    }

    public void MarkOffline()
    {
        LockStatus = SmartLockStatus.Offline;
    }

    public void MarkError()
    {
        LockStatus = SmartLockStatus.Error;
    }
}
