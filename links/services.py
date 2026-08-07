def build_link_data(link):

    return {

        "id": link.id,
        "platform": link.get_platform_display(),
        "platform_name": link.platform_name,
        "label": link.label,
        "url": link.url,
        "display_order": link.display_order,

    }