def user_preview_directory_path(instance, filename: str) -> str:
    return "users/user_{pk}/{filename}".format(pk=instance.pk, filename=filename)
