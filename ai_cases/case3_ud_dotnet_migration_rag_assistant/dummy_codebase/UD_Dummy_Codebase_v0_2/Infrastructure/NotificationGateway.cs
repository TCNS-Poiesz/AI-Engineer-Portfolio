using UDDummy.Domain;

namespace UDDummy.Infrastructure;

/// <summary>
/// Dummy gateway for sending alerts. In a real system this could send email, SMS, push notifications, or in-app messages.
/// </summary>
public interface INotificationGateway
{
    void Send(Alert alert);
}
