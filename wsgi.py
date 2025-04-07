from app import create_app
from app.config import Config
import sys
from pathlib import Path
from pyngrok import ngrok,conf
import threading
import time
import logging
import ssl
import requests
import os


sys.path.insert(0, str(Path(__file__).parent))

app = create_app()
PORT = 5000
# Konfigurasi ngrok
ngrok_config = conf.PyngrokConfig(
    auth_token=Config.ngrokAuthToken,
    region="ap",  # asia-pacific
    monitor_thread=False
    )            



def set_webhook_with_ngrok(AccessToken=Config):
    # Buka tunnel ngrok
    tunnel = ngrok.connect(PORT, "http", pyngrok_config=ngrok_config)

    webhook_url = f"{tunnel.public_url}/webhook"
    
    # # Dapatkan detail tunnel
    print("Tunnel URL:", tunnel.public_url)
    print("Tunnel Config:", tunnel.config)
    print(f"Ngrok URL: {webhook_url}")
    
    # Set webhook LINE
    headers = {
        'Authorization': f"Bearer {AccessToken.lineChannelAccessToken}",
        'Content-Type': 'application/json'
    }
    
    payload = {
        'endpoint': webhook_url
    }
    
    response = requests.put(
        'https://api.line.me/v2/bot/channel/webhook/endpoint',
        headers=headers,
        json=payload
    )
    
    print("Webhook setup response:", response.status_code, response.text)

def keep_ngrok_alive(port):
    while True:
        try:
            # Setup ngrok

            # Cek apakah tunnel masih aktif
            tunnels = ngrok.get_tunnels()
            if not any(t.public_url for t in tunnels):
                print("Restarting ngrok tunnel...")
                ngrok.kill()
                ngrok.connect(port, "http",pyngrok_config=ngrok_config)
        except:
            pass
        
        time.sleep(10)


def log_flask():
    logging.basicConfig(filename='app.log', level=logging.INFO)
def run_flask():
    # eksplisit set minimum protocol
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.minimum_version = ssl.TLSVersion.TLSv1_2  # Hanya TLS 1.3
    # # context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    # # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_cert_chain(
    # 'pelatge.localtest.me.pem',
    # 'pelatge.localtest.me-key.pem')    
    # app.run(debug=True, use_reloader=False,host='pelatge.localtest.me', port=8443,ssl_context=context)
    app.run(debug=True, use_reloader=True,host='0.0.0.0', port=PORT)
def background_thread():
     # Biarkan aplikasi tetap running
    while True:
        time.sleep(5)

if __name__ == '__main__':

    try : 

        
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            # Jalankan Flask di thread terpisah
            # threading.Thread(target=run_flask).start()
            
            # Running ngrok thread
            Ngrok_thread = threading.Thread(target=set_webhook_with_ngrok)
            Ngrok_thread.daemon = True
            Ngrok_thread.start()

            # logging 
            logFlask_thread = threading.Thread(target=log_flask)
            logFlask_thread.daemon = True
            logFlask_thread.start()
                   
            # thread menangani autostart ngrok
            # keepNgrokLive_thread = threading.Thread(target=keep_ngrok_alive, args=(PORT,))            
            # keepNgrokLive_thread.daemon = True
            # keepNgrokLive_thread.start()

            # Background thread utama 
            Bg_thread = threading.Thread(target=background_thread)
            Bg_thread.daemon = True
            Bg_thread.start()

        # tanpa thread 
        run_flask()

    except Exception as e:
        print(f"Error: {e}")
   