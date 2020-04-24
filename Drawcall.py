import re
import time
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from Common import Common

# 采集内存多线程类
class DrawcallThread(QThread, Common):

    trigger = pyqtSignal(int, bool)

    def __init__(self, excel, sheet, workbook, interval, durtime, package, lock):
        super(QThread, self).__init__()
        self.excel = excel
        self.interval = interval
        self.durtime = durtime
        self.package = package
        self.sheet = sheet
        self.workbook = workbook
        self.btn_enable = False
        self.lock = lock

    def run(self):
        row = 1
        avg_sum = 0

        durtime = self.durtime.replace("min", "")
        interval = self.interval.replace("s", "")
        durtime = int(durtime)*60
        interval = int(interval)
        n = int(durtime / interval)


        for i in range(n):
            sleep_interval = 0.001
            start_time = time.time()
            if self.check_adb(self.package) == 1:
                # cmd_fps = "adb shell service call SurfaceFlinger 1013"
                cmd = "adb shell \"cat /sdcard/jjlog_fps.log\""
                res = self.execshell(cmd)
                if res.poll() is None:
                    line = res.stdout.readline().decode('utf-8', 'ignore')
                    # line = str(res.stdout.readline())
                    if 'No such file or directory' in line:
                        pass
                    else:
                        line = re.findall('Draw\scall\s\:\s(\d+)', line)
                        if line:
                            line = line.pop()
                            line = int(line)
                            self.trigger.emit(line, self.btn_enable)
                            row += 1
                            self.sheet.write(row, 15, line)


                while (time.time()-start_time)*1000000 <= interval * 1000000:
                    sleep_interval += 0.0000001
                    sleep(sleep_interval)
                end_time = time.time()
                avg = (end_time-start_time)*1000
                print("Drawcall为%f" % avg)
        self.btn_enable = True
        self.trigger.emit(0, self.btn_enable)
        self.workbook.save(self.excel)