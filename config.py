#coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#微信token
WX_TOKEN = '2vX79QF'

class Config:
    SECRET_KEY = 'hjkawhedoi'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'goodwriter@163.com'
    MAIL_PASSWORD = 'goodwriter111111'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Goodwriter]'
    FLASKY_MAIL_SENDER = 'Goodwriter Team <goodwriter@163.com>'

    DEBUG = True

    # DIALECT = 'mysql'
    # DRIVER = 'pymysql'
    # USERNAME = 'goodwriter'
    # PASSWORD = '11111111'
    # HOST = '101.132.133.202'
    # PORT = '3306'
    # DATABASE = 'goodwriter'
    # DB_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
    # SQLALCHEMY_DATABASE_URI = DB_URI

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
             'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        pass

# #调试环境
# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
#
# #测试环境
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
#
# #生产环境
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    # 'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    #
    # 'default': DevelopmentConfig
    'default':Config
}
