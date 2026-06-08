# Retrieval Results

Query: Where is the LSP alert triggered?

## Result 1
- Score: 18
- File: `Services\AlertService.cs`
- Layer: Services
- Domain area: Alerts
- Lines: 1-45

```csharp
using UDDummy.Domain;
using UDDummy.Infrastructure;

namespace UDDummy.Services;

/// <summary>
/// Creates and sends alerts for important delivery workflow events.
/// </summary>
public class AlertService
{
    private readonly IAlertRepository _alertRepository;
    private readonly INotificationGateway _notificationGateway;

    public AlertService(IAlertRepository alertRepository, INotificationGateway notificationGateway)
    {
        _alertRepository = alertRepository;
        _notificationGateway = notificationGateway;
    }

    public Alert NotifyLspOfDeliveryAssignment(Guid lspOrganis
```

## Result 2
- Score: 16
- File: `Infrastructure\NotificationGateway.cs`
- Layer: Infrastructure
- Domain area: Alerts
- Lines: 1-11

```csharp
using UDDummy.Domain;

namespace UDDummy.Infrastructure;

/// <summary>
/// Dummy gateway for sending alerts. In a real system this could send email, SMS, push notifications, or in-app messages.
/// </summary>
public interface INotificationGateway
{
    void Send(Alert alert);
}
```

## Result 3
- Score: 14
- File: `Services\AlertService.cs`
- Layer: Services
- Domain area: Alerts
- Lines: 38-47

```csharp
recipientOrganisationId: null,
            deliveryId: deliveryId,
            AlertType.AccessGrantedToDeliverer,
            "Temporary access has been granted for this delivery.");

        _alertRepository.Save(alert);
        _notificationGateway.Send(alert);
        return alert;
    }
}
```

## Result 4
- Score: 13
- File: `Domain\Alert.cs`
- Layer: Domain
- Domain area: Alerts
- Lines: 1-38

```csharp
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
```

## Result 5
- Score: 13
- File: `Services\DeliveryAssignmentService.cs`
- Layer: Services
- Domain area: Delivery
- Lines: 1-45

```csharp
using UDDummy.Domain;
using UDDummy.Infrastructure;

namespace UDDummy.Services;

/// <summary>
/// Assigns deliveries to an LSP, matches delivery space, grants deliverer access, and triggers alerts.
/// This service is one of the main RAG targets for questions about delivery assignment.
/// </summary>
public class DeliveryAssignmentService
{
    private readonly IDeliveryRepository _deliveryRepository;
    private readonly SpaceMatchingService _spaceMatchingService;
    private readonly AccessControlService _accessControlService;
    private readonly AlertService _alertService;

    public De
```
