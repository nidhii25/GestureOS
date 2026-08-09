import cv2

from app.core.state.app_state import app_state
from app.services.camera_service import CameraService


camera_service = CameraService(app_state)

# Start camera
app_state.camera.camera_index = 0
result = camera_service.start_camera()
print(result)

if not result["success"]:
    print("Camera test failed.")
    print("Camera active:", app_state.camera.is_active)
    raise SystemExit

# Read and display frames
while True:
    success, frame = camera_service.read_frame()

    if not success:
        print("Failed to read frame.")
        break

    cv2.imshow("GestureOS Camera Test", frame)

    # Press Q to stop the test
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Stop camera
result = camera_service.stop_camera()
print(result)

cv2.destroyAllWindows()

print("Camera active:", app_state.camera.is_active)