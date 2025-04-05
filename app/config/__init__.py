import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
	lineChannelSecret=os.getenv('LINE_CHANNEL_SECRET', None)
	lineChannelAccessToken=os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

	nlpClientToken=os.getenv('WITAI_CLIENT_TOKEN', None)
	nlpClientUrl=os.getenv('WITAI_API_URL', None)

	ngrokAuthToken=os.getenv('NGROK_AUTH_TOKEN',None)

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', None)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # PostgreSQL di produksi
# Pilih config berdasarkan environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

__all__ = [Config]