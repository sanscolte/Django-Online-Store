def user_preview_directory_path(instance, filename: str) -> str:
    return "accounts/user_{pk}/{filename}".format(pk=instance, filename=filename)
