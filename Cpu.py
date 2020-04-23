# 获取cpu多线程类
import re
import time

from PyQt5.QtCore import QThread, pyqtSignal

from Common import Common


class CpuThread(QThread, Common):

    trigger = pyqtSignal(str, bool)

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
        count = 0

        durtime = self.durtime.replace("min", "")
        interval = self.interval.replace("s", "")
        durtime = int(durtime)*60
        interval = int(interval)
        interval_time = interval
        n = int(durtime / interval)
        n = str(n)
        cpuCore = 1

        name = self.get_package(self.package)
        interval = str(interval)
        cmd_cpu = "adb shell top -n " + n + " -d " + interval + " | find \""+name+"\""
        if self.check_adb(self.package) == 1:
            res = self.execshell(cmd_cpu)

            cpuInfo_res = self.execshell("adb shell \"cat /proc/cpuinfo\"")
            while cpuInfo_res.poll() is None:
                cpuInfo = cpuInfo_res.stdout.readline().decode('utf-8', 'ignore')
                if "cpu cores" in cpuInfo:
                    print(cpuInfo)
                    cpuCore = int(re.findall("cpu cores\\t\:\s(\S*)", cpuInfo).pop())
                elif "CPU architecture" in cpuInfo:
                    cpuCore = int(re.findall("CPU architecture:\s(\d)", cpuInfo).pop())

            while res.poll() is None:
                start_time = time.time()
                sleep_interval = 0.001
                line = res.stdout.readline().decode('utf-8', 'ignore')

                if name in line and "remote" not in line and "service" not in line:
                    if line != "":
                        cpu = self.format_by_re('(\d{1,2})\%', line)
                        if len(cpu) == 0:
                            cpu = re.split('\s+', line)
                            if cpu[0] == "":
                                cpu = float(cpu[9])
                            else:
                                cpu = float(cpu[8])
                            cpu = cpu/cpuCore
                            cpu = str(round(cpu, 1))
                        else:
                            cpu = cpu.pop()
                        self.trigger.emit(cpu, self.btn_enable)
                        count += 1
                        row += 1
                        self.sheet.write(row, 0, count)
                        self.sheet.write(row, 1, float(cpu))
                        while (time.time() - start_time) * 1000000 <= interval_time * 1000000:
                            sleep_interval += 0.0000001
                            time.sleep(sleep_interval)
                        end_time = time.time()
                        print("cpu为%f" % (end_time * 1000 - start_time * 1000))
            self.btn_enable = True
            self.trigger.emit('0', self.btn_enable)
            self.workbook.save(self.excel)

