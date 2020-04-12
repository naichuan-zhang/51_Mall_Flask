def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE") or "sqlite"
    driver = dbinfo.get("DRIVER") or "sqlite"
    username = dbinfo.get("USERNAME") or ""
    password = dbinfo.get("PASSWORD") or ""
    host = dbinfo.get("HOST") or ""
    port = dbinfo.get("PORT") or ""
    name = dbinfo.get("NAME") or ""

    return "{}+{}://{}:{}@{}:{}/{}" \
        .format(engine, driver, username,
                password, host, port, name)


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'naichuan'


class DevelopmentConfig(Config):
    DEBUG = True
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USERNAME": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "mall",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):
    TESTING = True
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USERNAME": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "mall",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USERNAME": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "mall",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USERNAME": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "mall",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
}
