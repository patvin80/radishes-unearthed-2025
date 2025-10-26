#region "Minified Code for Python Blocks - DONOT CHANGE"
import asyncio,motor,motor_pair,distance_sensor,color_matrix,force_sensor,color,orientation,math,random
from hub import button,sound,light_matrix,motion_sensor,light,port
async def dummyTask():
	timer.reset_timer()
	while True:await asyncio.sleep_ms(9999999)
class timerClass:
	def __init__(self):self.initial=None
	def get_time_ms(self,notUsed=None):return asyncio.ticks()-self.initial
	def reset_timer(self):self.initial=asyncio.ticks()
timer=timerClass()
class task_manager:
	def __init__(self):self.tasks={};self.main_tasks={};self.add_main_task('system_init',dummyTask())
	def add_main_task(self,task_id,coroutine):
		if task_id in self.main_tasks:raise ValueError('that main task already exists')
		task=asyncio.create_task(coroutine);self.main_tasks[task_id]=task
	def add_task(self,task_id,coroutine):
		if task_id in self.main_tasks:raise ValueError('cannot add task under id that already exists in main tasks')
		if not task_id in self.tasks:task=asyncio.create_task(coroutine);self.tasks[task_id]=task
	def add_or_replace_task(self,task_id,coroutine):
		if task_id in self.main_tasks:raise ValueError('cannot add task under id that already exists in main tasks')
		if task_id in self.tasks:self.remove_task(task_id)
		task=asyncio.create_task(coroutine);self.tasks[task_id]=task
	def cancel_task(self,task_id):
		if task_id in self.main_tasks:raise ValueError('cannot remove main task')
		if task_id in self.tasks:task=self.tasks[task_id];task.cancel();del self.tasks[task_id]
	def cancel_all_except(self,task_ids_to_keep=None):
		if task_ids_to_keep is None:task_ids_to_keep=[]
		elif isinstance(task_ids_to_keep,str):task_ids_to_keep=[task_ids_to_keep]
		tasks_to_cancel=[task_id for task_id in self.tasks if task_id not in task_ids_to_keep]
		for task_id in tasks_to_cancel:self.cancel_task(task_id)
	def remove_task(self,task_id):
		if task_id in self.main_tasks:raise ValueError('cannot remove main task')
		if task_id in self.tasks:del self.tasks[task_id]
	async def wait_for(self,task_ids):
		if isinstance(task_ids,str):task_ids=[task_ids]
		tasks_to_wait=[self.tasks[task_id]for task_id in task_ids if task_id in self.tasks]
		if tasks_to_wait:await asyncio.gather(*tasks_to_wait)
	async def run_all_tasks(self):all_tasks=list(self.tasks.values())+list(self.main_tasks.values());await asyncio.gather(*all_tasks)
loop=task_manager()
def midi_to_hz(midi_note):frequency=440*2**((midi_note-69)/12);return round(frequency)
class sound_class:
	async def beep(self,frequency=440,duration=500,volume=100,*,attack=0,decay=0,sustain=100,release=0,transition=10,waveform=sound.WAVEFORM_SINE,channel=sound.DEFAULT):sound.beep(frequency,duration,volume,attack=attack,decay=decay,sustain=sustain,release=release,transition=transition,waveform=waveform,channel=channel);await asyncio.sleep_ms(duration)
	async def note(self,note=60,duration=500,volume=100,*,attack=0,decay=0,sustain=100,release=0,transition=10,waveform=sound.WAVEFORM_SINE,channel=sound.DEFAULT):sound.beep(midi_to_hz(note),duration,volume,attack=attack,decay=decay,sustain=sustain,release=release,transition=transition,waveform=waveform,channel=channel);await asyncio.sleep_ms(duration)
	def noteSync(self,note=60,duration=500,volume=100,*,attack=0,decay=0,sustain=100,release=0,transition=10,waveform=sound.WAVEFORM_SINE,channel=sound.DEFAULT):sound.beep(midi_to_hz(note),duration,volume,attack=attack,decay=decay,sustain=sustain,release=release,transition=transition,waveform=waveform,channel=channel)
	def stop(self):sound.beep(0,0,0)
_sound=sound_class()
async def wait_for_motor(port,*,extra=0,skip=False):
	if skip:return
	if extra>0:await asyncio.sleep_ms(extra)
	while motor.get_duty_cycle(port)==0:await asyncio.sleep_ms(0)
	while not motor.get_duty_cycle(port)==0:await asyncio.sleep_ms(0)
class motor_class:
	def hold(self,choosen_stop,port):
		if choosen_stop==motor.HOLD:motor.stop(port,stop=motor.HOLD)
	def filter_hold(self,choosen_stop):return choosen_stop if choosen_stop!=motor.HOLD else motor.BRAKE
	async def run_for_time(self,port,duration,velocity,*,stop=motor.BRAKE,acceleration=5000,deceleration=5000):motor.stop(port);motor.run_for_time(port,duration,velocity,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(port,extra=20);self.hold(stop,port)
	async def run_for_degrees(self,port,degrees,velocity,*,stop=motor.SMART_BRAKE,acceleration=5000,deceleration=5000):motor.stop(port);motor.run_for_degrees(port,degrees,velocity,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(port,extra=20);self.hold(stop,port)
	async def run_to_absolute_position(self,port,position,velocity,*,direction,stop=motor.SMART_BRAKE,acceleration=5000,deceleration=5000):motor.stop(port);motor.run_to_absolute_position(port,position,velocity,direction=direction,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(port,skip=motor.absolute_position(port)==position,extra=20);self.hold(stop,port)
	async def run_to_relative_position(self,port,position,velocity,*,stop=motor.SMART_BRAKE,acceleration=5000,deceleration=5000):motor.stop(port);motor.run_to_relative_position(port,position,velocity,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(port,skip=motor.relative_position(port)==position,extra=20);self.hold(stop,port)
	def stop(self,port,*,stop=motor.BRAKE):motor.stop(port,stop=stop)
_motor=motor_class()
class motor_pair_class:
	def __init__(self):self.pairs=[[0,0]]*3;self.cm_per_360_deg=0;self.inch_per_360_deg=0
	def hold(self,choosen_stop,pair):
		if choosen_stop==motor.HOLD:motor_pair.stop(pair,stop=motor.HOLD)
	def filter_hold(self,choosen_stop):return choosen_stop if choosen_stop!=motor.HOLD else motor.BRAKE
	def pair(self,pair,left_motor,right_motor):motor_pair.pair(pair,left_motor,right_motor);self.pairs[pair]=[left_motor,right_motor]
	async def move_for_degrees(self,pair,degrees,steering,*,velocity=180,stop=motor.BRAKE,acceleration=2000,deceleration=2000):motor_pair.stop(pair);motor_pair.move_for_degrees(pair,degrees,steering,velocity=velocity,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(self.pairs[pair][0],extra=5);self.hold(stop,pair)
	async def move_for_time(self,pair,duration,steering,*,velocity=180,stop=motor.BRAKE,acceleration=2000,deceleration=2000):motor_pair.stop(pair);motor_pair.move_for_time(pair,duration,steering,velocity=velocity,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(self.pairs[pair][0],extra=5);self.hold(stop,pair)
	async def move_tank_for_degrees(self,pair,degrees,left_velocity,right_velocity,*,stop=motor.BRAKE,acceleration=2000,deceleration=2000):motor_pair.stop(pair);motor_pair.move_tank_for_degrees(pair,degrees,left_velocity,right_velocity,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(self.pairs[pair][0],extra=5);self.hold(stop,pair)
	async def move_tank_for_time(self,pair,left_velocity,right_velocity,duration,*,stop=motor.BRAKE,acceleration=2000,deceleration=2000):motor_pair.stop(pair);motor_pair.move_tank_for_time(pair,left_velocity,right_velocity,duration,stop=self.filter_hold(stop),acceleration=acceleration,deceleration=deceleration);await wait_for_motor(self.pairs[pair][0],extra=5);self.hold(stop,pair)
	def cm_to_degrees(self,cm):return round(cm/self.cm_per_360_deg*360)
	def inch_to_degrees(self,inch):return round(inch/self.inch_per_360_deg*360)
	def set_cm_per_360_deg(self,cm):self.cm_per_360_deg=cm
	def set_inch_per_360_deg(self,inch):self.inch_per_360_deg=inch
_motor_pair=motor_pair_class()
class color_matrix_class:
	async def show(self,port,pixels,duration):color_matrix.show(port,pixels);await asyncio.sleep_ms(duration);color_matrix.clear(port)
	def rotate_right(self,grid):face=[grid[i:i+3]for i in range(0,9,3)];rotated_face=[list(row)for row in zip(*face[::-1])];return[item for row in rotated_face for item in row]
	def rotate_left(self,grid):face=[grid[i:i+3]for i in range(0,9,3)];rotated_face=[list(row)for row in list(zip(*face))[::-1]];return[item for row in rotated_face for item in row]
	def scale_pixels(self,pixels,intensity):return[(x,round(y*intensity/100))for(x,y)in pixels]
_color_matrix=color_matrix_class()
class light_matrix_class:
	async def wait_for_light_matrix(self):
		def checkIfEmpty():
			for x in range(5):
				for y in range(5):
					if light_matrix.get_pixel(x,y)!=0:return False
			return True
		while not checkIfEmpty():await asyncio.sleep_ms(0)
		while checkIfEmpty():await asyncio.sleep_ms(0)
		while not checkIfEmpty():await asyncio.sleep_ms(0)
	async def write(self,text,intensity=100,time_per_character=500):light_matrix.write(text,intensity,time_per_character);await self.wait_for_light_matrix()
	async def show(self,pixels,duration):light_matrix.show(pixels);await asyncio.sleep_ms(duration);light_matrix.clear()
	async def show_image(self,image,duration):light_matrix.show_image(image);await asyncio.sleep_ms(duration);light_matrix.clear()
	def rotate_right(self):current_orientation=light_matrix.get_orientation();light_matrix.set_orientation(current_orientation+1)if current_orientation<3 else light_matrix.set_orientation(0)
	def rotate_left(self):current_orientation=light_matrix.get_orientation();light_matrix.set_orientation(current_orientation+-1)if current_orientation>0 else light_matrix.set_orientation(3)
	def prepare_image(self,pixels):return[(pixel+1)*10 if pixel!=0 else 0 for pixel in sum(image,[])]
	def scale_pixels(self,pixels,intensity):return[round(pixel*intensity/100)for pixel in pixels]
_light_matrix=light_matrix_class()
class waitClass:
	async def to_be(self,sensor,port,expected_value):
		while sensor(port)==expected_value:await asyncio.sleep_ms(0)
		while not sensor(port)==expected_value:await asyncio.sleep_ms(0)
	async def to_be_more(self,sensor,port,expected_value):
		while sensor(port)>expected_value:await asyncio.sleep_ms(0)
		while not sensor(port)>expected_value:await asyncio.sleep_ms(0)
	async def to_be_less(self,sensor,port,expected_value):
		while sensor(port)<expected_value:await asyncio.sleep_ms(0)
		while not sensor(port)<expected_value:await asyncio.sleep_ms(0)
	async def to_be_less_and_valid(self,sensor,port,expected_value):
		while sensor(port)<expected_value or sensor(port)==-1:await asyncio.sleep_ms(0)
		while not sensor(port)<expected_value or sensor(port)==-1:await asyncio.sleep_ms(0)
	async def to_not_be(self,sensor,port,expected_value):
		while sensor(port)==expected_value:await asyncio.sleep_ms(0)
	async def to_not_be_and_valid(self,sensor,port,expected_value):
		while sensor(port)==expected_value or sensor(port)==-1:await asyncio.sleep_ms(0)
wait=waitClass()
class eventsClass:
	def __init__(self):self.saved_values=[None]*6
	async def when_program_starts(self,task_id,coroutine):loop.add_task(task_id,coroutine(task_id))
	async def when_custom_sensor(self,task_id,coroutine,sensor):
		while True:await sensor();loop.add_task(task_id,coroutine(task_id))
	async def when_sensor_is(self,task_id,coroutine,sensor,_port,value):
		while True:await wait.to_be(sensor,_port,value);loop.add_task(task_id,coroutine(task_id))
	async def when_sensor_is_more(self,task_id,coroutine,sensor,_port,value):
		while True:await wait.to_be_more(sensor,_port,value);loop.add_task(task_id,coroutine(task_id))
	async def when_sensor_is_less(self,task_id,coroutine,sensor,_port,value):
		while True:await wait.to_be_less(sensor,_port,value);loop.add_task(task_id,coroutine(task_id))
	async def when_sensor_is_less_and_valid(self,task_id,coroutine,sensor,_port,value):
		while True:await wait.to_be_less(sensor,_port,value);loop.add_task(task_id,coroutine(task_id))
	async def when_sensor_changed(self,task_id,coroutine,sensor,_port):
		if self.saved_values[_port]==None:self.saved_values[_port]=sensor(_port)
		while True:await wait.to_not_be(sensor,_port,self.saved_values[_port]);self.saved_values[_port]=sensor(_port);loop.add_task(task_id,coroutine(task_id))
	async def when_sensor_changed_and_valid(self,task_id,coroutine,sensor,_port):
		if self.saved_values[_port]==None:self.saved_values[_port]=sensor(_port)
		while True:await wait.to_not_be_and_valid(sensor,_port,self.saved_values[_port]);self.saved_values[_port]=sensor(_port);loop.add_task(task_id,coroutine(task_id))
events=eventsClass()
class distanceSensorClass:
	def distance_cm(self,port):distance=distance_sensor.distance(port);return round(distance/10)if distance!=-1 else-1
	def distance_inch(self,port):distance=distance_sensor.distance(port);return round(distance*3.93701)if distance!=-1 else-1
	def distance_percentage(self,port):distance=distance_sensor.distance(port);return round(distance/2)if distance!=-1 else-1
_distanceSensor=distanceSensorClass()
class motionSensorClass:
	def tilt_angles(self,index):return motion_sensor.tilt_angles()[index]
	def tilted(self,_notUsed):tilts=motion_sensor.tilt_angles();return tilts[1]<-130 or tilts[1]>130 or tilts[2]<-130 or tilts[2]>130
	def upside_down(self,_notUsed):tilts=motion_sensor.tilt_angles();return(tilts[2]>1350 or tilts[2]<-1350)and(tilts[1]>-450 and tilts[1]<450)
	def gesture(self,_notUsed):return motion_sensor.gesture()
	def stable(self,_notUsed):return motion_sensor.stable()
_motion_sensor=motionSensorClass()

#endregion

#region "Helper Functions sync with unearthed/helpers/helper.py"

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

#region "Missions in this run - sync with unearthed/mission folder"
"""#####################"""
"""#MISSION FUNCTIONS #"""
"""#####################"""

async def mission_1_raise_left_arm_move_forward_move_backward(task_id):

    """
    Mission: Move robot forward 10 cm using helper function
    """
    def when_cancelled():
        # Stop all motors when cancelled
        motor_pair.stop(MOTOR_PAIR_ID)
        motor.stop(MOTOR_PAIR_LEFT)
        motor.stop(MOTOR_PAIR_RIGHT)
    try:
        # Raise the arm using the left motor using the 2 way arm
        await move_left_motor(120)
        await move_forward(30)
        await move_backward(10)
        await move_forward(20)
        await move_left_motor(-120)
		
        loop.remove_task(task_id)
    except asyncio.CancelledError:

        when_cancelled()

async def mission_3_raise_annie(task_id):

    """
    Mission: Move arm motor B 90 degrees to the left to drop the front arm
    """
    def when_cancelled():
        # Stop arm motor when cancelled
        motor.stop(LEFT_MOTOR)
    try:

        # 
        await move_left_motor(180)
        await move_left_motor(-180)
        loop.remove_task(task_id)

    except asyncio.CancelledError:
        when_cancelled()

async def mission_2_remove_the_hook(task_id):
    """
    Mission: Remove the hook
    Uses helper functions for movement and turns
    """
    def when_cancelled():
        # Stop all motors when cancelled
        motor_pair.stop(MOTOR_PAIR_ID)
        motor.stop(MOTOR_PAIR_LEFT)
        motor.stop(MOTOR_PAIR_RIGHT)

    try:
        await move_left_motor(120)
        await move_forward(20)
        # This will latch on the loop
        await turn_right(90)
		# this will move the loop over
        await move_forward(10)
        loop.remove_task(task_id)

    except asyncio.CancelledError:
        when_cancelled()
		
async def mission_2_unearth_dig_site(task_id):
    def when_cancelled():
        # Stop all motors when cancelled
        motor_pair.stop(MOTOR_PAIR_ID)
        motor.stop(MOTOR_PAIR_LEFT)
        motor.stop(MOTOR_PAIR_RIGHT)

    try:
        await move_backward(30, speed=(int)(DEFAULT_MOVEMENT_SPEED / 2))
        await move_forward(10)
        loop.remove_task(task_id)

    except asyncio.CancelledError:
        when_cancelled()

#endregion

#region "Multiple Mission Runs along with motion between the missions to bring the bot back home"

"""#####################"""
"""# RUN FUNCTIONS    #"""
"""#####################"""
async def run1_m1_m2_m3(task_id):
    """
    Simple run: Execute forward movement, arm drop, and back and forth movement using mission functions
    """
    def when_cancelled():
        # Stop all motors when cancelled
        motor_pair.stop(MOTOR_PAIR_ID)
        motor.stop(MOTOR_PAIR_LEFT)
        motor.stop(MOTOR_PAIR_RIGHT)
        motor.stop(LEFT_MOTOR)
    try:
        # Mission 1: Move forward 10 cm using mission function
        await mission_1_raise_left_arm_move_forward_move_backward('mission_1')
        # Small delay between missions
        await asyncio.sleep_ms(500)
        # Mission 2: Move the hook
        await mission_2_remove_the_hook('mission_2')
        # Small delay between missions
        await asyncio.sleep_ms(500)
        # Mission 3: Move forward and align next to annie
        await move_forward(20)
        await mission_3_raise_annie('mission_3')

        # Small delay between missions        
        await asyncio.sleep_ms(500)
        # Mission 2: Move backwards to move the block
        await mission_2_unearth_dig_site("mission_2")
        # This will align the bot
        await turn_right(90)
		# this will bring the robot back
        await move_forward(40)
        
        loop.remove_task(task_id)
    except asyncio.CancelledError:
        when_cancelled()

#endregion


"""#####################"""
"""# DEFINE MAIN TASKS #"""
"""#####################"""

async def mainLoop():
    # Set up the simple run with both missions
    loop.add_main_task("main_task", events.when_program_starts('run_1', run1_m1_m2_m3))
    await loop.run_all_tasks()

# Run the simple run

asyncio.run(mainLoop())
