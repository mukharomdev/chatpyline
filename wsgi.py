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


sys.path.insert(0, str(Path(__file__).parent))

app = create_app()

# Konfigurasi ngrok
ngrok_config = conf.PyngrokConfig(
    auth_token=Config.ngrokAuthToken,
    region="ap",  # asia-pacific
    monitor_thread=False
    )            



def set_webhook_with_ngrok(tunnel,AccessToken=Config):
    # Buka tunnel ngrok
    webhook_url = f"{tunnel.public_url}/webhook"
    
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
    app.run(debug=True, use_reloader=False,host='0.0.0.0', port=5000)
if __name__ == '__main__':

    try : 
        # # Buka tunnel dengan konfigurasi
        tunnel = ngrok.connect(5000, "http", pyngrok_config=ngrok_config)
        # # Dapatkan detail tunnel
        print("Tunnel URL:", tunnel.public_url)
        print("Tunnel Config:", tunnel.config)
        # # Daftar semua tunnel aktif
        # tunnels = ngrok.get_tunnels()
        # print("Active Tunnels:", tunnels)
        
        # set webhook otomatis 
        set_webhook_with_ngrok(tunnel)
        # Jalankan Flask di thread terpisah
        threading.Thread(target=run_flask).start()
        # tanpa thread 
        # run_flask()

        # logging 
        threading.Thread(target=log_flask).start()
        # Setup ngrok
        # Konfigurasi ngrok
        # ngrok_config = conf.PyngrokConfig(
        #     auth_token=Config.ngrokAuthToken,
        #     region="ap",  # asia-pacific
        #     monitor_thread=False
        # )


        
        # thread menangani autostart ngrok
        threading.Thread(target=keep_ngrok_alive, args=(5000,), daemon=True).start()
    except Exception as e:
        print(f"Error: {e}")
    # Biarkan aplikasi tetap running
    while True:
        time.sleep(1)