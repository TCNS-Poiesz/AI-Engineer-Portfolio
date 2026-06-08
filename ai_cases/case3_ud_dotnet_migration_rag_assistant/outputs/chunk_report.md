# UD Dummy Codebase Chunk Report

This report shows the first RAG-ready chunks created from the dummy C# codebase.

Total chunks: 39

## Chunks by layer

- Domain: 28
- Infrastructure: 3
- Services: 8

## Chunk inventory

- `AccessRight_chunk_1` | Domain | AccessControl | `Domain\AccessRight.cs` | lines 1-45
- `AccessRight_chunk_2` | Domain | AccessControl | `Domain\AccessRight.cs` | lines 38-82
- `AccessRight_chunk_3` | Domain | AccessControl | `Domain\AccessRight.cs` | lines 75-105
- `AccessRightStatus_chunk_1` | Domain | AccessControl | `Domain\AccessRightStatus.cs` | lines 1-10
- `AccessRightType_chunk_1` | Domain | AccessControl | `Domain\AccessRightType.cs` | lines 1-10
- `Alert_chunk_1` | Domain | Alerts | `Domain\Alert.cs` | lines 1-38
- `AlertType_chunk_1` | Domain | Alerts | `Domain\AlertType.cs` | lines 1-13
- `AssignmentStatus_chunk_1` | Domain | General | `Domain\AssignmentStatus.cs` | lines 1-11
- `CancellationReason_chunk_1` | Domain | General | `Domain\CancellationReason.cs` | lines 1-15
- `Delivery_chunk_1` | Domain | Delivery | `Domain\Delivery.cs` | lines 1-45
- `Delivery_chunk_2` | Domain | Delivery | `Domain\Delivery.cs` | lines 38-82
- `Delivery_chunk_3` | Domain | Delivery | `Domain\Delivery.cs` | lines 75-99
- `DeliveryAssignment_chunk_1` | Domain | Delivery | `Domain\DeliveryAssignment.cs` | lines 1-45
- `DeliveryAssignment_chunk_2` | Domain | Delivery | `Domain\DeliveryAssignment.cs` | lines 38-51
- `DeliverySpace_chunk_1` | Domain | Delivery | `Domain\DeliverySpace.cs` | lines 1-40
- `DeliveryStatus_chunk_1` | Domain | Delivery | `Domain\DeliveryStatus.cs` | lines 1-21
- `FailureReason_chunk_1` | Domain | General | `Domain\FailureReason.cs` | lines 1-15
- `Organisation_chunk_1` | Domain | IdentityAndRoles | `Domain\Organisation.cs` | lines 1-25
- `OrganisationType_chunk_1` | Domain | IdentityAndRoles | `Domain\OrganisationType.cs` | lines 1-10
- `SmartBox_chunk_1` | Domain | DeliverySpace | `Domain\SmartBox.cs` | lines 1-45
- `SmartBox_chunk_2` | Domain | DeliverySpace | `Domain\SmartBox.cs` | lines 38-48
- `SmartBoxStatus_chunk_1` | Domain | DeliverySpace | `Domain\SmartBoxStatus.cs` | lines 1-9
- `SmartLock_chunk_1` | Domain | SmartLock | `Domain\SmartLock.cs` | lines 1-45
- `SmartLock_chunk_2` | Domain | SmartLock | `Domain\SmartLock.cs` | lines 38-48
- `SmartLockStatus_chunk_1` | Domain | SmartLock | `Domain\SmartLockStatus.cs` | lines 1-9
- `SpaceType_chunk_1` | Domain | DeliverySpace | `Domain\SpaceType.cs` | lines 1-9
- `User_chunk_1` | Domain | IdentityAndRoles | `Domain\User.cs` | lines 1-34
- `UserRole_chunk_1` | Domain | IdentityAndRoles | `Domain\UserRole.cs` | lines 1-12
- `LockProviderGateway_chunk_1` | Infrastructure | SmartLock | `Infrastructure\LockProviderGateway.cs` | lines 1-9
- `NotificationGateway_chunk_1` | Infrastructure | Alerts | `Infrastructure\NotificationGateway.cs` | lines 1-11
- `RepositoryInterfaces_chunk_1` | Infrastructure | General | `Infrastructure\RepositoryInterfaces.cs` | lines 1-29
- `AccessControlService_chunk_1` | Services | AccessControl | `Services\AccessControlService.cs` | lines 1-42
- `AlertService_chunk_1` | Services | Alerts | `Services\AlertService.cs` | lines 1-45
- `AlertService_chunk_2` | Services | Alerts | `Services\AlertService.cs` | lines 38-47
- `DeliveryAssignmentService_chunk_1` | Services | Delivery | `Services\DeliveryAssignmentService.cs` | lines 1-45
- `DeliveryAssignmentService_chunk_2` | Services | Delivery | `Services\DeliveryAssignmentService.cs` | lines 38-72
- `DeliveryStatusService_chunk_1` | Services | Delivery | `Services\DeliveryStatusService.cs` | lines 1-45
- `DeliveryStatusService_chunk_2` | Services | Delivery | `Services\DeliveryStatusService.cs` | lines 38-61
- `SpaceMatchingService_chunk_1` | Services | DeliverySpace | `Services\SpaceMatchingService.cs` | lines 1-31