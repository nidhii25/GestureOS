import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService


MODEL_PATH = "models/hand_landmarker.task"


camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)

# Initialize hand detection
hand_service.initialize()

# Start camera
camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit

print(camera_result)
print("Hand detection started.")

# Read frames and detect hands
while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("Failed to read camera frame.")
        break

    result = hand_service.detect(frame)

    # Draw detected hand landmarks
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            height, width, _ = frame.shape

            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

    cv2.imshow("GestureOS - Hand Detection", frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("Camera active:", app_state.camera.is_active)
print("Hand detection stopped.")