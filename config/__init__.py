import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


lineChannelSecret=os.getenv('LINE_CHANNEL_SECRET', None)
lineChannelAccessToken=os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

nlpClientToken=os.getenv('WITAI_CLIENT_TOKEN', None)
nlpClientUrl=os.getenv('WITAI_API_URL', None)


__ALL__ = [lineChannelSecret,lineChannelAccessToken,nlpClientToken,nlpClientUrl]