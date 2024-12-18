# Just Blink

Just Blink is a desktop application designed to help users reduce digital eye strain by monitoring their blink rates. The app uses computer vision to track blinks and sends notifications when the blink rate falls below a healthy threshold. Additionally, the app provides session usage reports displayed on a dashboard, helping users maintain healthier screen habits.

[![Watch the intro video](https://img.youtube.com/vi/xJWYBKFWrCo/0.jpg)](https://youtu.be/xJWYBKFWrCo)

## Features

- Blink Detection: Tracks the user's blink rate in real-time using OpenCV.
- Notifications: Alerts the user when their blink rate drops below the threshold.
- Customizable Settings: Adjust sensitivity, notification frequency, and timer duration.
- Dashboard: Displays session trends and reports using interactive graphs.
- User-Friendly Interface: Built with PyQt5 for a seamless and intuitive experience.

## Installation

There is no installer, download the latest portable release from **[Releases](https://github.com/Pushkar-Adari/Just-Blink/releases)** tab and extract the zip file to your preferred location.

## Deployment

Clone the repository

```bash
git clone https://github.com/Pushkar-Adari/Just-Blink.git
cd Just-Blink
```

Install Dependencies

```bash
pip install -r requirements.txt

```

Run the application

```bash
python main.py
```
