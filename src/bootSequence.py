from time import sleep

def startup_sequence(led, lcd):
    print("\n**IntelliGuard Systems Activates, please access the local web to begin**\n")

    # Start-Up: Flash white briefly
    led.color = (0.3, 0.3, 0.3)  # White with reduced intensity
    sleep(0.3)
    led.off()
    sleep(0.3)
    
    lcd.text("IntelliGuard", 1)  # Print on the first line
    lcd.text("Systems Starting", 2)  # Print on the second line

    # Initialization
    led.color = (0.3, 0, 0)  # Red with reduced intensity
    sleep(0.3)
    led.off()
    sleep(0.3)

    led.color = (0, 0.3, 0)  # Green with reduced intensity
    sleep(0.3)
    led.off()
    sleep(0.3)

    led.color = (0, 0, 0.3)  # Blue with reduced intensity
    sleep(0.3)
    led.off()

    lcd.text("Proceed to site", 1) # Print on the first line
    lcd.text("To run system", 2) # Print on second line