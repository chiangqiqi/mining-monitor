from monitor.sms import SMSSender
from monitor.monitor import Monitor
from time import sleep

def main():
    # account like : 0x3121213232
    # tele like: '13012345678'
    monitor = Monitor('your-account')
    sender = SMSSender('your-api-key')
    tele = 'your-tele'
    while(1):
        offline_workders = monitor.get_offline_workers()

        if offline_workders:
            print('worker {0} are offline'.format(offline_workders))
            sender.send_warning(tele, offline_workders)
        else:
            print('no worker is offline')

        sleep(30)

if __name__ == '__main__':
    main()
