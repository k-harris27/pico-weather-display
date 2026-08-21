import network
import time

import open_meteo
import display
import inky_helper

def main():

    while True:
        try:
            check_network_connection()

            json = open_meteo.retrieve_forecast()

            display.draw_weather(json)

            time.sleep(30 * 60)

        except KeyboardInterrupt: raise
        except SystemExit: raise
        
        except Exception:

            time.sleep(10)
    
def check_network_connection():
    """
    A network connection should be automatically started by the firmware when the pico starts.
    It can fail for unexpected reasons (such as state.json not existing). In this case, we can connect manually.
    """
    wlan = network.WLAN(network.WLAN.IF_STA)
    attempted = False
    while not (wlan.active() and wlan.isconnected()):
        import secrets
        if attempted:
            raise RuntimeError(f"Could not connect to wifi network: {secrets.WIFI_SSID}, pass: {secrets.WIFI_PASSWORD}")
        inky_helper.network_connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        attempted = True

main()
                
