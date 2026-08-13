import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService
from app.vision.landmark_processor import LandmarkProcessor
from app.gestures.thumb import (
    is_left_thumb,
    is_right_thumb,
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
print("Show your LEFT hand.")
print("Extend only your thumb.")
print("Then try your RIGHT hand.")
print("Press Q to stop.")

while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("\nFailed to read frame.")
        break

    result = hand_service.detect(frame)

    if result.hand_landmarks:
        for i, hand_landmarks in enumerate(
            result.hand_landmarks
        ):
            landmarks = landmark_processor.process_hand(
                hand_landmarks
            )

            handedness = result.handedness[i][0].category_name

            left_thumb = is_left_thumb(
                landmarks,
                handedness,
            )

            right_thumb = is_right_thumb(
                landmarks,
                handedness,
            )
            thumb_tip = landmarks[4]
            thumb_mcp = landmarks[2]

            # print(
            #     f"\rHand: {handedness} | "
            #     f"Thumb TIP: "
            #     f"({thumb_tip.x:.2f}, {thumb_tip.y:.2f}) | "
            #     f"Thumb MCP: "
            #     f"({thumb_mcp.x:.2f}, {thumb_mcp.y:.2f}) | "
            #     f"Left: {left_thumb} | "
            #     f"Right: {right_thumb}",
            #     end="",
            # )
            print(
                f"\rHand: {handedness} | "
                f"Left Thumb: {left_thumb} | "
                f"Right Thumb: {right_thumb}",
                end="",
            )

    cv2.imshow(
        "GestureOS - H002 Thumb Test",
        cv2.flip(frame, 1),
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()

print("\nH002 thumb test complete.")