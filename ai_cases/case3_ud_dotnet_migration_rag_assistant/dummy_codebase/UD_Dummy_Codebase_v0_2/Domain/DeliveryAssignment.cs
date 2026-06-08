namespace UDDummy.Domain;

/// <summary>
/// Links a delivery to an LSP, optionally to a deliverer, and optionally to a delivery space.
/// </summary>
public class DeliveryAssignment
{
    public Guid AssignmentId { get; private set; }
    public Guid DeliveryId { get; private set; }
    public Guid LspOrganisationId { get; private set; }
    public Guid? DelivererUserId { get; private set; }
    public Guid? AssignedSpaceId { get; private set; }
    public AssignmentStatus AssignmentStatus { get; private set; }
    public DateTime AssignedAt { get; private set; }

    public DeliveryAssignment(Guid deliveryId, Guid lspOrganisationId)
    {
        AssignmentId = Guid.NewGuid();
        DeliveryId = deliveryId;
        LspOrganisationId = lspOrganisationId;
        AssignmentStatus = AssignmentStatus.Pending;
        AssignedAt = DateTime.UtcNow;
    }

    public void Accept()
    {
        AssignmentStatus = AssignmentStatus.Accepted;
    }

    public void Plan(Guid delivererUserId, Guid assignedSpaceId)
    {
        DelivererUserId = delivererUserId;
        AssignedSpaceId = assignedSpaceId;
        AssignmentStatus = AssignmentStatus.Planned;
    }

    public void StartExecution()
    {
        AssignmentStatus = AssignmentStatus.InExecution;
    }

    public void Complete()
    {
        AssignmentStatus = AssignmentStatus.Completed;
    }

    public void Reject()
    {
        AssignmentStatus = AssignmentStatus.Rejected;
    }
}
