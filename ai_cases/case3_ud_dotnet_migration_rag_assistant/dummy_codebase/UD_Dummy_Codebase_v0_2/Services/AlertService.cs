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
            recipientOrganisationId: lspOrganisationId,
            deliveryId: deliveryId,
            AlertType.DeliveryAssignedToLsp,
            "A new delivery has been assigned to your LSP organisation.");

        _alertRepository.Save(alert);
        _notificationGateway.Send(alert);
        return alert;
    }

    public Alert NotifyDelivererAccessGranted(Guid delivererUserId, Guid deliveryId)
    {
        var alert = new Alert(
            recipientUserId: delivererUserId,
            recipientOrganisationId: null,
            deliveryId: deliveryId,
            AlertType.AccessGrantedToDeliverer,
            "Temporary access has been granted for this delivery.");

        _alertRepository.Save(alert);
        _notificationGateway.Send(alert);
        return alert;
    }
}
