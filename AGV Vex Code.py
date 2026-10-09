# Kyle Chan
# Autonomous Guided Vehicle - VEX V5
# Python reconstruction of my original VEXcode Blocks project.
# Reconstructed from photographs; not tested on hardware.
#
# Required configured devices:
# brain          - V5 Brain
# drivetrain     - Robot drivetrain
# optical        - Optical sensor
# distance       - Distance sensor
# led            - LED indicator
# start_bumper   - Start bumper switch
# stop_bumper    - Stop bumper switch
#
# Add the actual VEX device configuration below the import.
# Motor ports, gearing, wheel dimensions, and wiring are unknown.

# Extremely important note: The code may not work as intended as it was reconstructed from photographs of the original project.
# Additionally, some block code features do not have direct equivalents in Python, so some logic may be lost or misrepresented.

from vex import *


# ---------- Add robot configuration here ----------


def stop_project():
    drivetrain.stop()
    brain.program_stop()


def monitor_obstacles():
    while True:
        if distance.object_distance(MM) < 150:
            led.on()
            drivetrain.stop()

        wait(20, MSEC)


def follow_colors():
    while True:
        drivetrain.set_drive_velocity(20, PERCENT)

        brain.screen.print(optical.hue())
        brain.screen.next_row()

        optical.set_light_power(100, PERCENT)
        optical.set_light(LEDStateType.ON)
        led.off()

        # Retained from the photo, where it is labeled old code.
        if optical.color() == Color.BLUE:
            led.off()
            drivetrain.stop()
            wait(3, SECONDS)
            drivetrain.drive(FORWARD)
            drivetrain.set_drive_velocity(15, PERCENT)

        hue = optical.hue()

        # Red: turn left.
        if 15 < hue < 25:
            led.off()
            drivetrain.set_drive_velocity(15, PERCENT)
            drivetrain.turn_for(LEFT, 20, DEGREES)
            drivetrain.drive(FORWARD)
            wait(0.25, SECONDS)

        # Green: turn right.
        elif 65 < hue < 90:
            led.off()
            drivetrain.set_turn_velocity(15, PERCENT)
            drivetrain.turn_for(RIGHT, 20, DEGREES)
            drivetrain.drive(FORWARD)
            wait(0.25, SECONDS)

        # Empty else-if branch in the photo omitted.

        # Yellow: continue forward.
        elif 25 < hue < 65:
            led.off()
            drivetrain.drive(FORWARD)

        # Purple: stop temporarily, then continue forward.
        elif hue > 90:
            led.on()
            drivetrain.stop()
            wait(4, SECONDS)
            drivetrain.drive(FORWARD)
            wait(0.75, SECONDS)

        wait(20, MSEC)


# Stop bumper ends the project.
if stop_bumper.pressing():
    stop_project()

# Wait for the start bumper before starting both tasks.
while not start_bumper.pressing():
    wait(20, MSEC)

Thread(monitor_obstacles)
follow_colors()