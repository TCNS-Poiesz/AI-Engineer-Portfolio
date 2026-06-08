using UDDummy.Domain;
using UDDummy.Infrastructure;

namespace UDDummy.Services;

/// <summary>
/// Grants permanent owner access and temporary deliverer access to smart locks.
/// </summary>
public class AccessControlService
{
    private readonly IAccessRightRepository _accessRightRepository;

    public AccessControlService(IAccessRightRepository accessRightRepository)
    {
        _accessRightRepository = accessRightRepository;
    }

    public AccessRight GrantOwnerPermanentAccess(Guid receiverUserId, Guid smartLockId)
    {
        var accessRight = AccessRight.CreateOwnerPermanentAccess(receiverUserId, smartLockId);
        _accessRightRepository.Save(accessRight);
        return accessRight;
    }

    public AccessRight GrantDelivererTemporaryAccess(
        Guid delivererUserId,
        Guid smartLockId,
        Guid deliveryId,
        DateTime validFrom,
        DateTime validUntil)
    {
        var accessRight = AccessRight.CreateDelivererTemporaryAccess(
            delivererUserId,
            smartLockId,
            deliveryId,
            validFrom,
            validUntil);

        _accessRightRepository.Save(accessRight);
        return accessRight;
    }
}
