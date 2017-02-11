from magicbot import StateMachine, state, timed_state
from components.geardepositiondevice import GearDepositionDevice
from components.gearalignmentdevice import GearAlignmentDevice
from networktables import NetworkTable
from components.vision import Vision

class ManipulateGear(StateMachine):
    gearalignmentdevice = GearAlignmentDevice
    geardepositiondevice = GearDepositionDevice
    sd = NetworkTable
    aligned = False
    vision = Vision
    checked = False
  #  lidar = int

    # example first state
    @state(first=True, must_finish=True)
    def pegAlign(self):
        # do something to align with the peg
        # now move to the next state
        #move forward
        if -0.1 <= self.vision.x <= 0.1:
            self.gearalignmentdevice.stopMotors()
            aligned = True
            self.next_state("openPistons")
        elif -0.3 <= self.vision.x <= 0.3:
            if self.vision.x > 0.1:
                self.gearalignmentdevice.align(0.5)
            if self.vision.x < 0.1:
                self.gearalignmentdevice.align(-0.5)
            aligned = False
        else:
            if self.vision.x > 0.1:
                self.gearalignmentdevice.align(1)
            if self.vision.x < 0.1:
                self.gearalignmentdevice.align(-1)
            aligned = False

    @timed_state(duration=3.0, next_state="closePistons", must_finish=True)
    def openPistons(self):
        self.geardepositiondevice.push_gear()
        self.geardepositiondevice.drop_gear()

    @state(must_finish=True)
    def closePistons(self):
        self.geardepositiondevice.retract_gear()
        self.geardepositiondevice.lock_gear()
        self.done()

    def put_dashboard(self):
        """Update all the variables on the smart dashboard"""

'''
    @state
    def measureDistance(self):
        if lidar < 5:
            if not self.checked:
                self.next_state("pegAlign")
                self.checked = True
            else:
                self.next_state("usePistons")
        else:
            self.next_state("pegAlign")
'''
