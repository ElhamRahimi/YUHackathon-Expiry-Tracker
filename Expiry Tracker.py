from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import cv2
import os
import numpy as np
from datetime import datetime
import pytesseract
import csv
import pandas as pd
from kivy.uix.image import Image
from kivy.core.window import Window


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class AddWindow(Screen):
    def __init__(self, **kwargs):
        super(AddWindow, self).__init__(**kwargs)
        self.btn5 = Button(text='Main Menu', size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .03})
        self.add_widget(self.btn5)
        self.btn5.bind(on_press=self.screen_transition_back)
        self.btn6 = Button(text='Camera', size_hint=(0.5, 0.2), pos_hint={'center_x': .5, 'y': .4})
        self.product = TextInput(multiline=False,  pos_hint={'center_x': .5, 'y': .26}, size_hint=(0.5, 0.09))
        self.add_widget(self.product)
        self.add_widget(self.btn6)
        self.btn6.bind(on_press=self.Cam)
        self.add_widget(Label(text='Enter Product Name: ',pos_hint={'center_x': .5, 'y': .34}, size_hint=(0.5, 0.07)))

        self.btn7 = Button(text='Submit', size_hint=(0.5, 0.1), pos_hint={'center_x': .5, 'y': .15})
        self.add_widget(self.btn7)
        self.btn7.bind(on_press=self.getProductName)
        self.btn8 = Button(text='Upload', pos_hint={'center_x': 0.5, 'y': 0.7}, size_hint=(0.5, 0.2))
        self.add_widget(self.btn8)
        self.btn8.bind(on_press=self.OpenFiles)


    # will have to call a function to receive the image taken by webcam
    # should function be triggered by the cam function or should it be triggered some other way?
    def Cam(self, *args):
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        img_counter = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                # maybe put the function for image analysis in here. call it at the end of the this elif
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()

        cv2.destroyAllWindows()
    def screen_transition_back(self, *args):
        self.manager.current = 'login'

    def getProductName(self, instance):
        productName = self.product.text
        now = datetime.now()  # current date and time
        current_year = now.strftime("%Y")
        current_year = int(current_year)
        current_month = now.strftime("%m")
        current_month = int(current_month)
        current_day = now.strftime("%d")
        current_day = int(current_day)

        product = ["", "", "", ""]

        # Import image using openCV
        image = 'createdExpiration.png'
        userImageGreyScaled = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        # Convert image to greyscale

        # ret, thresh = cv2.threshold(img, 127, 255, 0)
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cont = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        detectedText = pytesseract.image_to_string(userImageGreyScaled)
        sortedText = detectedText.split()
        print(sortedText)

        # Loop through sorted text to identify "EXP" text
        arrayLength = len(sortedText)
        position = ""
        remainder = ""
        expiryDate = ""

        for i in range(arrayLength):
            if sortedText[i] == "EXP":
                position = i
                remainder = arrayLength - position - 1

                if remainder > 1:
                    print(remainder)

                    for j in range(remainder):
                        position += 1
                        currentRead = sortedText[position]
                        if len(currentRead) == 2:
                            month = currentRead
                            print("LOL")


                        else:
                            year = currentRead
                            print("LMAO")
                        if j == remainder - 1:
                            expiryDate = year + "/" + month


                else:
                    expiryDate = sortedText[i + 1]

        slashCount = expiryDate.count("/")

        month = ""
        year = ""
        day = ""

        if slashCount == 2:
            for i in range(0, 4):
                year = year + expiryDate[i]
            for j in range(5, 7):
                month = month + expiryDate[j]
            for k in range(8, 10):
                day = day + expiryDate[k]

            product[1] = year
            product[2] = month
            product[3] = day

        else:
            for i in range(0, 4):
                year = year + expiryDate[i]
            for j in range(5, 7):
                month = month + expiryDate[j]

            day = "N/A"

            product[1] = year
            product[2] = month
            product[3] = day

        print(day)

        print("The expiration date is: ", expiryDate)
        print("year: ", year, " month:", month, " day:", day)

        product_name = productName

        product[0] = product_name

        data = [[product_name, year, month, day]]
        df = pd.DataFrame(data, columns=['Name', 'year', 'month', 'day'])

        df.to_csv("data.csv")

        g = "LOL"


    def OpenFiles(self, instance):
        path = "C:/Users"
        path = os.path.realpath(path)
        os.startfile(path)
        return


class HelpWindow(Screen):
    def __init__(self, **kwargs):
        super(HelpWindow, self).__init__(**kwargs)
        self.add_widget(Label(text='Step 1: Take a picture of your product. Ensure that the picture is clear and that the espiry date is close to the camera.', size_hint=(0.5,0.32), pos_hint={'center_x': .5, 'y':0.6}))
        self.add_widget(Label(text='Step 2: Type in the name of your product in the provided textbox after taking a picture and click submit.', size_hint=(0.5, 0.32), pos_hint={'center_x': .5, 'y': 0.5}))
        self.btn5 = Button(text='Main Menu', size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .03})
        self.add_widget(self.btn5)
        self.btn5.bind(on_press=self.screen_transition_back)

    def screen_transition_back(self, *args):
        self.manager.current = 'login'

class RegisterWindow(Screen):
    def __init__(self, **kwargs):
        # the current list of products will need to be displayed here
        # some function can maybe sort through the data base / array and spit out terms in order
        # ideally each of the terms would be stored in a variable
        # create a label for each term. Maybe create through a for loop that creates a label for each term and terminates when i = length of list from function
        super(RegisterWindow, self).__init__(**kwargs)
        self.btn5 = Button(text='Main Menu', size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .03})

        def sort():
            date = np.array([[2019, 1, 29],
                             [2020, 2, 10],
                             [2020, 5, 20], [2020, 12, 16], [2021, 7, 34]])

            sorted_array = date[np.argsort(date[:, 0])]

            x = str(sorted_array[0, :])
            x1 = str(sorted_array[1, :])
            x2 = str(sorted_array[2, :])
            x3 = str(sorted_array[3, :])
            x4 = str(sorted_array[4, :])

            return x, x1, x2, x3, x4
        x, x1, x2, x3, x4 = sort()
        #x5 = damithscode()
        self.add_widget(Label(text='Milk' +'   '+ x,size_hint=(0.5, 0.32),pos_hint={'center_x': .5, 'y': .7}))
        self.add_widget(Label(text='Poptarts' +'   '+ x1, size_hint=(0.5, 0.32),pos_hint={'center_x': .5, 'y': .6}))
        self.add_widget(Label(text='Popcorn' +'   '+x2, size_hint=(0.5, 0.32),pos_hint={'center_x': .5, 'y': .5}))
        self.add_widget(Label(text='Cream' +'   '+x3, size_hint=(0.5, 0.32),pos_hint={'center_x': .5, 'y': .4}))
        self.add_widget(Label(text='Love' +'   '+x4, size_hint=(0.5, 0.32),pos_hint={'center_x': .5, 'y': .3}))
        self.add_widget(self.btn5)
        self.btn5.bind(on_press=self.screen_transition_back)

    def screen_transition_back(self, *args):
        self.manager.current = 'login'



class LoginWindow(Screen):
        def __init__(self, **kwargs):

            super(LoginWindow, self).__init__(**kwargs)
            self.btn2 = Button(text='Add Product',pos_hint={'center_x': .5, 'y': .4},size_hint=(.45, .1))
            self.add_widget(self.btn2)
            self.btn2.bind(on_press = self.screen_transition)

            self.btn3 = Button(text = 'View Products',pos_hint={'center_x': .5, 'y': .5},size_hint=(.45, .1))
            self.add_widget(self.btn3)
            self.btn3.bind(on_press=self.screen_transition2)

            self.btn4 = Button(text='Help', pos_hint={'center_x': .5, 'y': .6}, size_hint=(.45, .1))
            self.add_widget(self.btn4)
            self.btn4.bind(on_press=self.screen_transition_help)

            bimage = Image(source="darren.png", allow_stretch="True", keep_ratio="False")

        def screen_transition(self, *args):
            self.manager.current = 'Add Product'

        def screen_transition2(self,*args):
            self.manager.current = 'View Products'

        def screen_transition_help(self,*args):
            self.manager.current = 'Help'

        def screen_transition_back(self,*args):
            self.manager.current = 'Main Menu'


class Application(App):
    def build(self):

        sm = ScreenManagement(transition=FadeTransition())
        sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(RegisterWindow(name='View Products'))
        sm.add_widget(HelpWindow(name='Help'))
        sm.add_widget(AddWindow(name='Add Product'))
        sm.add_widget(AddWindow(name='Main Menu'))
        Window.clearcolor = (151/255, 151/255, 151/255, 1)

        return sm


if __name__ == "__main__":
    Application().run()