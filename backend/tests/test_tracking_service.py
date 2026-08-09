from app.core.state.app_state import app_state
from app.core.state.permission_state import PermissionStatus
from app.services.tracking_service import TrackingService

tracking_service = TrackingService(app_state)
app_state.application.is_running = False

print(tracking_service.start_tracking())

app_state.application.is_running = True
print(tracking_service.start_tracking())

app_state.permission.grant_camera()

print(tracking_service.start_tracking())

print(app_state.tracking.status)

print(tracking_service.idle_tracking())

print(app_state.tracking.status)