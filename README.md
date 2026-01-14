# SmartGuard CCTV: AI-Powered Intrusion Detection System

**SmartGuard CCTV** is a real-time surveillance solution designed to monitor restricted areas using a webcam. By combining **YOLOv8** for object detection and **dlib** for facial recognition, the system tracks individuals entering defined zones and triggers audio-visual alerts based on loitering time or identity.

## 🚀 Key Features

* **Real-time Person Detection:** Uses the Ultralytics YOLOv8 model to detect humans with high accuracy.
* **Restricted Zone Monitoring:** Define specific coordinates within the video feed to act as a "virtual fence."
* **Facial Recognition:** Identifies known individuals against a local database of images.
* **Loitering Detection:** Tracks how long a person remains in the zone and triggers alerts after a set threshold.
* **Audio Alerts:** Integrated Text-to-Speech (TTS) engine (`pyttsx3`) to vocalize warnings.
* **Evidence Capture:** Automatically saves high-resolution screenshots when an alert is triggered.

## 📂 Project Structure

To run the system correctly, your directory must be structured as follows:

```text
SmartGuard-CCTV/
│
├── known_faces/           # 📁 REQUIRED: Folder containing images of known people
│   ├── person1.jpg        # Image filenames become the person's ID name
│   ├── john_doe.png
│   └── ...
│
├── cctv3.0.py             # 📄 Version 3.0: General Loitering Detection
├── cctv5.1.py             # 📄 Version 5.1: Targeted Person Alert
├── cct5.2.py              # 📄 Version 5.2: Unknown Intruder Alert
│
├── requirements.txt       # 📄 Python dependencies
└── yolov8n.pt             # 🧠 Model weights (downloaded auto on first run)

```

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmed-Jedidi/SIVAR_NextDeep.git
cd SIVAR_NextDeep

```

### 2. Install Dependencies

**Note:** The `face_recognition` library requires `dlib`, which depends on CMake.

**Windows Users:** You may need to install Visual Studio with C++ tools first to compile `dlib`.
**Linux/Mac Users:** Ensure `cmake` is installed (`sudo apt install cmake`).

```bash
pip install opencv-python ultralytics face_recognition playsound pyttsx3

```

Otherwise, You can install all required libraries using the provided `requirements.txt` file.

**Create the `requirements.txt` file:**

```text
opencv-python
ultralytics
face_recognition
playsound==1.2.2
pyttsx3
cmake

```

**Run the installation:**

```bash
pip install -r requirements.txt

```

### ⚠️ Critical Installation Notes

Please read this before installing, as the **Face Recognition** and **Audio** libraries have specific system requirements:

* **Playsound Version:** The `requirements.txt` strictly specifies `playsound==1.2.2`. Do not upgrade this package. Newer versions (like 1.3.0) often fail on Windows/Python 3.x environments.
* **Face Recognition & Dlib:** The `face_recognition` library depends on `dlib`, which is a C++ library.
* **Windows Users:** You must have **Visual Studio** installed with the **"Desktop development with C++"** workload enabled to compile `dlib`.
* **Linux/Mac Users:** You must have CMake installed before running pip.
* Linux: `sudo apt-get install cmake`
* Mac: `brew install cmake`

### 3. Setup Known Faces

Create a folder named `known_faces` in the root directory. Add clear, forward-facing photos of people you want the system to recognize.

* *Example:* If you add `admin.jpg`, the system will recognize that face as "admin".

## 💻 Usage & script Versions

Run the script using Python:

```bash
python cctv5.1.py

```

### Version Breakdown

| Script | Purpose | Logic |
| --- | --- | --- |
| **cctv3.0.py** | **General Security** | Detects *any* person in the zone. Triggers an alert if they stay longer than **30 seconds**. Uses YOLO primarily. |
| **cctv5.1.py** | **Targeted Tracking** | Scans faces. Triggers an alert ONLY if a *specific person* (e.g., "person1") is detected in the zone for > **5 seconds**. |
| **cct5.2.py** | **Intruder Alert** | Scans faces. Triggers an alert if an **Unknown** person (face not in database) lingers in the zone for > **10 seconds**. |

## ⚙️ Configuration

You can customize the system by editing the variables at the top of the Python scripts.

### 1. Adjusting the Restricted Zone

Change the coordinates of the bounding box `(x1, y1, x2, y2)`:

```python
# (Left, Top, Right, Bottom)
zone = (150, 100, 500, 400) 

```

### 2. Changing Alert Logic

* **In `cctv5.1.py`:** Change the target name to match your image filename.
```python
if name == "John": # Change "John" to the name of your file in known_faces/

```



## ⚠️ Troubleshooting

* **`ModuleNotFoundError: No module named 'cmake'`**: Run `pip install cmake` and try installing `face_recognition` again.
* **Laggy Video:** If running on a CPU, switch the YOLO model to the nano version (`yolov8n.pt`) for better FPS.
* **Camera not opening:** Ensure `cv2.VideoCapture(0)` is correct. If you have multiple webcams, try changing `0` to `1`.

## 📜 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.



