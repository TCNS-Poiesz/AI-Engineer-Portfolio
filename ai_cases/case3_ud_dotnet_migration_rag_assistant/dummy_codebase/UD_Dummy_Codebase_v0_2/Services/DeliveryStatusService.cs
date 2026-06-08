using UDDummy.Domain;
using UDDummy.Infrastructure;

namespace UDDummy.Services;

/// <summary>
/// Handles delivery status changes after the execution phase.
/// Delivered and Received are intentionally separate:
/// Delivered = placed in box/space by deliverer.
/// Received = retrieved by receiver.
/// </summary>
public class DeliveryStatusService
{
    private readonly IDeliveryRepository _deliveryRepository;

    public DeliveryStatusService(IDeliveryRepository deliveryRepository)
    {
        _deliveryRepository = deliveryRepository;
    }

    public void MarkOutForDelivery(Guid deliveryId)
    {
        var delivery = GetDelivery(deliveryId);
        delivery.MarkOutForDelivery();
        _deliveryRepository.Save(delivery);
    }

    public void MarkDelivered(Guid deliveryId)
    {
        var delivery = GetDelivery(deliveryId);
        delivery.MarkDelivered();
        _deliveryRepository.Save(delivery);
    }

    public void MarkReceived(Guid deliveryId)
    {
        var delivery = GetDelivery(deliveryId);
        delivery.MarkReceived();
        _deliveryRepository.Save(delivery);
    }

    public void MarkFailed(Guid deliveryId, FailureReason reason)
    {
        var delivery = GetDelivery(deliveryId);
        delivery.Fail(reason);
        _deliveryRepository.Save(delivery);
    }

    public void MarkCancelled(Guid deliveryId, CancellationReason reason)
    {
        var delivery = GetDelivery(deliveryId);
        delivery.Cancel(reason);
        _deliveryRepository.Save(delivery);
    }

    private Delivery GetDelivery(Guid deliveryId)
    {
        return _deliveryRepository.GetById(deliveryId)
            ?? throw new InvalidOperationException("Delivery not found.");
    }
}
