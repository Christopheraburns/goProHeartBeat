from goprocam import GoProCamera
from goprocam import constants
from threading import Timer

gpCam = GoProCamera.GoPro()
upTime = 0



#SSID = GP26185174
# must use 2.6GHZ network

class PerpetualTimer:
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        print('handled target')
        self._start_timer()

    def _start_timer(self):
        # Code could have been running when cancel was called.
        if self._should_continue:
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def cancel(self):
        if self.thread is not None:
            # Just in case thread is running and cancel fails.
            self._should_continue = False
            self.thread.cancel()


def takePic(imgName):
    gpCam.take_photo(0.1), "heartbeat_" + str(upTime) + ".jpg"


if __name__ == '__main__':

    def heartbeat():
        global upTime

        upTime = upTime + 5
        status = gpCam.getStatus(constants.Status.Status,constants.Status.STATUS.Mode)
        if status:
            print("Status = {}, Uptime = {}".format(status, upTime))

    t = PerpetualTimer(60, heartbeat)
    t.start()

