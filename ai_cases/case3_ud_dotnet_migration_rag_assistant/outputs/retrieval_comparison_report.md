# UD Dummy Codebase - Retrieval Comparison Report

This report compares two retrieval methods over the UD dummy C# codebase:

- Keyword / rule-based retrieval
- Vector-style TF-IDF retrieval

The purpose is to understand how different retrieval methods find relevant code chunks before moving to a full LangChain/vector-store RAG setup.

---

## Query

Where is delivery assignment handled?

## Keyword / rule-based retrieval

### Keyword result 1
- Score: 30
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

### Keyword result 2
- Score: 28
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
        delivery.Grant
```

### Keyword result 3
- Score: 27
- File: `Domain\DeliveryAssignment.cs`
- Layer: Domain
- Domain area: Delivery
- Lines: 1-45

```csharp
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

    public DeliveryAssignmen
```

## Vector-style TF-IDF retrieval

### Vector result 1
- Similarity: 0.2911
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

### Vector result 2
- Similarity: 0.1373
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

    public DeliveryAssignmentService(
        IDeliveryRepository deliveryRepository,
        SpaceMatchingServic
```

### Vector result 3
- Similarity: 0.0662
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

## Quick interpretation

Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. In a full RAG system, both approaches can be combined with real embeddings.

---

## Query

Where is temporary deliverer access granted?

## Keyword / rule-based retrieval

### Keyword result 1
- Score: 26
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 1-45

```csharp
namespace UDDummy.Domain;

/// <summary>
/// Represents permission to open a smart lock. Receiver/owner access can be permanent.
/// Deliverer access is temporary and linked to one delivery.
/// </summary>
public class AccessRight
{
    public Guid AccessRightId { get; private set; }
    public Guid UserId { get; private set; }
    public Guid SmartLockId { get; private set; }
    public Guid? DeliveryId { get; private set; }
    public AccessRightType AccessRightType { get; private set; }
    public AccessRightStatus Status { get; private set; }
    public DateTime ValidFrom { get; private se
```

### Keyword result 2
- Score: 26
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 38-82

```csharp
Status = AccessRightStatus.Active;
    }

    public static AccessRight CreateOwnerPermanentAccess(Guid receiverUserId, Guid smartLockId)
    {
        return new AccessRight(
            receiverUserId,
            smartLockId,
            deliveryId: null,
            AccessRightType.OwnerPermanentAccess,
            DateTime.UtcNow,
            validUntil: null,
            isPermanent: true);
    }

    public static AccessRight CreateDelivererTemporaryAccess(
        Guid delivererUserId,
        Guid smartLockId,
        Guid deliveryId,
        DateTime validFrom,
        DateTi
```

### Keyword result 3
- Score: 22
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 75-105

```csharp
}

        if (moment < ValidFrom)
        {
            return false;
        }

        if (!IsPermanent && ValidUntil.HasValue && moment > ValidUntil.Value)
        {
            return false;
        }

        return true;
    }

    public void MarkUsed()
    {
        UsedAt = DateTime.UtcNow;

        if (!IsPermanent)
        {
            Status = AccessRightStatus.Used;
        }
    }

    public void Revoke()
    {
        RevokedAt = DateTime.UtcNow;
        Status = AccessRightStatus.Revoked;
    }
}
```

## Vector-style TF-IDF retrieval

### Vector result 1
- Similarity: 0.2979
- File: `Services\AccessControlService.cs`
- Layer: Services
- Domain area: AccessControl
- Lines: 1-42

```csharp
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
        return ac
```

### Vector result 2
- Similarity: 0.2295
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 38-82

```csharp
Status = AccessRightStatus.Active;
    }

    public static AccessRight CreateOwnerPermanentAccess(Guid receiverUserId, Guid smartLockId)
    {
        return new AccessRight(
            receiverUserId,
            smartLockId,
            deliveryId: null,
            AccessRightType.OwnerPermanentAccess,
            DateTime.UtcNow,
            validUntil: null,
            isPermanent: true);
    }

    public static AccessRight CreateDelivererTemporaryAccess(
        Guid delivererUserId,
        Guid smartLockId,
        Guid deliveryId,
        DateTime validFrom,
        DateTime validUntil)
    {
        return new AccessRight(
            delivererUserId,
            smartL
```

### Vector result 3
- Similarity: 0.221
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 1-45

```csharp
namespace UDDummy.Domain;

/// <summary>
/// Represents permission to open a smart lock. Receiver/owner access can be permanent.
/// Deliverer access is temporary and linked to one delivery.
/// </summary>
public class AccessRight
{
    public Guid AccessRightId { get; private set; }
    public Guid UserId { get; private set; }
    public Guid SmartLockId { get; private set; }
    public Guid? DeliveryId { get; private set; }
    public AccessRightType AccessRightType { get; private set; }
    public AccessRightStatus Status { get; private set; }
    public DateTime ValidFrom { get; private set; }
    public DateTime? ValidUntil { get; private set; }
    public bool IsPermanent { get; privat
```

## Quick interpretation

Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. In a full RAG system, both approaches can be combined with real embeddings.

---

## Query

Where does a delivery become Received?

## Keyword / rule-based retrieval

### Keyword result 1
- Score: 21
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

    public void MarkOutForDelivery(Guid deliver
```

### Keyword result 2
- Score: 21
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
        return _deliveryRepository.GetById(del
```

### Keyword result 3
- Score: 19
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

## Vector-style TF-IDF retrieval

### Vector result 1
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

### Vector result 2
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

### Vector result 3
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

## Quick interpretation

Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. In a full RAG system, both approaches can be combined with real embeddings.

---

## Query

Where is the LSP alert triggered?

## Keyword / rule-based retrieval

### Keyword result 1
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

### Keyword result 2
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

### Keyword result 3
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

## Vector-style TF-IDF retrieval

### Vector result 1
- Similarity: 0.2767
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

    public Alert NotifyLspOfDeliveryAssignment(Guid lspOrganisationId, Guid deliveryId)
    {
        var alert = new Alert(
            recipientUserId: null,
```

### Vector result 2
- Similarity: 0.1964
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

### Vector result 3
- Similarity: 0.1271
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
        Guid? recipientUserId,
        Guid? recipientOrganisationId,
        Guid? deliveryId,
```

## Quick interpretation

Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. In a full RAG system, both approaches can be combined with real embeddings.

---

## Query

Which files relate to smart-lock access?

## Keyword / rule-based retrieval

### Keyword result 1
- Score: 24
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 1-45

```csharp
namespace UDDummy.Domain;

/// <summary>
/// Represents permission to open a smart lock. Receiver/owner access can be permanent.
/// Deliverer access is temporary and linked to one delivery.
/// </summary>
public class AccessRight
{
    public Guid AccessRightId { get; private set; }
    public Guid UserId { get; private set; }
    public Guid SmartLockId { get; private set; }
    public Guid? DeliveryId { get; private set; }
    public AccessRightType AccessRightType { get; private set; }
    public AccessRightStatus Status { get; private set; }
    public DateTime ValidFrom { get; private se
```

### Keyword result 2
- Score: 23
- File: `Domain\SmartLock.cs`
- Layer: Domain
- Domain area: SmartLock
- Lines: 1-45

```csharp
namespace UDDummy.Domain;

/// <summary>
/// Represents the digital lock that protects a delivery space or smart box.
/// </summary>
public class SmartLock
{
    public Guid SmartLockId { get; private set; }
    public string ProviderName { get; private set; }
    public string ExternalLockReference { get; private set; }
    public Guid? LinkedSpaceId { get; private set; }
    public SmartLockStatus LockStatus { get; private set; }
    public DateTime? LastOpenedAt { get; private set; }

    public SmartLock(string providerName, string externalLockReference)
    {
        SmartLockId = Guid.Ne
```

### Keyword result 3
- Score: 22
- File: `Domain\AccessRight.cs`
- Layer: Domain
- Domain area: AccessControl
- Lines: 38-82

```csharp
Status = AccessRightStatus.Active;
    }

    public static AccessRight CreateOwnerPermanentAccess(Guid receiverUserId, Guid smartLockId)
    {
        return new AccessRight(
            receiverUserId,
            smartLockId,
            deliveryId: null,
            AccessRightType.OwnerPermanentAccess,
            DateTime.UtcNow,
            validUntil: null,
            isPermanent: true);
    }

    public static AccessRight CreateDelivererTemporaryAccess(
        Guid delivererUserId,
        Guid smartLockId,
        Guid deliveryId,
        DateTime validFrom,
        DateTi
```

## Vector-style TF-IDF retrieval

### Vector result 1
- Similarity: 0.2062
- File: `Services\AccessControlService.cs`
- Layer: Services
- Domain area: AccessControl
- Lines: 1-42

```csharp
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
        return ac
```

### Vector result 2
- Similarity: 0.1467
- File: `Infrastructure\LockProviderGateway.cs`
- Layer: Infrastructure
- Domain area: SmartLock
- Lines: 1-9

```csharp
namespace UDDummy.Infrastructure;

/// <summary>
/// Dummy gateway for communicating with an external smart-lock provider.
/// </summary>
public interface ILockProviderGateway
{
    bool OpenLock(Guid smartLockId, Guid userId);
}
```

### Vector result 3
- Similarity: 0.1316
- File: `Domain\SmartLock.cs`
- Layer: Domain
- Domain area: SmartLock
- Lines: 38-48

```csharp
public void MarkOffline()
    {
        LockStatus = SmartLockStatus.Offline;
    }

    public void MarkError()
    {
        LockStatus = SmartLockStatus.Error;
    }
}
```

## Quick interpretation

Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. In a full RAG system, both approaches can be combined with real embeddings.

---

## Query

Which files would be relevant for a .NET version migration?

## Keyword / rule-based retrieval

### Keyword result 1
- Score: 13
- File: `Infrastructure\RepositoryInterfaces.cs`
- Layer: Infrastructure
- Domain area: General
- Lines: 1-29

```csharp
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
```

### Keyword result 2
- Score: 11
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

### Keyword result 3
- Score: 11
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

## Vector-style TF-IDF retrieval

### Vector result 1
- Similarity: 0.1216
- File: `Infrastructure\RepositoryInterfaces.cs`
- Layer: Infrastructure
- Domain area: General
- Lines: 1-29

```csharp
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
    void Save(Alert al
```

### Vector result 2
- Similarity: 0.05
- File: `Services\SpaceMatchingService.cs`
- Layer: Services
- Domain area: DeliverySpace
- Lines: 1-31

```csharp
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
            throw new InvalidOperat
```

### Vector result 3
- Similarity: 0.0359
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

## Quick interpretation

Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. In a full RAG system, both approaches can be combined with real embeddings.
