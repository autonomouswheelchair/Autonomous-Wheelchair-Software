import platform
from check_system import CheckSystem
from initialize_model import InitializeModel
from video_processing import VideoProcessing
import cv2, torch

def main():
    os_name = platform.system()
    print('---------------------------------------------------------------------------------------------------------------------------')
    print('-------------------------------------------- AUTONOMOUS MANEUVERING WHEELCHAIR --------------------------------------------')
    print('--------------------------------------------          SYSTEM PROGRAM           --------------------------------------------')
    print('---------------- AUTHORS: AATMAJ K. MHATRE aatmaj.m@somaiya.edu, SUSHANT M. NAIR sushant.nair@somaiya.edu -----------------')
    print('----------------        PROJECT GUIDE: DR. PRASANNA J. SHETE, DEPARTMENT OF COMPUTER ENGINEERING          -----------------')
    print('---------------- © K J SOMAIYA COLLEGE OF ENGINEERING, SOMAIYA VIDYAVIHAR UNIVERSITY, ALL RIGHTS RESERVED -----------------')
    print('---------------------------------------------------------------------------------------------------------------------------')
    option = int(input('Enter \'1\' for default Port Number, Baud Rate and Time Out for Arduino Board and default Port Number for RPLIDAR else \'0\': '))
    print(os_name)
    
    if option == 1:
        if os_name == 'Windows':
            rplidar_port = 'COM3'
            arduino_port = 'COM4'
        elif os_name == 'Linux':
            rplidar_port = '/dev/ttyUSB0'
            arduino_port = '/dev/ttyACM0'
        baudrate = 9600
        timeout = .1
    else:        
        rplidar_port = input('Enter Port of Computer to which the RPLIDAR is connected: ')
        arduino_port = input('Enter Port of Computer to which the Arduino Board is connected: ')
        baudrate = int(input('Enter the Baudrate: '))
        timeout = float(input('Enter the timeout: '))

    arduino = CheckSystem.check_system(os_name, rplidar_port, arduino_port, baudrate, timeout)
    model, device = InitializeModel.initialize_model()
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = midas_transforms.small_transform
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        VideoProcessing.video_processing(frame, model, device, transform, arduino)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()