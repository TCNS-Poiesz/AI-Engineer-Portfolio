# UD Dummy Codebase - RAG-Style Answer

## Question

Where is temporary deliverer access granted?

## Short answer

The question appears to be about access control. The most relevant files are likely AccessControlService.cs and AccessRight.cs.

## Best matching source

- File: `Services\AccessControlService.cs`
- Layer: Services
- Domain area: AccessControl
- Lines: 1-42

## Evidence from retrieved code

### Evidence 1
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

### Evidence 2
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

### Evidence 3
- Similarity: 0.2210
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

### Evidence 4
- Similarity: 0.1996
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

### Evidence 5
- Similarity: 0.1422
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

## Interpretation

This answer is grounded only in the retrieved dummy codebase chunks. In a full RAG assistant, this retrieval step would be followed by an LLM that writes a more fluent explanation using these same retrieved sources.