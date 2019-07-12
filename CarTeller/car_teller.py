from CarBoardTeller.car_board_main import car_board_tell
from CarInfoTeller.car_info_main import car_info_tell
from CarTypeTellerMore.car_type_more_main import car_type_more_tell
from CarTypeTellerOne.car_type_one_main import car_type_one_tell
from DriverBehavior.behavior_main import behavior_tell
from CarAttributeTeller.car_attribute_main import car_attribute_tell
import os

class CarTeller:
    @staticmethod
    def car_board_tell(img):
        old = os.getcwd()
        os.chdir("./CarBoardTeller")
        try:
            temp = car_board_tell(img)
        finally:
            os.chdir(old)
        return temp

    @staticmethod
    def car_info_tell(img):
        old = os.getcwd()
        os.chdir("./CarInfoTeller")
        try:
            temp = car_info_tell(img)
        finally:
            os.chdir(old)
        return temp

    @staticmethod
    def car_type_more_tell(img):
        old = os.getcwd()
        os.chdir("./CarTypeTellerMore")
        try:
            temp = car_type_more_tell(img)
        finally:
            os.chdir(old)
        return temp

    @staticmethod
    def car_type_one_tell(img):
        old = os.getcwd()
        os.chdir("./CarTypeTellerOne")
        try:
            temp = car_type_one_tell(img)
        finally:
            os.chdir(old)
        return temp

    @staticmethod
    def behavior_tell(img):
        old = os.getcwd()
        os.chdir("./DriverBehavior")
        try:
            temp = behavior_tell(img)
        finally:
            os.chdir(old)
        return temp

    @staticmethod
    def car_attribute_tell(img):
        old = os.getcwd()
        os.chdir("./CarAttributeTeller")
        try:
            temp = car_attribute_tell(img)
        finally:
            os.chdir(old)
        return temp

'''
def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString,np.uint8)
    image = cv2.imdecode(nparr,cv2.COLOR_BAYER_BG2BGR)
    return image


if __name__ == '__main__':
    #img = Image.open("./CarTypeTellerOne/test.jpg")
    #img = cv2.imread("./CarTypeTellerMore/test.jpg")
    img=base64_cv2(str)
    print(type(img))
    #img = io.imread("./CarInfoTeller/test.jpg")
    # img = cv2.imread("./CarBoardTeller/test.jpg")
    #img = cv2.imread("./DriverBehavior/test.jpg")
    #print(CarTeller.car_info_tell(img))
    car_info_li, pros_li = CarTeller.car_info_tell(img)
'''
