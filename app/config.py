import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://caricature:password@localhost/caricature_shop"
    SQLALCHEMY_TRACK_MODIFICATIONS = False