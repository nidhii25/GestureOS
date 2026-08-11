import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.gestures.gesture_types import GestureType
from app.gestures.gesture_recognizer import GestureRecognizer
from app.gestures.gesture_hold import GestureHold
from app.gestures.gesture_controller import GestureController


MODEL_PATH = "models/hand_landmarker.task"

camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)
landmark_processor = LandmarkProcessor()

gesture_recognizer = GestureRecognizer()
gesture_hold = GestureHold(hold_time=1.0)
gesture_controller = GestureController(app_state)


hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit


print("Camera started.")
print("Show an open palm and hold it for 1 second.")
print("Remove your hand and repeat to toggle tracking.")
print("Press Q to stop.")


last_tracking_status = app_state.tracking.status


while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("\nFailed to read frame.")
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

    confirmed = gesture_hold.update(gesture)

    if confirmed:
        response = gesture_controller.handle(
            gesture
        )

        print(
            f"\nGesture confirmed: {gesture.name}"
        )
        print(response)

    current_tracking_status = app_state.tracking.status

    if current_tracking_status != last_tracking_status:
        print(
            f"\nTracking status: "
            f"{current_tracking_status.name}"
        )

        last_tracking_status = current_tracking_status

    cv2.imshow(
        "GestureOS - Open Palm Tracking",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print(
    "\nFinal tracking status:",
    app_state.tracking.status
)