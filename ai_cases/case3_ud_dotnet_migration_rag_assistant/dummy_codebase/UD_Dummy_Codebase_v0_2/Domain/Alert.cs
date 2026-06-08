namespace UDDummy.Domain;

/// <summary>
/// Represents a system message or notification triggered by delivery workflow events.
/// </summary>
public class Alert
{
    public Guid AlertId { get; private set; }
    public Guid? RecipientUserId { get; private set; }
    public Guid? RecipientOrganisationId { get; private set; }
    public Guid? DeliveryId { get; private set; }
    public AlertType AlertType { get; private set; }
    public string Message { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public bool WasRead { get; private set; }

    public Alert(
        Guid? recipientUserId,
        Guid? recipientOrganisationId,
        Guid? deliveryId,
        AlertType alertType,
        string message)
    {
        AlertId = Guid.NewGuid();
        RecipientUserId = recipientUserId;
        RecipientOrganisationId = recipientOrganisationId;
        DeliveryId = deliveryId;
        AlertType = alertType;
        Message = message;
        CreatedAt = DateTime.UtcNow;
        WasRead = false;
    }

    public void MarkRead()
    {
        WasRead = true;
    }
}
