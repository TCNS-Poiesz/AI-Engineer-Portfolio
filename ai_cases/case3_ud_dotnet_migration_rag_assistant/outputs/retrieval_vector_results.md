# Vector Retrieval Results

Query: Where does a delivery become Received?

## Result 1
- Similarity: 0.1785
- File: `Services\DeliveryStatusService.cs`
- Layer: Services
- Domain area: Delivery
- Lines: 1-45

```csharp
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
```

## Result 2
- Similarity: 0.1703
- File: `Domain\DeliveryStatus.cs`
- Layer: Domain
- Domain area: Delivery
- Lines: 1-21

```csharp
namespace UDDummy.Domain;

/// <summary>
/// Describes the lifecycle status of a delivery in the UD dummy model.
/// Delivered means the deliverer placed the delivery in the authorized space.
/// Received means the receiver retrieved it from the space.
/// </summary>
public enum DeliveryStatus
{
    Created,
    AssignedToLsp,
    AcceptedByLsp,
    Planned,
    SpaceMatched,
    AccessGranted,
    OutForDelivery,
    Delivered,
    Received,
    DeliveryFailed,
    DeliveryCancelled
}
```

## Result 3
- Similarity: 0.1244
- File: `Domain\Delivery.cs`
- Layer: Domain
- Domain area: Delivery
- Lines: 75-99

```csharp
public void MarkDelivered()
    {
        DeliveredAt = DateTime.UtcNow;
        CurrentStatus = DeliveryStatus.Delivered;
    }

    public void MarkReceived()
    {
        ReceivedAt = DateTime.UtcNow;
        CurrentStatus = DeliveryStatus.Received;
    }

    public void Fail(FailureReason reason)
    {
        FailureReason = reason;
        CurrentStatus = DeliveryStatus.DeliveryFailed;
    }

    public void Cancel(CancellationReason reason)
    {
        CancellationReason = reason;
        CurrentStatus = DeliveryStatus.DeliveryCancelled;
    }
}
```

## Result 4
- Similarity: 0.0976
- File: `Services\DeliveryStatusService.cs`
- Layer: Services
- Domain area: Delivery
- Lines: 38-61

```csharp
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
```

## Result 5
- Similarity: 0.0558
- File: `Services\DeliveryAssignmentService.cs`
- Layer: Services
- Domain area: Delivery
- Lines: 38-72

```csharp
return new DeliveryAssignment(deliveryId, lspOrganisationId);
    }

    public DeliveryAssignment PlanDelivery(
        DeliveryAssignment assignment,
        Guid delivererUserId,
        Guid smartLockId,
        DateTime accessValidFrom,
        DateTime accessValidUntil)
    {
        var delivery = _deliveryRepository.GetById(assignment.DeliveryId)
            ?? throw new InvalidOperationException("Delivery not found.");

        var space = _spaceMatchingService.MatchAndReserveSpace(delivery.ReceiverUserId);

        delivery.MatchToSpace(space.SpaceId);
        delivery.GrantAccess();
        _deliveryRepository.Save(delivery);

        assignment.Accept();
        assignme
```
