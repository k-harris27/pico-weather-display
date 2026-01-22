import network

import met_office
import display
import inky_helper

def main():

    check_network_connection()

    weather_json = met_office.retrieve_forecast(
        timesteps = "hourly",
        )
    location = weather_json["location"]["name"]
    timeseries = weather_json["timeSeries"]
    
    print("Debug:")
    for k,v in timeseries[0].items():
        print(f"{k}: {v}")
    
    display.draw_weather(location, timeseries)
    
def check_network_connection():
    """
    A network connection should be automatically started by the firmware when the pico starts.
    It can fail for unexpected reasons (such as state.json not existing). In this case, we can connect manually.
    """
    wlan = network.WLAN(network.WLAN.IF_STA)
    if not (wlan.active() and wlan.isconnected()):
        import secrets
        inky_helper.network_connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

main()
                
