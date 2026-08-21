from profiles.services import get_relationship
from visibility.models import LinkVisibilityRule

## Link layout to be used for templates and API responsws
def build_link_data(link):

    return {
        "id": link.id,
        "platform": link.get_platform_display(),
        "platform_name": link.platform_name,
        "label": link.label,
        "url": link.url,
        "display_order": link.display_order,
    }

## Get the links that are visible per connectiom type
def get_visible_links(profile, viewer):
    ## profile owner can always see all their links
    relationship = get_relationship(
        viewer,
        profile.user,
    )

    if relationship == "owner":
        return profile.links.all()

    ## other viewers only see links matching relationship type
    visible_link_ids = LinkVisibilityRule.objects.filter(
        owner = profile.user,
        visible_to__in=["public", relationship],
    ).values_list("link_id", flat=True,)

    return profile.links.filter(
        id__in = visible_link_ids,
    )