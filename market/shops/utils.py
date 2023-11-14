def shop_preivew_directory_path(instance, filename: str) -> str:
    return "shops/shop_{pk}/{filename}".format(pk=instance.pk, filename=filename)
