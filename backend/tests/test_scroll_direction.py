import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor

from app.gestures.scroll_direction import get_scroll_direction


MODEL_PATH = "models/hand_landmarker.task"


camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)
landmark_processor = LandmarkProcessor()


hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit


print("Camera started.")
print()
print("☝️ Point index UP   → UP")
print("👇 Point index DOWN → DOWN")
print("Other gesture       → NONE")
print()
print("Press Q to stop.")


while True:

    success, frame = camera_service.read_frame()

    if not success:
        print("\nFailed to read frame.")
        break

    result = hand_service.detect(frame)

    direction = None

    if result.hand_landmarks:

        landmarks = landmark_processor.process_hand(
            result.hand_landmarks[0]
        )

        direction = get_scroll_direction(
            landmarks
        )

    print(
        f"\rScroll Direction: "
        f"{str(direction):<5}",
        end=""
    )

    cv2.imshow(
        "GestureOS - Scroll Direction Test",
        cv2.flip(frame, 1)
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nScroll direction test complete.")