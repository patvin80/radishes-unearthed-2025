# Global variables for robot configuration

WHEEL_CIRCUMFERENCE_CM = 9.0# Wheel circumference in centimeters
MOTOR_PAIR_LEFT = port.A    # Left motor port
MOTOR_PAIR_RIGHT = port.E    # Right motor port
MOTOR_PAIR_ID = 0            # Motor pair identifier
LEFT_MOTOR = port.F            # Left motor port
RIGHT_MOTOR = port.B            # Right motor port

# Default movement parameters
DEFAULT_MOVEMENT_SPEED = 900# Default movement speed
DEFAULT_TURN_SPEED = 300    # Default turn speed
DEFAULT_ARM_SPEED = 600        # Default arm motor speed
DEFAULT_MOVEMENT_DELAY = 100# Default delay between movements (ms)

_motor_pair.cm_per_360_deg = WHEEL_CIRCUMFERENCE_CM

_motor_pair.pair(motor_pair.PAIR_1, MOTOR_PAIR_LEFT, MOTOR_PAIR_RIGHT)

"""#####################"""
"""# HELPER FUNCTIONS#"""
"""#####################"""

async def move_forward(distance_cm, *, speed=DEFAULT_MOVEMENT_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move robot forward a specified distance
    Args:
        distance_cm: Distance to move forward in centimeters

        speed: Motor speed (default: DEFAULT_MOVEMENT_SPEED)

        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)

    """
    degrees_needed = _motor_pair.cm_to_degrees(distance_cm)
    await _motor_pair.move_for_degrees(MOTOR_PAIR_ID, degrees_needed, 0, velocity=speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)


async def move_backward(distance_cm, *, speed=DEFAULT_MOVEMENT_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move robot backward a specified distance
    Args:
        distance_cm: Distance to move backward in centimeterscm_to_degrees
        speed: Motor speed (default: DEFAULT_MOVEMENT_SPEED)
        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    degrees_needed = _motor_pair.cm_to_degrees(distance_cm)
    await _motor_pair.move_for_degrees(MOTOR_PAIR_ID, -degrees_needed, 0, velocity=speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)

async def move_forward_and_back(forward_distance_cm, *, speed=DEFAULT_MOVEMENT_SPEED, delay_between=DEFAULT_MOVEMENT_DELAY):
    """
    Move robot forward then back to original position
    Args:
        forward_distance_cm: Distance to move forward (and back)
        speed: Motor speed (default: DEFAULT_MOVEMENT_SPEED)
        delay_between: Delay between forward and back movement (default: DEFAULT_MOVEMENT_DELAY)
    """
    await move_forward(forward_distance_cm, speed=speed, delay_after=0)
    if delay_between > 0:
        await asyncio.sleep_ms(delay_between)
    await move_backward(forward_distance_cm, speed=speed, delay_after=0)

async def turn_right(degrees=90, *, speed=DEFAULT_TURN_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):

    """
    Turn robot right by specified degrees
    Args:
        degrees: Degrees to turn right (default: 90)
        speed: Motor speed (default: DEFAULT_TURN_SPEED)
        delay_after: Delay after turn in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    # Reset yaw angle for accurate turn measurement
    motion_sensor.reset_yaw(0)
    await asyncio.sleep_ms(100)

    # Turn right using steering (steering value 100 = turn in place to the right)
    rotations = 0.5
    await _motor_pair.move_for_degrees(MOTOR_PAIR_ID,  (int)(rotations * 360), 100, velocity=speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)

async def turn_left(degrees=90, *, speed=DEFAULT_TURN_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Turn robot left by specified degrees
    Args:
        degrees: Degrees to turn left (default: 90)
        speed: Motor speed (default: DEFAULT_TURN_SPEED)
        delay_after: Delay after turn in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    # Reset yaw angle for accurate turn measurement
    motion_sensor.reset_yaw(0)
    await asyncio.sleep_ms(100)

    # Turn left using steering (steering value -100 = turn in place to the left)
    rotations = 0.5
    await _motor_pair.move_for_degrees(MOTOR_PAIR_ID,  (int)(rotations * 360), -100, velocity=speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)

async def move_left_motor(degrees, *, speed=DEFAULT_ARM_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move arm motor by specified degrees
    Args:
        degrees: Degrees to move arm (positive = one direction, negative = opposite)
        speed: Motor speed (default: DEFAULT_ARM_SPEED)
        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    await _motor.run_for_degrees(LEFT_MOTOR, degrees, speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)

async def move_right_motor(degrees, *, speed=DEFAULT_ARM_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move arm motor by specified degrees
    Args:
        degrees: Degrees to move arm (positive = one direction, negative = opposite)
        speed: Motor speed (default: DEFAULT_ARM_SPEED)
        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    await _motor.run_for_degrees(RIGHT_MOTOR, degrees, speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)    

async def move_left_motor_up_or_down(degrees, *, speed=DEFAULT_ARM_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move arm motor by specified degrees
    Args:
        degrees: Degrees to move arm (positive = one direction, negative = opposite)
        speed: Motor speed (default: DEFAULT_ARM_SPEED)
        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    await _motor.run_for_degrees(LEFT_MOTOR, degrees, speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)

async def move_right_motor_up_or_down(degrees, *, speed=DEFAULT_ARM_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move arm motor by specified degrees
    Args:
        degrees: Degrees to move arm (positive = one direction, negative = opposite)
        speed: Motor speed (default: DEFAULT_ARM_SPEED)
        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    await _motor.run_for_degrees(RIGHT_MOTOR, degrees, speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)      

async def move_left_motor_sideways(degrees, *, speed=DEFAULT_ARM_SPEED, delay_after=DEFAULT_MOVEMENT_DELAY):
    """
    Move arm motor by specified degrees
    Args:
        degrees: Degrees to move arm (positive = one direction, negative = opposite)
        speed: Motor speed (default: DEFAULT_ARM_SPEED)
        delay_after: Delay after movement in milliseconds (default: DEFAULT_MOVEMENT_DELAY)
    """
    await _motor.run_for_degrees(LEFT_MOTOR, degrees, speed)
    if delay_after > 0:
        await asyncio.sleep_ms(delay_after)                  

#endregion 