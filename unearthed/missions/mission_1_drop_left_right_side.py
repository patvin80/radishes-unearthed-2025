async def mission_forward_10cm(task_id):

    """
    Mission: Move robot forward 10 cm using helper function
    """
    def when_cancelled():
        # Stop all motors when cancelled
        motor_pair.stop(MOTOR_PAIR_ID)
        motor.stop(MOTOR_PAIR_LEFT)
        motor.stop(MOTOR_PAIR_RIGHT)
    try:
        # Move forward 10 cm using helper function
        await move_forward(20)
        loop.remove_task(task_id)
    except asyncio.CancelledError:

        when_cancelled()