using UDDummy.Domain;

namespace UDDummy.Infrastructure;

/// <summary>
/// Minimal repository interfaces for the dummy model. In a real system these would connect to a database.
/// For the RAG prototype, they show which objects services need to read and update.
/// </summary>
public interface IDeliveryRepository
{
    Delivery? GetById(Guid deliveryId);
    void Save(Delivery delivery);
}

public interface IDeliverySpaceRepository
{
    DeliverySpace? FindAvailableSpaceForReceiver(Guid receiverUserId);
    void Save(DeliverySpace deliverySpace);
}

public interface IAccessRightRepository
{
    void Save(AccessRight accessRight);
}

public interface IAlertRepository
{
    void Save(Alert alert);
}
