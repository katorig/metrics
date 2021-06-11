from dynaconf import settings


def load_val_to_env(name, val):
    settings.name = val


if __name__ == '__main__':
    settings.TERADATA_PASSWORD = "xx"
    for i in settings:
        print(i)
    # print(settings.TERADATA_PASSWORD)
