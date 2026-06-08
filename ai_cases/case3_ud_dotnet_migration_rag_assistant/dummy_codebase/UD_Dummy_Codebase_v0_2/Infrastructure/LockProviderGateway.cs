namespace UDDummy.Infrastructure;

/// <summary>
/// Dummy gateway for communicating with an external smart-lock provider.
/// </summary>
public interface ILockProviderGateway
{
    bool OpenLock(Guid smartLockId, Guid userId);
}
