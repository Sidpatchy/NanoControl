from flask import Flask, request, Response
import setStatus
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    JSON = request.json
    print(JSON)
    
    # Parse data from webhook
    application = JSON['application']
    action = JSON['action']

    # Print the parsed data
    print('Application:', application)
    print('Action:', action)

    # Call module for function
    if action == 'on':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        print('Successfully powered on!')
    elif action == 'off':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', False)
        print('Successfully powered off!')
    elif action == 'rainbow':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'rainbow')
        print('Successfully set to rainbow!')
    elif action == 'fast rainbow':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'fastRainbow')
        print('Successfully set to fastRainbow!')
    elif action == 'cascading rainbow':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'cascadingRainbow')
        print('Successfully set to cascadingRainbow!')
    elif action == 'strip test' or action == 'strep test':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'stripTest')
        print('Successfully set to stripTest!')
    elif action == 'Christmas':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'christmas')
    elif action == 'white color':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'notSure2')
    elif action == 'not sure':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'notSure')
    elif action == 'heartbeat':
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'heartbeat')
    elif action == "pumpkin":
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'pumpkin')
    elif action == "white":
        setStatus.writeConfig('hardwareIntegration/status.yml', 'powered', True)
        setStatus.writeConfig('hardwareIntegration/status.yml', 'mode', 'white')


    return Response(status=200)
    
app.run(host='192.168.1.119',port=5000,debug=True)