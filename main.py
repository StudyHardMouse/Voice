from tkinter import *
import threading
import pyaudio
import numpy as np
import time
import wave
import os
import scipy.io.wavfile as wav
import math
import winsound

def main():
    try:
        # function
        def start_check():
            while True:
                # Start Check in Noise
                # Make an Audio
                def start_audio(time=3, save_file=r"C:\test12.wav"):
                    CHUNK = 1024
                    FORMAT = pyaudio.paInt16
                    CHANNELS = 2
                    RATE = 16000
                    RECORD_SECONDS = 0.5  # 需要录制的时间
                    WAVE_OUTPUT_FILENAME = save_file  # 保存的文件名

                    p = pyaudio.PyAudio()  # 初始化
                    print("ON")

                    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)  # 创建录音文件
                    frames = []

                    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        frames.append(data)  # 开始录音

                    print("OFF")

                    stream.stop_stream()
                    stream.close()
                    p.terminate()

                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 保存
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()

                start_audio()
                # Check
                filename = r'C:\test12.wav'
                sample_rate, audio_data = wav.read(filename)
                audio_data = np.array(audio_data, dtype=float)
                amplitude = np.abs(audio_data)
                decibel = 20 * np.log10(np.clip(np.abs(amplitude), 1e-20, 1e100))
                print(type(decibel))
                list1 = decibel.tolist()
                print(len(list1))
                while True:
                    try:
                        new_list = list1.index([-400.0, -400.0])
                        b = list1.index([0.0, -400.0])
                        c = list1.index([-400.0, 0.0])
                        d = list1.index([0.0, 0.0])
                        del list1[new_list]
                        del list1[b]
                        del list1[c]
                        del list1[d]
                    except:
                        break
                fs = []
                for xs in list1:
                    for ed in xs:
                        ed = int(round(ed, 1))
                        fs.append(ed)
                if round(sum(fs) / len(fs), 1) >= 0:
                    var1.set(round(sum(fs) / len(fs), 1))
                    var2.set(round(max(fs), 1))
                else:
                    var1.set(0)
                    var2.set(0)
                if round(sum(fs) / len(fs), 1) <= 40:
                    var3.set('声音较小')
                elif round(sum(fs) / len(fs), 1) > 40 and round(sum(fs) / len(fs), 1) <= 60:
                    var3.set('声音正常')
                else:
                    var3.set('声音较大')
                win.update()
                os.remove(r'C:\test12.wav')
        # GUI
        win = Tk()
        win.geometry("814x580+167+94")
        win.minsize(116, 1)
        win.maxsize(1366, 746)
        win.resizable(1, 1)
        win.title("环境响度检测器")
        win.config(background='#ffffff')

        Label(win, background="#ffffff", foreground="#000000", text='''环境响度检测器''', font="-family {楷体} -size 36 -weight bold").place(relx=0.295, rely=0.034, height=93, width=355)
        Label(win, bg='white', fg='black', text='开发者：小金豆    v1.0   2024.01.06', font="-family {微软雅黑} -size 12").place(relx=0.356, rely=0.172, height=33, width=267)
        t1 = Text(win, bg='white', relief='solid', font=("宋体", 15))
        t1.place(relx=0.025, rely=0.241, relheight=0.728, relwidth=0.447)
        t1.insert(1.0, '噪声参考值（单位：dB）\n\n树叶沙沙声 10\n图书馆阅览室 30\n正常交谈 50——60\n繁忙商铺 65\n大型商场 70\n嘈杂的街道 80\n工厂车间 90\n电锯工作 100——110\n飞机发动机引擎 120\n火箭发射 140')
        t1.configure(state='disable')
        Label(win, bg='white', relief='groove').place(relx=0.491, rely=0.241, height=423, width=394)
        b1 = Button(win, bg='white', relief='groove', text='开始检测', command=start_check)
        b1.place(relx=0.663, rely=0.759, height=28, width=119)
        Label(win, bg='white', text='单位：分贝（dB）', font="-family {微软雅黑} -size 15").place(relx=0.504, rely=0.259, height=43, width=196)
        global var1, var2, var3
        var1 = StringVar()
        var2 = StringVar()
        var3 = StringVar()
        Label(win, bg='white', text='平均响度：', font="-family {微软雅黑} -size 15").place(relx=0.504, rely=0.379, height=43, width=105)
        Label(win, bg='white', text='最高响度：', font="-family {微软雅黑} -size 15").place(relx=0.504, rely=0.483, height=43, width=105)
        Label(win, bg='white', textvariable=var1, font="-family {叶根友毛笔行书2.0版} -size 36").place(relx=0.639, rely=0.379, height=43, width=105)
        Label(win, bg='white', textvariable=var2, font="-family {叶根友毛笔行书2.0版} -size 36").place(relx=0.639, rely=0.483, height=43, width=105)
        Label(win, bg='white', text='评价：', font="-family {微软雅黑} -size 15").place(relx=0.504, rely=0.586, height=43, width=105)
        global p1
        p1 = Label(win, bg='white', textvariable=var3, font="-family {仿宋} -size 30 -weight bold -slant italic").place(relx=0.627, rely=0.586, height=43, width=215)
        Label(win, bg='white', text='联系：xuebaxiaoshu@126.com', font="-family {微软雅黑} -size 12").place(relx=0.59, rely=0.897, height=33, width=267)

        win.mainloop()
    except Exception as e:
        print(e)
        os._exit(0)
if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=main)
        t1.start()
    except Exception as e1:
        print(e1)
        os._exit(0)