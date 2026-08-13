import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor

from app.gestures.double_click import is_double_click_gesture
from app.gestures.double_click_hold import DoubleClickHold

from app.controllers.mouse_controller import MouseController


MODEL_PATH = "models/hand_landmarker.task"


camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)
landmark_processor = LandmarkProcessor()

double_click_hold = DoubleClickHold(
    hold_time=0.6
)

mouse_controller = MouseController()


hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit


print("Camera started.")
print()
print("H008 - Double Click Test")
print()
print("Put the cursor over a harmless file/icon.")
print("Show the pinky and hold for ~0.6 sec.")
print("It should double-click ONCE.")
print("Remove the pinky to re-arm.")
print()
print("Press Q to stop.")


while True:

    success, frame = camera_service.read_frame()

    if not success:
        print("\nFailed to read frame.")
        break


    result = hand_service.detect(frame)

    gesture_active = False


    if result.hand_landmarks:

        landmarks = landmark_processor.process_hand(
            result.hand_landmarks[0]
        )

        gesture_active = is_double_click_gesture(
            landmarks
        )


    # --------------------------------------------------------
    # H008 - DOUBLE CLICK
    # --------------------------------------------------------

    if double_click_hold.update(
        gesture_active
    ):

        mouse_controller.double_click()

        print(
            "\nH008 → DOUBLE CLICK"
        )


    print(
        f"\rH008: "
        f"{str(gesture_active):<5}",
        end=""
    )


    cv2.imshow(
        "GestureOS - H008 Double Click",
        cv2.flip(frame, 1)
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


double_click_hold.reset()

camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nH008 double-click test complete.")