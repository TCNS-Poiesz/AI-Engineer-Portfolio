namespace UDDummy.Domain;

/// <summary>
/// Represents a person who logs into the UD system and acts on behalf of an organisation.
/// </summary>
public class User
{
    public Guid UserId { get; private set; }
    public string FullName { get; private set; }
    public string Email { get; private set; }
    public Guid OrganisationId { get; private set; }
    public List<UserRole> Roles { get; private set; }
    public bool IsActive { get; private set; }

    public User(string fullName, string email, Guid organisationId, IEnumerable<UserRole> roles)
    {
        UserId = Guid.NewGuid();
        FullName = fullName;
        Email = email;
        OrganisationId = organisationId;
        Roles = roles.ToList();
        IsActive = true;
    }

    public bool HasRole(UserRole role)
    {
        return Roles.Contains(role);
    }

    public void Deactivate()
    {
        IsActive = false;
    }
}
