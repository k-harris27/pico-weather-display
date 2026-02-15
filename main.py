import network

import met_office
import display
import inky_helper

def main():

    check_network_connection()

    hourly_json = met_office.retrieve_forecast(
        timesteps = "hourly",
        )
    location = hourly_json["location"]["name"]
    hourly_timeseries = hourly_json["timeSeries"]

    daily_json = met_office.retrieve_forecast(
        timesteps = "daily",
    )
    daily_timeseries = daily_json["timeSeries"]
    
    print("Debug Hourly:")
    for k,v in hourly_timeseries[0].items():
        print(f"{k}: {v}")

    print("Debug Daily:")
    for k,v in daily_timeseries[1].items():
        print(f"{k}: {v}")
    
    display.draw_weather(location, hourly_timeseries, daily_timeseries)
    
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
                
