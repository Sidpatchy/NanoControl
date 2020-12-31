var powerOnButton = document.createElement('button');
powerOnButton.id = powerOnButton;
powerOnButton.innerHTML = 'Power on';
document.body.appendChild(powerOnButton);

// This makes this incompatible with Internet Explorer 8 and earlier. Owned.
powerOnButton.addEventListener('click', powerOn);

function powerOn() {
    console.log('"Power on" button clicked');

    var URL = 'http://mox.sidpatchy.com:5000/webhook';

    // Send a post request
    fetch(URL, {
        method: "POST",
        body: JSON.stringify('json/powerOn.json'),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
}