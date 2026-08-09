import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
    is_open_palm,
)


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
print("Show different hand positions.")
print("Press Q to stop.")

while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("Failed to read frame.")
        break

    result = hand_service.detect(frame)

    if result.hand_landmarks:
        landmarks = landmark_processor.process_hand(
            result.hand_landmarks[0]
        )

        print(
            f"\rIndex: {is_index_extended(landmarks)} | "
            f"Middle: {is_middle_extended(landmarks)} | "
            f"Ring: {is_ring_extended(landmarks)} | "
            f"Pinky: {is_pinky_extended(landmarks)} | "
            f"Open Palm: {is_open_palm(landmarks)}",
            end=""
        )

    cv2.imshow("GestureOS - Finger Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nFinger detection test complete.")