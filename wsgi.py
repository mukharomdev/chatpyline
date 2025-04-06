from app import create_app
from app.config import Config
import sys
from pathlib import Path
from pyngrok import ngrok
import threading
import time
import logging
import ssl



sys.path.insert(0, str(Path(__file__).parent))

app = create_app()




def log_flask():
    logging.basicConfig(filename='app.log', level=logging.INFO)
def run_flask():
    # eksplisit set minimum protocol
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2  # Hanya TLS 1.3
    # context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    # context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(
    'pelatge.localtest.me.pem',
    'pelatge.localtest.me-key.pem')    
    app.run(debug=True, use_reloader=False,host='pelatge.localtest.me', port=8443,ssl_context=context)
if __name__ == '__main__':

    try :    
         # Jalankan Flask di thread terpisah
        threading.Thread(target=run_flask).start()

        # logging 
        threading.Thread(target=log_flask).start()
        # Setup ngrok
        ngrok.set_auth_token(Config.ngrokAuthToken)
        public_url = ngrok.connect(8443, "http")
        print(" * Ngrok tunnel:", public_url)
        print("Using https localhost")
    except Exception as e:
        print(f"Error: {e}")
    # Biarkan aplikasi tetap running
    while True:
        time.sleep(1)