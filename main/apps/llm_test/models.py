from django.contrib.auth import get_user_model
from django.db.models import \
    CASCADE, ForeignKey, OneToOneField, CharField, DateTimeField, EmailField, \
    BooleanField, PositiveSmallIntegerField, Q, QuerySet, TextField
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from simple_history import register as register_history
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import UUID_Model
User = get_user_model()


__all__ = [
    'AccessLevel',
    'Org',
    'OrgUser',
    'OrgUserGroup',
    'OrgUserInOrgUserGroup',
    'OrgUserInvite',
    'OrgUserGroupInvite',
]


class AccessLevel(IntegerChoices):
    """ Access level for user in group """
    MEMBER  = 0, _('Member' )  # Can view the group
    MANAGER = 1, _('Manager')  # + add/remove members
    ADMIN   = 2, _('Admin'  )  # + add/remove managers and create/delete subgroups


class LLM_Test(UUID_Model):
    """ Organization """ 
    name        = CharField(max_length=64, null=False)
    is_active   = BooleanField(default=True)
    subdomain   = CharField(max_length=64, null=True, blank=True, unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class OrgUser(UUID_Model):
    """ User in Organization """ 
    org         = ForeignKey(Org , on_delete=CASCADE, related_name='org_users')
    user        = ForeignKey(User, on_delete=CASCADE, related_name='org_users')
    is_active   = BooleanField(default=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = (("org", "user"),)

    def __str__(self):
        return f"{self.user} in {self.org} (active: {self.is_active})"

    def get_groups(self, required_level: AccessLevel = AccessLevel.MEMBER):
        """ Get user groups according to the required access level """
        groups = OrgUserGroup.objects.filter(
            links_to_org_users__org_user=self,
            links_to_org_users__level__gte=required_level
        )
        ancestors_q   = Q()
        descendants_q = Q()
        for group in groups:
            # Member can view parents groups also
            if AccessLevel.MEMBER == required_level:
                ancestors_q |= Q(pk__in=group.get_ancestors())
            # Any level can view descendants
            descendants_q |= Q(pk__in=group.get_descendants())
        
        return OrgUserGroup.objects.filter(descendants_q | ancestors_q | Q(pk__in=groups))



class OrgUserGroup(UUID_Model, MPTTModel):
    """ Hierarchical groups in Organization """ 
    parent  = TreeForeignKey('self', on_delete=CASCADE, null=True , blank=True, related_name='children')
    org     = ForeignKey    (Org   , on_delete=CASCADE, null=False, blank=True, related_name='org_user_groups')
    name    = CharField     (max_length=32)
    desc    = TextField     (null=True, blank=True)

    class Meta:
        unique_together = (('parent', 'name'), )

    def __str__(self):
        return f"{self.org} :: {self.parent.name if self.parent else 'ROOT'} :: {self.name}"

# MPTTModel has conflict with HistoricalRecords, so we need to register it manually
register_history(OrgUserGroup)


class OrgUserInOrgUserGroup(UUID_Model):
    """ Org-User in Organization User Group """
    org_user_group  = ForeignKey(OrgUserGroup, on_delete=CASCADE, null=False, related_name='links_to_org_users')
    org_user        = ForeignKey(OrgUser     , on_delete=CASCADE, null=False, related_name='links_to_org_user_groups')
    level = PositiveSmallIntegerField(default=AccessLevel.MEMBER, choices=AccessLevel.choices)
    # access can be limited to certain time period, if it is not set, it is valid for all time
    start_from = DateTimeField(null=True, blank=True)
    end_to     = DateTimeField(null=True, blank=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.org_user_group} :: {self.org_user} :: {self.level}"

    class Meta:
        unique_together = (('org_user_group', 'org_user'), )


class OrgUserInvite(UUID_Model):
    """ Org-User Invite.  
        Use it only for users that are not in the org. 
    """
    org             = ForeignKey(Org, on_delete=CASCADE, related_name='org_user_invites')
    email           = EmailField()
    org_user        = OneToOneField(OrgUser, on_delete=CASCADE, null=True, blank=True, related_name='org_user_invite')
    is_active       = BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.org} :: {self.email} :: {'accepted' if self.org_user else 'pending'}"

    class Meta:
        unique_together = (('org', 'email'), )


class OrgUserGroupInvite(UUID_Model):
    """ Extra data for invite. User can be invited to multiple groups or none.  """
    invite          = ForeignKey(OrgUserInvite, on_delete=CASCADE, related_name='org_user_group_invites')
    org_user_group  = ForeignKey(OrgUserGroup,  on_delete=CASCADE, related_name='org_user_group_invites')
    level           = PositiveSmallIntegerField(default=AccessLevel.MEMBER, choices=AccessLevel.choices)
    
    history = HistoricalRecords()
    
    class Meta:
        unique_together = (('invite', 'org_user_group'), )
