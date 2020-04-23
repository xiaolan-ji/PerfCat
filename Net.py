import re
import time

from PyQt5.QtCore import QThread, pyqtSignal

from Common import Common

# 采集内存多线程类
class NetThread(QThread, Common):

    trigger = pyqtSignal(list, bool)

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
        rx_wlan = 0
        tx_wlan = 0
        wlan_total_recieve = 0
        wlan_total_send = 0

        rx_rmnet = 0
        tx_rmnet = 0
        rmnet_total_recieve = 0
        rmnet_total_send = 0


        durtime = self.durtime.replace("min", "")
        interval = self.interval.replace("s", "")
        durtime = int(durtime) * 60
        interval = int(interval)
        n = int(durtime / interval)
        name = self.get_package(self.package)

        sleep_interval = interval
        avg_sum = 0

        cmd_mem = "adb shell dumpsys package " + name + " | findstr userId"
        wlan_res = self.execshell(cmd_mem)
        userId = str(wlan_res.stdout.readline())
        userId = re.findall('userId=(\d+)', userId).pop()

        for i in range(n+1):
            if self.check_adb(self.package) == 1:
                start_time = time.time()
                sleep_interval = 0.001
                wlan_res = []
                rmnet_res = []
                cmd_mem = "adb shell \"cat /proc/net/xt_qtaguid/stats | grep " + userId
                res = self.execshell(cmd_mem)

                while res.poll() is None:
                    line = res.stdout.readline()
                    if len(line) > 0:
                        line = str(line)
                        if '1' in line.split()[4]:
                            if 'wlan' in line:
                                if rx_wlan == 0 and tx_wlan == 0:
                                    wlan_rx_bytes = int(line.split()[5])
                                    wlan_tx_bytes = int(line.split()[7])
                                    rx_wlan = wlan_rx_bytes
                                    tx_wlan = wlan_tx_bytes
                                else:
                                    wlan_rx_bytes = int(line.split()[5])
                                    wlan_tx_bytes = int(line.split()[7])
                                    wlan_recieve = (wlan_rx_bytes - rx_wlan)/1024
                                    wlan_send = (wlan_tx_bytes - tx_wlan)/1024
                                    if wlan_recieve > 0 and wlan_send > 0:
                                        wlan_recspeed = round(wlan_recieve/interval, 4)
                                        wlan_sendspeed = round(wlan_send/interval, 4)
                                        wlan_total_recieve += wlan_recieve/1024
                                        wlan_total_send += wlan_send/1024
                                        wlan_total_send = round(wlan_total_send, 4)
                                        wlan_total_recieve = round(wlan_total_recieve, 4)
                                        wlan_total = wlan_total_recieve + wlan_total_send
                                        wlan_total = round(wlan_total, 4)
                                        rx_wlan = wlan_rx_bytes
                                        tx_wlan = wlan_tx_bytes

                                        wlan_res.append(wlan_recspeed)
                                        wlan_res.append(wlan_sendspeed)
                                        wlan_res.append(wlan_total_recieve)
                                        wlan_res.append(wlan_total_send)
                                        wlan_res.append(wlan_total)

                                        self.trigger.emit(wlan_res, self.btn_enable)

                                        row += 1
                                        self.sheet.write(row, 4, wlan_recspeed)
                                        self.sheet.write(row, 5, wlan_sendspeed)
                                        self.sheet.write(row, 6, wlan_total_recieve)
                                        self.sheet.write(row, 7, wlan_total_send)
                                        self.sheet.write(row, 8, wlan_total)
                                        # self.workbook.save(self.excel)
                            if 'rmnet' in line:
                                if rx_rmnet == 0 and tx_rmnet == 0:
                                    rmnet_rx_bytes = int(line.split()[5])
                                    rmnet_tx_bytes = int(line.split()[7])
                                    rx_rmnet = rmnet_rx_bytes
                                    tx_rmnet = rmnet_tx_bytes
                                else:
                                    rmnet_rx_bytes = int(line.split()[5])
                                    rmnet_tx_bytes = int(line.split()[7])
                                    rmnet_recieve = (rmnet_rx_bytes - rx_rmnet) / 1024
                                    rmnet_send = (rmnet_tx_bytes - tx_rmnet) / 1024
                                    if rmnet_recieve > 0 and rmnet_send > 0:
                                        rmnet_recspeed = round(rmnet_recieve/interval, 4)
                                        rmnet_sendspeed = round(rmnet_send/interval, 4)
                                        rmnet_total_recieve += rmnet_recieve / 1024
                                        rmnet_total_send += rmnet_send / 1024
                                        rmnet_total_send = round(rmnet_total_send, 4)
                                        rmnet_total_recieve = round(rmnet_total_recieve, 4)
                                        rmnet_total = rmnet_total_recieve + rmnet_total_send
                                        rmnet_total = round(rmnet_total, 4)
                                        rx_rmnet = rmnet_rx_bytes
                                        tx_rmnet = rmnet_tx_bytes
                                        rmnet_res.append(rmnet_recspeed)
                                        rmnet_res.append(rmnet_sendspeed)
                                        rmnet_res.append(rmnet_total_recieve)
                                        rmnet_res.append(rmnet_total_send)
                                        rmnet_res.append(rmnet_total)

                                        self.trigger.emit(rmnet_res, self.btn_enable)

                                        row += 1
                                        self.sheet.write(row, 9, rmnet_recspeed)
                                        self.sheet.write(row, 10, rmnet_sendspeed)
                                        self.sheet.write(row, 11, rmnet_total_recieve)
                                        self.sheet.write(row, 12, rmnet_total_send)
                                        self.sheet.write(row, 13, rmnet_total)

                while (time.time() - start_time) * 1000000 <= interval * 1000000:
                    sleep_interval += 0.0000001
                    time.sleep(sleep_interval)
                end_time = time.time()
                avg = (end_time - start_time) * 1000
                avg_sum += avg
                print("net为%f" % (avg_sum / (i + 1)))
        self.btn_enable = True
        self.trigger.emit([0,0,0,0,0], self.btn_enable)
        self.workbook.save(self.excel)
