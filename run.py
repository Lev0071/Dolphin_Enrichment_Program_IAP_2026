from app import create_app
from config import DEBUG_MODE

app = create_app()

if __name__ == '__main__':
    # listen on all interfaces so you can hit it from your Windows machine
    app.run(host="0.0.0.0",port=5000,debug=DEBUG_MODE)