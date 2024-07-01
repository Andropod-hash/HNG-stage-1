
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def temperature(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')

    # Get client's external IP address
    try:
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip_response.raise_for_status()
        client_ip = ip_response.json()['ip']
        print(f'Retrieved client IP: {client_ip}')  # Log client IP
    except requests.RequestException as e:
        print(f'Error fetching IP address: {e}')
        client_ip = None

    # Fetch location based on IP
    if client_ip:
        try:
            ip_info_response = requests.get(f'http://ipinfo.io/{client_ip}')
            ip_info_response.raise_for_status()  # Check for HTTP errors
            ip_info_data = ip_info_response.json()
            location = ip_info_data.get('city', 'Unknown Location')
            print(f'IP Info response: {ip_info_data}')  # Debug print entire response
        except requests.RequestException as e:
            print(f'Error fetching IP info: {e}')  # Debug print error
            location = 'Unknown Location'

        # Fetch temperature for the location
        if location != 'Unknown Location':
            try:
                weather_response = requests.get(
                    f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid=43e769b33eb4f77f65c367a2670055cc&units=metric'
                )
                weather_response.raise_for_status()  # Check for HTTP errors
                weather_data = weather_response.json()
                temperature = weather_data.get('main', {}).get('temp', 'Unknown')
                print(f'Weather response: {weather_data}')  # Debug print entire response
            except requests.RequestException as e:
                print(f'Error fetching weather data: {e}')  # Debug print error
                temperature = 'Unknown'
        else:
            temperature = 'Unknown'
    else:
        location = 'Unknown Location'
        temperature = 'Unknown'

    # Construct response data
    response_data = {
        'client_ip': client_ip,
        'location': location,
        'greeting': f'Hello, {visitor_name}, the temperature is {temperature} degrees Celsius in {location}'
    }

    print(f'Response data: {response_data}')  # Debug print response data

    return Response(response_data)
