import cv2

from app.core.state.app_state import app_state

from app.services.camera_service import CameraService
from app.services.hand_detection_service import HandDetectionService

from app.vision.landmark_processor import LandmarkProcessor
from app.vision.palm_tracker import PalmTracker
from app.vision.palm_movement import PalmMovement
from app.vision.continuous_scroll import ContinuousScroll

from app.gestures.gesture_types import GestureType
from app.gestures.gesture_recognizer import GestureRecognizer
from app.gestures.gesture_controller import GestureController

from app.gestures.thumb import (
    is_left_thumb,
    is_right_thumb,
)

from app.gestures.gesture_confirmation import GestureConfirmation
from app.gestures.edge_trigger import EdgeTrigger

from app.gestures.gesture_hold import GestureHold
from app.gestures.fist import is_fist

from app.gestures.victory import is_victory
from app.gestures.victory_hold import VictoryHold
from app.gestures.scroll_mode import ScrollMode
from app.gestures.scroll_direction import get_scroll_direction

from app.gestures.double_click import (
    is_double_click_gesture
)
from app.gestures.double_click_hold import (
    DoubleClickHold
)

from app.controllers.mouse_controller import MouseController
from app.controllers.drag_controller import DragController


MODEL_PATH = "models/hand_landmarker.task"


# ============================================================
# SERVICES
# ============================================================

camera_service = CameraService(app_state)
hand_service = HandDetectionService(MODEL_PATH)

landmark_processor = LandmarkProcessor()

mouse_controller = MouseController()

drag_controller = DragController(
    mouse_controller
)


# ============================================================
# H009 - TRACKING ON/OFF
# ============================================================

gesture_recognizer = GestureRecognizer()

gesture_controller = GestureController(
    app_state
)

gesture_hold = GestureHold(
    hold_time=8.0
)

open_palm_trigger = EdgeTrigger()


# ============================================================
# H001 - PALM CURSOR
# ============================================================

palm_tracker = PalmTracker()

palm_movement = PalmMovement(
    sensitivity=2200.0,
    deadzone=0.003,
)


# ============================================================
# H002 / H003 - THUMB CLICKS
# ============================================================

left_confirmation = GestureConfirmation(
    required_frames=5
)

right_confirmation = GestureConfirmation(
    required_frames=5
)

left_trigger = EdgeTrigger()
right_trigger = EdgeTrigger()


# ============================================================
# H006 - SCROLL MODE
# ============================================================

scroll_mode = ScrollMode()

victory_hold = VictoryHold(
    hold_time=2.0
)

continuous_scroll = ContinuousScroll(
    speed=5
)


# ============================================================
# H008 - DOUBLE CLICK
# ============================================================

double_click_hold = DoubleClickHold(
    hold_time=0.6
)


# ============================================================
# INITIALIZATION
# ============================================================

hand_service.initialize()

camera_result = camera_service.start_camera()

if not camera_result["success"]:
    print(camera_result)
    hand_service.close()
    raise SystemExit


print()
print("==========================================")
print("       GestureOS MAIN INTEGRATION TEST")
print("==========================================")
print()

print("H001 → Palm Movement → Cursor")
print("H002 → Left Thumb → Left Click")
print("H003 → Right Thumb → Right Click")
print("H004 → Fist → Grab / Drag")
print("H005 → Open Hand → Release / Drop")
print("H006 → Victory 2 sec → Scroll Mode ON/OFF")
print("H007 → Index UP/DOWN → Continuous Scroll")
print("H008 → Pinky 0.6 sec → Double Click")
print("H009 → Open Palm 5 sec → Tracking ON/OFF")

print()
print("Tracking starts in:")
print(app_state.tracking.status.name)

print()
print("Press Q to stop.")
print()


last_tracking_status = app_state.tracking.status


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = camera_service.read_frame()

    if not success:
        print("\nFailed to read frame.")
        break


    # --------------------------------------------------------
    # HAND DETECTION
    # --------------------------------------------------------

    result = hand_service.detect(frame)


    # Default values

    gesture = GestureType.NONE

    left_thumb_detected = False
    right_thumb_detected = False

    fist_detected = False
    open_hand_detected = False

    victory_detected = False
    double_click_detected = False

    scroll_direction = None
    scroll_amount = 0


    # --------------------------------------------------------
    # PROCESS HAND
    # --------------------------------------------------------

    if result.hand_landmarks:

        landmarks = landmark_processor.process_hand(
            result.hand_landmarks[0]
        )


        # ====================================================
        # BASIC GESTURE RECOGNITION
        # ====================================================

        gesture = gesture_recognizer.recognize(
            landmarks
        )


        # ====================================================
        # H009 - OPEN PALM TRACKING TOGGLE
        # ====================================================

        gesture = gesture_recognizer.recognize(
            landmarks
        )

        confirmed = gesture_hold.update(
            gesture
        )

        if gesture != GestureType.OPEN_PALM:
            open_palm_trigger.reset()

        if open_palm_trigger.update(
            confirmed and gesture == GestureType.OPEN_PALM
        ):

            response = gesture_controller.handle(
                GestureType.OPEN_PALM
            )

            print(
                "\nH009 → Open Palm → Tracking toggled"
            )

            print(response)


        # ====================================================
        # HANDEDNESS
        # ====================================================

        handedness = (
            result.handedness[0][0].category_name
        )


        # ====================================================
        # H002 / H003 - THUMB DETECTION
        # ====================================================

        if not open_hand_detected:

            left_thumb_detected = is_left_thumb(
                landmarks,
                handedness
            )

            right_thumb_detected = is_right_thumb(
                landmarks,
                handedness
            )


        # ====================================================
        # H004 - FIST
        # ====================================================

        fist_detected = is_fist(
            landmarks
        )


        # ====================================================
        # H006 - VICTORY
        # ====================================================

        victory_detected = is_victory(
            landmarks
        )

        if victory_hold.update(
            victory_detected
        ):

            active = scroll_mode.toggle()

            # Reset scroll reference whenever
            # scroll mode changes.
            scroll_direction = None

            print(
                f"\nH006 → Scroll Mode: "
                f"{'ACTIVE' if active else 'INACTIVE'}"
            )


        # ====================================================
        # H008 - PINKY DOUBLE CLICK
        # ====================================================

        double_click_detected = (
            is_double_click_gesture(
                landmarks
            )
        )


    else:

        # No hand detected.

        open_hand_detected = False
        victory_detected = False
        double_click_detected = False

        # Re-arm hold-based gestures.
        gesture_hold.update(GestureType.NONE)
        victory_hold.update(False)
        double_click_hold.update(False)

        # Don't keep an old scroll reference.
        scroll_direction = None


    # --------------------------------------------------------
    # TRACKING STATUS
    # --------------------------------------------------------

    current_tracking_status = (
        app_state.tracking.status
    )


    if current_tracking_status != last_tracking_status:

        print(
            f"\nTracking status: "
            f"{current_tracking_status.name}"
        )


        # Reset cursor reference whenever
        # tracking changes.

        palm_movement.reset()


        # Reset click states.

        left_confirmation.reset()
        right_confirmation.reset()

        left_trigger.reset()
        right_trigger.reset()


        # Reset scroll.

        scroll_mode.reset()
        victory_hold.reset()


        # Reset double click.

        double_click_hold.reset()


        # SAFETY:
        # Never leave a drag active when tracking
        # becomes inactive.

        drag_controller.reset()


        last_tracking_status = (
            current_tracking_status
        )


    # ========================================================
    # ONLY RUN ACTIONS WHEN TRACKING IS ACTIVE
    # ========================================================

    if (
        current_tracking_status.name == "ACTIVE"
        and result.hand_landmarks
    ):


        # ====================================================
        # H001 - PALM CURSOR
        # ====================================================

        palm_x, palm_y = (
            palm_tracker.get_palm_center(
                landmarks
            )
        )

        movement_x, movement_y = (
            palm_movement.update(
                palm_x,
                palm_y
            )
        )


        if movement_x != 0 or movement_y != 0:

            mouse_controller.move_relative(
                movement_x,
                movement_y
            )


        # ====================================================
        # H002 - LEFT CLICK
        # ====================================================

        left_confirmed = (
            left_confirmation.update(
                left_thumb_detected
            )
        )


        if left_trigger.update(
            left_confirmed
        ):

            mouse_controller.left_click()

            print(
                "\nH002 → LEFT CLICK"
            )


        # ====================================================
        # H003 - RIGHT CLICK
        # ====================================================

        right_confirmed = (
            right_confirmation.update(
                right_thumb_detected
            )
        )


        if right_trigger.update(
            right_confirmed
        ):

            mouse_controller.right_click()

            print(
                "\nH003 → RIGHT CLICK"
            )


        # ====================================================
        # H004 - FIST → START DRAG
        # ====================================================

        if (
            fist_detected
            and not drag_controller.dragging
        ):

            if drag_controller.start_drag():

                print(
                    "\nH004 → DRAG START"
                )


        # ====================================================
        # H005 - OPEN HAND → DROP
        # ====================================================

        if (
            open_hand_detected
            and drag_controller.dragging
        ):

            if drag_controller.stop_drag():

                print(
                    "\nH005 → DROP"
                )


        # ====================================================
        # H007 - CONTINUOUS SCROLL
        # ====================================================

        if scroll_mode.active:

            scroll_direction = (
                get_scroll_direction(
                    landmarks
                )
            )


            scroll_amount = (
                continuous_scroll.get_amount(
                    scroll_direction
                )
            )


            if scroll_amount != 0:

                mouse_controller.scroll(
                    scroll_amount
                )


        # ====================================================
        # H008 - DOUBLE CLICK
        # ====================================================

        if double_click_hold.update(
            double_click_detected
        ):

            mouse_controller.double_click()

            print(
                "\nH008 → DOUBLE CLICK"
            )


    else:

        # ====================================================
        # TRACKING INACTIVE
        # ====================================================

        palm_movement.reset()

        left_confirmation.reset()
        right_confirmation.reset()

        left_trigger.reset()
        right_trigger.reset()

        # Safety: release an active drag.
        drag_controller.reset()


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    cv2.imshow(
        "GestureOS - Main Integration Test",
        cv2.flip(frame, 1)
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

drag_controller.reset()

palm_movement.reset()

scroll_mode.reset()
victory_hold.reset()

gesture_hold.reset()
open_palm_trigger.reset()

double_click_hold.reset()


camera_service.stop_camera()
hand_service.close()

cv2.destroyAllWindows()


print()
print("==========================================")
print("       GestureOS TEST COMPLETE")
print("==========================================")
print(
    "Final tracking status:",
    app_state.tracking.status
)