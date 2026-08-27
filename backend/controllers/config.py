class Config:
    SECRET_KEY = 'my_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECURITY_PASSWORD_SALT = "MY_PASS_SALT"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_AUTHENTICATION_SCHEME = ''

    CELERY = dict(
        broker_url="redis://localhost:6379/1",
        result_backend="redis://localhost:6379/2",
        task_ignore_result=True,
    )