import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.vision.landmark_indices import INDEX_TIP, THUMB_TIP


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
print("Move your hand in front of the camera.")
print("Press Q to stop.")

while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("Failed to read camera frame.")
        break

    result = hand_service.detect(frame)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:

            landmarks = landmark_processor.process_hand(
                hand_landmarks
            )

            index_tip = landmarks[INDEX_TIP]
            thumb_tip = landmarks[THUMB_TIP]

            print(
                f"\rIndex: ({index_tip.x:.2f}, "
                f"{index_tip.y:.2f}) | "
                f"Thumb: ({thumb_tip.x:.2f}, "
                f"{thumb_tip.y:.2f})",
                end=""
            )

    cv2.imshow("GestureOS - Landmark Integration", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nCamera active:", app_state.camera.is_active)
print("Landmark integration test complete.")