using UDDummy.Domain;
using UDDummy.Infrastructure;

namespace UDDummy.Services;

/// <summary>
/// Finds an available delivery space for a receiver and reserves it for the delivery.
/// </summary>
public class SpaceMatchingService
{
    private readonly IDeliverySpaceRepository _deliverySpaceRepository;

    public SpaceMatchingService(IDeliverySpaceRepository deliverySpaceRepository)
    {
        _deliverySpaceRepository = deliverySpaceRepository;
    }

    public DeliverySpace MatchAndReserveSpace(Guid receiverUserId)
    {
        var space = _deliverySpaceRepository.FindAvailableSpaceForReceiver(receiverUserId);

        if (space == null)
        {
            throw new InvalidOperationException("No available delivery space found for receiver.");
        }

        space.Reserve();
        _deliverySpaceRepository.Save(space);
        return space;
    }
}
