import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.gestures.gesture_recognizer import GestureRecognizer
from app.gestures.gesture_types import GestureType


MODEL_PATH = "models/hand_landmarker.task"


camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)
landmark_processor = LandmarkProcessor()
gesture_recognizer = GestureRecognizer()

hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit

print("Camera started.")
print("Show an open palm, then close your hand.")
print("Press Q to stop.")

while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("Failed to read frame.")
        break

    result = hand_service.detect(frame)

    gesture = GestureType.NONE

    if result.hand_landmarks:
        landmarks = landmark_processor.process_hand(
            result.hand_landmarks[0]
        )

        gesture = gesture_recognizer.recognize(
            landmarks
        )

    print(
        f"\rRecognized gesture: {gesture.name}",
        end=""
    )

    cv2.imshow(
        "GestureOS - Gesture Recognition",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nGesture recognition test complete.")