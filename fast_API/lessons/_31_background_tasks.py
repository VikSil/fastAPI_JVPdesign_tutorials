import time
from fastapi import APIRouter, BackgroundTasks, Depends

router = APIRouter()

# N.B. Background tasks are used to pass around in-memory objects
# for heavy background computation use Celery instead


def write_notification(email: str, message=''):
    with open('log.txt', mode='w') as email_file:
        content = f'notification for {email}: {message}\n'
        time.sleep(5)
        email_file.write(content)


@router.post('/send-email/{email}', status_code=202)  # 202 - Accepted
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message='some notification')

    return {'message': 'notification sent in the background'}


def write_log(message: str):
    with open('log.txt', mode='a') as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f'Found query: {q} \n'
        background_tasks.add_task(write_log, message)

    return q


@router.post('/send-notification/{email}')
async def send_notification(email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)):
    message = f'Message to {email}\n'
    background_tasks.add_task(write_log, message)

    return {'message': 'Message sent', 'query': q}
