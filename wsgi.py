from app import create_app
from app.config import Config
import sys
from pathlib import Path
from pyngrok import ngrok
import threading
import time

sys.path.insert(0, str(Path(__file__).parent))

app = create_app()
def run_flask():
    app.run(debug=True, use_reloader=False,host='0.0.0.0', port=5000)
if __name__ == '__main__':
    
     # Jalankan Flask di thread terpisah
    threading.Thread(target=run_flask).start()
        # Setup ngrok
    ngrok.set_auth_token(Config.ngrokAuthToken)
    public_url = ngrok.connect(5000, "http")
    print(" * Ngrok tunnel:", public_url)
    
    # Biarkan aplikasi tetap running
    while True:
        time.sleep(1)