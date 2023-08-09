from multiprocessing import Process, Queue
from src.services.queue_service import mail_consumer
from src.app import create_app, rabbitmq_config, check_reservations
from flask_apscheduler import APScheduler

if __name__ == '__main__':
    app = create_app()
    queue = Queue()

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job(id='check_credits', func=check_reservations, args=[app], trigger='cron', hour=21, minute=00)
    scheduler.start()

    queue_consumer_process = Process(target=mail_consumer, args=(rabbitmq_config, queue))
    queue_consumer_process.start()

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        queue_consumer_process.terminate()
        queue_consumer_process.join()

