# Just Blink

Just Blink is a desktop application designed to help users reduce digital eye strain by monitoring their blink rates. The app uses computer vision to track blinks and sends notifications when the blink rate falls below a healthy threshold. Additionally, the app provides session usage reports displayed on a dashboard, helping users maintain healthier screen habits.

<div align="center">
[![Watch the intro video](https://img.youtube.com/vi/xJWYBKFWrCo/0.jpg)](https://youtu.be/xJWYBKFWrCo)
</div>
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

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

You are free to use, modify, and distribute this software under the following terms:

- You must include the original copyright and license notice in any copies or substantial portions of the software.
- If you distribute modified versions of the software, they must also be licensed under GPL v3.

For more details, see the full [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
