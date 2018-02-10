from threading import Thread

from observable import Observable

obs = Observable()

def getObservable():
    print("got observable")
    return obs

def main():
    #Repeating logic goes in here
    while True:
        obs.trigger('input',{ 'soft_pot': 0 })
        return

main_thread = Thread(target=main)
main_thread.setDaemon(True)
main_thread.start()
