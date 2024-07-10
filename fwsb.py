from plyer import notification
import time

blink_reminder = notification.notify(
    title = 'Just Blink',
    message = 'Reminder to blink',
    app_icon = None,
    timeout = 10,
    toast = False
)
time.sleep(15)
timer_reminder = notification.notify(
    title = 'Just Blink',
    message = 'Your break is about to finish.',
    app_icon = None,
    timeout=10,
    toast = True
)

