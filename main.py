# main.py
import threading
import time
from stepper import StepperMotor
import camera_dashboard  # Assumes camera_dashboard has thread-safe methods

# Initialize the stepper motor
motor = StepperMotor(pins=[17, 18, 27, 22])  # Match to your wiring

def run_camera_dashboard():
    """
    Runs the tkinter-based camera dashboard GUI.
    This function is blocking and should run in its own thread if needed.
    """
    camera_dashboard.set_motor_instance(motor)  # Inject motor dependency
    camera_dashboard.run_dashboard()

def monitor_shutdown():
    """
    Optional background task to monitor for shutdown conditions or cleanup logic.
    """
    try:
        while True:
            time.sleep(1)  # Simulate doing background monitoring or logging
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        motor.cleanup()

if __name__ == "__main__":
    # Thread for optional monitoring
    monitor_thread = threading.Thread(target=monitor_shutdown, daemon=True)
    monitor_thread.start()

    # Run camera dashboard (blocking main thread)
    run_camera_dashboard()
