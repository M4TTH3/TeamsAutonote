from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QPushButton, QFileDialog, QLineEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCloseEvent
from imgstonote import ImgsToNote
import sys

class teamsnotegui(QWidget):
    
   def __init__(self, url: str, service_path: str) -> None:
      super().__init__()
      self._service = Service(service_path)
      if url == '': url = self.close()
      self._url = url

      self._driver = self.get_driver(self._url, self._service)
      self._xpath = '/html/body/div[1]/div[2]/div/div[1]/div/calling-screen/div/div[2]/div[2]/div[3]/calling-stage/div/calling-participant-stream/div/div[3]/video'
      self.content: any

      self.imgnote = ImgsToNote()

      # Make the GUI
      self.setFixedSize(300, 100)

      self.setWindowTitle('Teams Auto Gui')

      self._layout = QVBoxLayout()

      # Button for record/stop recording
      self.record_button = QPushButton('RECORD')
      self.record_button.setFixedSize(200, 20)
      self.record_button.clicked.connect(self.record)

      # Error/Support prompts
      self._status_label = QLabel('ENTER THE MEET AND PRESS "RECORD"')
      self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

      # Save button
      self.save_button = QPushButton('SAVE')
      self.save_button.setFixedSize(200, 20)
      self.save_button.clicked.connect(self.save)

      # A loop to grab the screenshots
      self._recording = QTimer()

      self.add_record_screen()
      self.setLayout(self._layout)
      self.show()

   def add_record_screen(self) -> None:
      # Initialize starting display
      self._layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)
      self._layout.addWidget(self._status_label, alignment=Qt.AlignmentFlag.AlignCenter)
      self._layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

   def closeEvent(self, event: QCloseEvent) -> None:
      "Override close function"
      self._recording.stop()
      try:
         self._driver.quit()
      except Exception:
         pass
      event.accept()

   def record(self) -> None:
      if self.record_button.text() == "RECORD" and 'https://teams.live.com/' in self._driver.current_url:

         # Initialize the element to grab the image from
         self.content = self._driver.find_element(by='xpath', value=self._xpath)

         self._recording.timeout.connect(self.update_note)
         self._recording.start(10000)
         self.record_button.setText("STOP")
         self._status_label.setText('RECORDING...')

      elif self.record_button.text() == 'STOP':
         # Stop the timer and change the button
         self._recording.stop()
         self.record_button.setText("RECORD")
         self._status_label.setText('TO ADD MORE PRESS RECORD')

      else:
         self._status_label.setText('PLEASE ENTER THE MEET')

   def update_note(self) -> None:
      try:
         img = self.content.screenshot_as_png
         self.imgnote.insert_image(img)
      except Exception: 
         # If you are no longer in the meet, it will auto-stop and prompt
         self.record()
         self.record()

   def save(self) -> None:
      if self.record_button.text() == 'STOP':
         self._recording.stop()

      self.clear_layout(self._layout)

      to_slide = QPushButton('Convert into an image slide')
      to_note = QPushButton('Convert into a note')

      to_slide.clicked.connect(lambda: self.save_note('slide'))
      to_note.clicked.connect(lambda: self.save_note('note'))

      self._layout.addWidget(to_slide)
      self._layout.addWidget(to_note)

   def save_note(self, type: str= 'note'):
      "Choose either slide or note"
      path = self.get_file_loc()
      if not path == "":
         if type == 'note':
            self.imgnote.make_note(path=path)
         elif type == 'slide':
            self.imgnote.make_slide(path=path)
         else:
            # INVALID option
            return 
         
         self.clear_layout(self._layout)
         self.new_meet()

   def new_meet(self):
      saved = QLabel()
      saved.setText('IT HAS BEEN SAVED!')
      self._layout.addWidget(saved, alignment=Qt.AlignmentFlag.AlignCenter)

   @staticmethod
   def get_file_loc() -> str:
      text = QFileDialog().getSaveFileName(filter="*.pdf")
      return text[0]

   @staticmethod
   def clear_layout(layout: QVBoxLayout) -> None:
      for i in reversed(range(layout.count())): 
         layout.itemAt(i).widget().setParent(None)

   @staticmethod
   def get_driver(url: str, service: Service) -> webdriver.Chrome:
      # Options to make browsing easier
      options = webdriver.ChromeOptions()
      options.add_argument("disable-infobars")
      options.add_argument("start-maximized")
      options.add_argument("disable-dev-shm-usage")
      options.add_argument("no-sandbox")
      options.add_experimental_option("excludeSwitches", ["enable-automation"])
      options.add_argument("disable-blink-features=AutomationControlled")

      driver = webdriver.Chrome(service=service, options=options)
      driver.get(url)
      return driver


class link_app(QLineEdit):

   def __init__(self, lst: list) -> None:
      super().__init__()
      self._list = lst

      self.setFixedSize(300, 40)
      self.setPlaceholderText('Type in your Teams Meet link and Press ENTER')
      self.returnPressed.connect(self.update_url)
      self.show()

   def update_url(self) -> str:
      self._list[0] = self.text()
      self.close()
      

if __name__ == '__main__':
   "Assuming chrome webdriver is in the same file as code"

   str = ['google.ca']
   
   get_url_app = QApplication([])
   label = link_app(str)
   get_url_app.exec()

   try:
      app = QApplication([])
      win = teamsnotegui(str[0], "/chromedriver_win32/chromedriver.exe")
      sys.exit(app.exec())

   except Exception:
      app = QApplication([])
      win = teamsnotegui('https://google.ca', "/chromedriver_win32/chromedriver.exe")
      sys.exit(app.exec())

