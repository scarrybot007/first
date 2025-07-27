import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temprature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()                                    #used to align the items vertically

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temprature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)                                    #To set the layout

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temprature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")                 #used to imply style to its object name
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temprature_label.setObjectName("temprature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""                                       
            QLabel,QPushButton {
                    font-family: calibr;
                        }
            QLabel#city_label {
                    font-size: 40px;
                    font-style: italic;
                        }
            QLineEdit#city_input {
                    font-size:40px;
                        }
            QPushButton#get_weather_button {
                    font-size: 30px;
                    font-weight: bold;
                        }
            QLabel#temprature_label {
                    font-size: 70px;
                        }
            QLabel#emoji_label {
                    font-size: 100px;
                    font-family: Segoe UI Emoji;
                        }
            QLabel#description_label {
                    font-size: 50px;   
                        }
            """)                                #""" is used for multiple objects               
      
        self.get_weather_button.clicked.connect(self.get_weather)               #used to connect the fun to button


    def get_weather(self):
       
        api_key = "e33d9d532617b1d97135cac19010d23a"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"           #for city data

        try:
            response = requests.get(url)
            response.raise_for_status()                           #checks for errors
            data = response.json()

            if data["cod"] == 200:                               #200  shows the success
             self.display_weather(data)
            
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                     self.display_error("Bad request\nPlease check your input")                      #self.display is used to show the error in the window
                case 401:
                     self.display_error("Unauthorized\nInvalid API key")
                case 403:
                     self.display_error("Forbidden\nAccess denied")
                case 404:
                     self.display_error("Not Found:\nCity not found")
                case 500:
                     self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                     self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                     self.display_error("Service Unavailable:\nServer is down")
                case 504:
                     self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                     self.display_errort(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
             self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
             self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
             self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
             self.display_error(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temprature_label.setStyleSheet("font-size: 30px;")
        self.temprature_label.setText(message)                                          #displays the message
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temprature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]                                        #fetch the temp from the main dictionary as key value pair
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]                                        #weather is key, 0 is position, id is key in weather key at 0 index
     #    print(data)                                                               #to check the weather condition
        weather_description = data["weather"][0]["description"]                   #used to show the description of weather


        self.temprature_label.setText(f"{temperature_c:.0f}°C")                 #:.0f - no num will be shown after decimal pt
        self.emoji_label.setText(self.get_weather_emoji(weather_id))            #fun is called to insert the emoji from the fun
        self.description_label.setText(weather_description)                     #set the description as current weather



    @staticmethod 
    def get_weather_emoji(weather_id):
        
        if 200 <= weather_id <= 232:
            return "⛈️"                                     #thunderstorm
        elif 300 <= weather_id <= 321:
            return "☁️"                                     #clouds
        elif 500 <= weather_id <= 531:
            return "🌧️"                                     #rain
        elif 600 <= weather_id <= 622:
            return "❄️"                                     #Snow 
        elif 700 <= weather_id <= 741:
            return "🌫️"                                     #fog
        elif weather_id == 762:
            return "🌋"                                     #volcano
        elif weather_id == 771:
            return "💨"                                     #wind
        elif weather_id == 781:
            return "🌪️"                                     #tornado
        elif weather_id == 800:
            return "☀️"                                     #clear sky
        elif 801 <= weather_id <= 804:
            return "☁️"                                     #clouds
        else:
            return ""


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())