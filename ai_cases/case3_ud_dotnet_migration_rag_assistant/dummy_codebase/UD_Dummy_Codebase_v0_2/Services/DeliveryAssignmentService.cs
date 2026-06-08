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
        SpaceMatchingService spaceMatchingService,
        AccessControlService accessControlService,
        AlertService alertService)
    {
        _deliveryRepository = deliveryRepository;
        _spaceMatchingService = spaceMatchingService;
        _accessControlService = accessControlService;
        _alertService = alertService;
    }

    public DeliveryAssignment AssignDeliveryToLsp(Guid deliveryId, Guid lspOrganisationId)
    {
        var delivery = _deliveryRepository.GetById(deliveryId)
            ?? throw new InvalidOperationException("Delivery not found.");

        delivery.AssignToLsp(lspOrganisationId);
        _deliveryRepository.Save(delivery);

        _alertService.NotifyLspOfDeliveryAssignment(lspOrganisationId, deliveryId);

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
        assignment.Plan(delivererUserId, space.SpaceId);

        _accessControlService.GrantDelivererTemporaryAccess(
            delivererUserId,
            smartLockId,
            delivery.DeliveryId,
            accessValidFrom,
            accessValidUntil);

        _alertService.NotifyDelivererAccessGranted(delivererUserId, delivery.DeliveryId);

        return assignment;
    }
}
