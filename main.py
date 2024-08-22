from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import random,time
from mutagen.mp3 import MP3
import pygame
from pygame.locals import *
from form import Ui_MainWindow
from mutagen import File
import sys
pygame.mixer.init()
musiclist=[]
mute=False
count=0
songLength = 0
stop1=False
class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)  
        self.paused=True
        self.play=False
        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon("icon1.png"))          
        self.ui.progressbar.setTextVisible(False)       
      
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateprogressbar)          
      
        self.ui.movie=QMovie()
        self.ui.movie.setFileName("musicpl.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie.stop()        
        
        self.ui.play_btn.setIcon(QtGui.QIcon("playicon1.png"))
        self.ui.play_btn.setIconSize(QtCore.QSize(50,50))
        self.ui.stop_btn.setIcon(QtGui.QIcon("stopicn.png"))
        self.ui.stop_btn.setIconSize(QtCore.QSize(40,40)) 
        self.ui.next.setIcon(QtGui.QIcon("skipicn.png"))
        self.ui.next.setIconSize(QtCore.QSize(40,40))
        self.ui.prev.setIcon(QtGui.QIcon("revbtn.png"))
        self.ui.prev.setIconSize(QtCore.QSize(47,47))
        self.ui.repeat.setIcon(QtGui.QIcon("unmute.png"))
        self.ui.repeat.setIconSize(QtCore.QSize(40,40)) 
        #Desable widgets before playe music
        self.ui.play_btn.setEnabled(False)
        self.ui.next.setEnabled(False)
        self.ui.prev.setEnabled(False)
        self.ui.stop_btn.setEnabled(False)         
        
        self.ui.playlist.clicked.connect(self.playsong_1)
        self.ui.openfile_action.triggered.connect(self.open_file)        
        self.ui.play_btn.clicked.connect(self.play_music)        
        self.ui.stop_btn.clicked.connect(self.stop)
        self.ui.repeat.clicked.connect(self.mutesong)
        self.ui.volumeslider.valueChanged.connect(self.slide_volume)        
        self.ui.prev.clicked.connect(self.previoussong) 
        self.ui.next.clicked.connect(self.nextsong)       
       
        self.set_status()
        
        self.short_key()    
    def slide_volume(self,value):
        global mute
        self.volume=self.ui.volumeslider.value()
        if self.volume > 0 and mute == True:
           self.mutesong()  
        pygame.mixer.music.set_volume(self.volume/100)           
    def mutesong(self):
        global mute 
        _translate = QtCore.QCoreApplication.translate
        if mute == False:
            pygame.mixer.music.set_volume(0.0)
            self.ui.repeat.setIcon(QtGui.QIcon("mute.png"))
            self.ui.repeat.setIconSize(QtCore.QSize(40,40))
            self.ui.repeat.setToolTip(_translate("MainWindow", "Unmute"))
            self.ui.volumeslider.setValue(0)
            mute = True
        else:
            self.ui.repeat.setIcon(QtGui.QIcon("unmute.png"))
            self.ui.repeat.setIconSize(QtCore.QSize(40,40))   
            self.ui.repeat.setToolTip(_translate("MainWindow", "Mute"))
            self.ui.volumeslider.setValue(70)
            mute = False    
    def updateprogressbar(self):
        global count,songLength,stop1
        count +=1     
        self.ui.progressbar.setValue(count)        
        self.ui.songLengthLabel.setText(time.strftime("%M:%S",time.gmtime(count)))
        
        if count == songLength:
            self.timer.stop()
            self.ui.movie.stop()
        if stop1==True:
            count=0
            self.ui.progressbar.setValue(count)
            self.timer.stop()
            self.ui.songLengthLabel.setText(time.strftime("%M:%S",time.gmtime(count)))            
            self.ui.movie.stop()    
    def set_status(self):
        status=QStatusBar(self)        
        status.showMessage("Music Player v1.0")
        status.setStyleSheet("color: #90ee90")
        self.setStatusBar(status)
    def short_key(self):
        exit_key=QShortcut(QKeySequence("Ctrl+Q"),self)
        exit_key.activated.connect(self.close)
        exit2_key=QShortcut(QKeySequence("Ctrl+o"),self)
        exit2_key.activated.connect(self.open_file)
    def previoussong(self):
        global play,current_song,songLength,count,index
        #if play end of list back to first
        if index ==0:
            index = len(musiclist)-1
        else:
            index-=1    
        try:
            count = 0
            pygame.mixer.music.load(musiclist[index])
            pygame.mixer.music.play()
            self.ui.play_btn.setIcon(QtGui.QIcon("pauseicn.png"))
            self.ui.play_btn.setIconSize(QtCore.QSize(50,50))            
            current_song = index
            self.timer.start()
            sound = MP3(str(musiclist[index]))
            songLength = sound.info.length
            songLength =round(songLength)
            min,sec=divmod(songLength,60)
            self.ui.alllength.setText("/ "+str(min)+":"+str(sec))
            self.progressbar.setMaximum(songLength)    
        except:
            pass
    def nextsong(self):  
        global play,current_song,songLength,count,index
        if index ==len(musiclist)-1:
            index = 0
        else:
            index+=1    
        try:
            count = 0
            pygame.mixer.music.load(musiclist[index])
            pygame.mixer.music.play()
            self.ui.play_btn.setIcon(QtGui.QIcon("pauseicn.png"))
            self.ui.play_btn.setIconSize(QtCore.QSize(50,50))        
            current_song = index
            self.timer.start()
            sound = MP3(str(musiclist[index]))
            songLength = sound.info.length
            songLength =round(songLength)
            min,sec=divmod(songLength,60)
            self.ui.alllength.setText("/ "+str(min)+":"+str(sec))
            self.progressbar.setMaximum(songLength)    
        except:
            pass       
    def playsong_1(self):
        global play,current_song,songLength,count,index
        count = 0
        index = self.ui.playlist.currentRow()      
        try:
            pygame.mixer.music.load(str(musiclist[index]))
            pygame.mixer.music.play()
            self.ui.play_btn.setIcon(QtGui.QIcon("pauseicn.png"))
            self.ui.play_btn.setIconSize(QtCore.QSize(50,50))  
            self.ui.play_btn.setEnabled(True)          
            play =True
            current_song = index
            self.timer.start()
            duration=self.get_music_duration(self.file_path)        
            songLength =round(duration)         
            min,sec=divmod(songLength,60)
            self.ui.alllength.setText("/ "+str(min)+":"+str(sec))         
            self.ui.progressbar.setMaximum(songLength)            
        except:
            pass 
    def open_file(self):  
        global count,index,current_song
        count=0      
        try:
         #Open file dialog to select music and add to playlist
         self.file=QFileDialog().getOpenFileName(self,"Open Music File","c\\","MP3 (*MP3)")
         self.file_path=self.file[0]   
         musiclist.append(self.file_path)   
         self.ui.playlist.addItem(self.file_path)  
         self.ui.lstlabel.setText("Play List") 
         self.ui.stop_btn.setEnabled(True)
         self.ui.next.setEnabled(True)
         self.ui.prev.setEnabled(True)
         self.ui.play_btn.setIcon(QtGui.QIcon("pauseicn.png"))
         self.ui.play_btn.setIconSize(QtCore.QSize(50,50))         
        except:
            #if user dont select any file show message to user
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Music")
            msg.setInformativeText('you dont select any music')
            msg.setWindowTitle("Mention")
            msg.exec_()
    def play_music(self):
        global cout,songLength,stop1,index1,current_song
        index = self.ui.playlist.currentRow()
        if self.play:
           
            pygame.mixer.music.load(str(musiclist[index]))                  
            pygame.mixer.music.play()       
            current_song = index           
            self.ui.stop_btn.setEnabled(True)
            self.ui.play_btn.setIcon(QtGui.QIcon("pauseicn.png"))
            self.ui.play_btn.setIconSize(QtCore.QSize(50,50))
            if stop1:
                count=1
                self.timer.timeout.connect(self.updateprogressbar)
                self.timer.start()
                stop1=False            
            self.play=False
        elif self.paused:
            #pause
            pygame.mixer.music.pause() 
            self.ui.play_btn.setIcon(QtGui.QIcon("playicon1.png"))
            self.ui.play_btn.setIconSize(QtCore.QSize(50,50))
            self.timer.timeout.connect(self.updateprogressbar)
            self.timer.stop()
            self.ui.movie.stop()      
            
        else:
            #unpause
            pygame.mixer.music.unpause()
            self.timer.timeout.connect(self.updateprogressbar)
            self.timer.start()
            self.ui.movie.start()
            self.ui.play_btn.setIcon(QtGui.QIcon("pauseicn.png"))
            self.ui.play_btn.setIconSize(QtCore.QSize(50,50))
            self.ui.movie.start()
        self.paused=not self.paused 
            
    def repeat_mus(self):
        count=0
        pygame.mixer.music.rewind()
    def close(self):
        sys.exit()   
    def get_music_duration(self,file_path):  
     audio = File(file_path)  
     return audio.info.length if audio else None      
    def stop(self):  
        global count,stop1
        stop1=True  
        count=0        
        pygame.mixer.music.stop()
        self.ui.play_btn.setIcon(QtGui.QIcon("playicon1.png"))
        self.ui.play_btn.setIconSize(QtCore.QSize(50,50))
        self.play=True
        self.timer.timeout.connect(self.updateprogressbar)
        self.timer.stop()
        self.ui.movie.stop()     
def main():
    app=QApplication(sys.argv)
    app.setApplicationName("Music Player")
    app.setApplicationVersion("1.0")
    win=Window()
    win.show()
    sys.exit(app.exec_())
main()