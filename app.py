from flask import Flask
from endpoints import endpoints
import thread_manager
import threading

if __name__ == "__main__":
    app = Flask(__name__)

    threading.Thread(target=thread_manager.run).start()

    app.register_blueprint(endpoints)
    app.run()

