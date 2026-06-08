namespace UDDummy.Domain;

/// <summary>
/// Central object in the UD flow. A delivery moves from creation through assignment,
/// space matching, access granting, delivery, and final receiver retrieval.
/// </summary>
public class Delivery
{
    public Guid DeliveryId { get; private set; }
    public string ReferenceNumber { get; private set; }
    public Guid ShipperOrganisationId { get; private set; }
    public Guid? LspOrganisationId { get; private set; }
    public Guid ReceiverUserId { get; private set; }
    public string DeliveryAddress { get; private set; }
    public DateTime RequestedDeliveryWindowStart { get; private set; }
    public DateTime RequestedDeliveryWindowEnd { get; private set; }
    public DeliveryStatus CurrentStatus { get; private set; }
    public Guid? AssignedSpaceId { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime? DeliveredAt { get; private set; }
    public DateTime? ReceivedAt { get; private set; }
    public CancellationReason? CancellationReason { get; private set; }
    public FailureReason? FailureReason { get; private set; }

    public Delivery(
        string referenceNumber,
        Guid shipperOrganisationId,
        Guid receiverUserId,
        string deliveryAddress,
        DateTime requestedDeliveryWindowStart,
        DateTime requestedDeliveryWindowEnd)
    {
        DeliveryId = Guid.NewGuid();
        ReferenceNumber = referenceNumber;
        ShipperOrganisationId = shipperOrganisationId;
        ReceiverUserId = receiverUserId;
        DeliveryAddress = deliveryAddress;
        RequestedDeliveryWindowStart = requestedDeliveryWindowStart;
        RequestedDeliveryWindowEnd = requestedDeliveryWindowEnd;
        CurrentStatus = DeliveryStatus.Created;
        CreatedAt = DateTime.UtcNow;
    }

    public void AssignToLsp(Guid lspOrganisationId)
    {
        LspOrganisationId = lspOrganisationId;
        CurrentStatus = DeliveryStatus.AssignedToLsp;
    }

    public void MarkAcceptedByLsp()
    {
        CurrentStatus = DeliveryStatus.AcceptedByLsp;
    }

    public void MarkPlanned()
    {
        CurrentStatus = DeliveryStatus.Planned;
    }

    public void MatchToSpace(Guid spaceId)
    {
        AssignedSpaceId = spaceId;
        CurrentStatus = DeliveryStatus.SpaceMatched;
    }

    public void GrantAccess()
    {
        CurrentStatus = DeliveryStatus.AccessGranted;
    }

    public void MarkOutForDelivery()
    {
        CurrentStatus = DeliveryStatus.OutForDelivery;
    }

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
