import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.vision.palm_tracker import PalmTracker
from app.vision.palm_movement import PalmMovement
from app.controllers.mouse_controller import MouseController


MODEL_PATH = "models/hand_landmarker.task"


camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)
landmark_processor = LandmarkProcessor()

palm_tracker = PalmTracker()

palm_movement = PalmMovement(
    sensitivity=1500.0,
    deadzone=0.003,
)

mouse_controller = MouseController()


hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit


print("Camera started.")
print("Move your whole palm to control the cursor.")
print("Remove your hand to stop movement.")
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

        palm_x, palm_y = palm_tracker.get_palm_center(
            landmarks
        )

        movement_x, movement_y = palm_movement.update(
            palm_x,
            palm_y,
        )

        print(
            f"\rPalm: ({palm_x:.3f}, {palm_y:.3f}) | "
            f"Movement: ({movement_x:.1f}, {movement_y:.1f})",
            end="",
        )

        if movement_x != 0 or movement_y != 0:
            mouse_controller.move_relative(
                movement_x,
                movement_y,
            )

    else:
        palm_movement.reset()

    cv2.imshow(
        "GestureOS - Palm Cursor",
        cv2.flip(frame, 1),
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nPalm cursor test complete.")