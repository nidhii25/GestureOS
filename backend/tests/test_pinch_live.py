import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.vision.landmark_indices import THUMB_TIP, INDEX_TIP
from app.vision.geometry import distance
from app.gestures.pinch import PinchDetector


MODEL_PATH = "models/hand_landmarker.task"

camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)
landmark_processor = LandmarkProcessor()
pinch_detector = PinchDetector(
    pinch_threshold=0.045,
    release_threshold=0.060,
)
hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit

print("Camera started.")
print("Open your hand.")
print("Then slowly pinch thumb + index finger.")
print("Press Q to stop.")

while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("\nFailed to read frame.")
        break

    result = hand_service.detect(frame)

    if result.hand_landmarks:
        landmarks = landmark_processor.process_hand(
            result.hand_landmarks[0]
        )

        thumb = landmarks[THUMB_TIP]
        index = landmarks[INDEX_TIP]

        pinch_distance = distance(
            thumb,
            index,
        )

        pinching = pinch_detector.update(landmarks)

        print(
            f"\rDistance: {pinch_distance:.4f} | "
            f"Pinching: {pinching}",
            end="",
        )

    cv2.imshow(
        "GestureOS - Pinch Test",
        cv2.flip(frame, 1),
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nPinch test complete.")