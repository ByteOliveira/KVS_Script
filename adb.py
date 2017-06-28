import os

class ADB(object):

    def call(self, command):
        command_result = ''
        command_text = 'adb '+command
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        return command_result

    def devices(self):
        result = self.call("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        return [device for device in devices if len(device) > 2]

    def upload(self, fr, to):
        result = self.call("push " + fr + " " + to)
        return result
    
    def get(self, fr, to):
        result = self.call("pull " + fr + " " + to)
        return result

    def install(self, param):
        result = self.call("install " + param)
        return result

    def uninstall(self, package):
        result = self.call("shell pm uninstall " + package)
        return result

    def clearData(self, package):
        result = self.call("shell pm clear " + package)
        return result

    def shell(self, command):
        result = self.call("shell " + command)
        return result
        
    def kill(self, package):
        result = self.call("kill " + package)
        return result

    def start(self, pack):
        #pack = app.split()
        result = "Nothing to run"
        if len(pack) == 1:
            result = self.call("shell am start " + pack[0])    
        elif len(pack) == 2:
            result = self.call("shell am start " + pack[0] + "/." + pack[1])
        elif len(pack) == 3:
            result = self.call("shell am start " + pack[0] + " " + pack[1] + "/." + pack[2])
        return result

    def screen(self, res):
        result = self.call("am display-size " + res)
        return result

    def dpi(self, dpi):
        result = self.call("am display-density " + dpi)
        return result

    def screenRecord(self, param):
        params = param.split()
        if params.length == 1:
            result = self.call("shell screenrecord " + params[0])
        elif params.length == 2:
            result = self.call("shell screenrecord --time-limit " + params[0] + " " + params[1])
        return result

    def screenShot(self, output):
        self.call("shell screencap -p /sdcard/temp_screen.png")
        self.get("/sdcard/temp_screen.png", output)
        self.call("shell rm /sdcard/temp_screen.png")
