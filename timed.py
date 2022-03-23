import pyttsx3
import threading

close_object = {}
violence_time = {}
times = {}


def thread_voice_alert(engine):
    engine.say("warning")
    engine.runAndWait()


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


def timer(a, b, fps):
    if times.get((a, b)) == None:
        if times.get((b, a)) != None:
            times[b, a] += 4/fps
        else:
            times[a, b] = 0
    else:
        times[a, b] += 4/fps


def del_time(a, b):
    if times.get((a, b)) == None:
        if times.get((b, a)) != None:
            del times[b, a]
        else:
            pass
    else:
        del times[a, b]


def check_time(th):
    for time in times.copy().values():
        if time > th:
            t = threading.Thread(target=thread_voice_alert, args=(engine,))
            t.start()
            times.clear()
