from time import sleep
import cv2

def exit_handler(video_capture, led, lcd):
    video_capture.release()
    cv2.destroyAllWindows()
    sleep(0.5)

    led.color = (0.3, 0, 0)  # Red with reduced intensity
    sleep(0.3)
    led.off()
    sleep(0.3)

    print("\nExiting IntelliGuard Systems")
    
    led.color = (0, 0.3, 0)  # Green with reduced intensity
    sleep(0.3)
    led.off()
    sleep(0.3)

    lcd.clear()
    lcd.text("IntelliGuard", 1)
    lcd.text("Systems Closing", 2)

    led.color = (0, 0, 0.3)  # Blue with reduced intensity
    sleep(1)
    led.off()

    lcd.clear()  # Clear the LCD display
    exit(0)
