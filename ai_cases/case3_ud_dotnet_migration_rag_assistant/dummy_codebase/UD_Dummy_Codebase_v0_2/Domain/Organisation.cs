namespace UDDummy.Domain;

/// <summary>
/// Represents a company or operational party in the UD network, such as a shipper, LSP, buyer, or receiver organisation.
/// </summary>
public class Organisation
{
    public Guid OrganisationId { get; private set; }
    public string Name { get; private set; }
    public OrganisationType OrganisationType { get; private set; }
    public bool IsActive { get; private set; }

    public Organisation(string name, OrganisationType organisationType)
    {
        OrganisationId = Guid.NewGuid();
        Name = name;
        OrganisationType = organisationType;
        IsActive = true;
    }

    public void Deactivate()
    {
        IsActive = false;
    }
}
