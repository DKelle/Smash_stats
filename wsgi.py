from app import app
import thread_manager
import threading
from worker import Worker
from endpoints import endpoints

worker = Worker(target=thread_manager.run, name ="App")
t = threading.Thread(target=worker.start)
t.daemon = True
t.start()

app.register_blueprint(endpoints)
if __name__ == "__main__":
    app.run()
