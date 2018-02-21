from flask import Flask
from endpoints import endpoints
import thread_manager
import threading
from worker import Worker

if __name__ == "__main__":
    app = Flask(__name__)

    worker = Worker(target=thread_manager.run, name ="App")
    
    t = threading.Thread(target=worker.start)
    t.daemon = True
    t.start()

    app.register_blueprint(endpoints)
    app.run(host='0.0.0.0', debug = False)
