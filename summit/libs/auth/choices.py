class OrganizationChoices:
    PARTNER = 'Partner'
    FEDERAL_AGENCY = 'Federal Agency'

    ORG_TYPE = (
        (PARTNER, 'Partner'),
        (FEDERAL_AGENCY, 'Federal Agency')
    )
class UserChoices:

    VIEWER = 'VIEWER'
    USER = 'USER'
    ADMIN = 'ADMIN'

    ROLE = (
        (VIEWER, 'Viewer'),
        (USER, 'User'),
        (ADMIN, 'Admin'),
    )