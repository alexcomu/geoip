#GEOIP APP

Simple Python server API built with Turbogears2 and MongoDB to retreive, from a given IP address, the geolocation. 

There is a test version that you can reach at the following link: ``http://geoip.top-ix.org``

## Installation and Setup

Install ``geoip`` using the setup.py script:

    $ pip install tg.devtools
    $ cd geoip
    $ python setup.py develop

Create the project database for any model classes defined:

    $ gearbox setup-app

Start the paste http server:

    $ gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option:

    $ gearbox serve --reload --debug

Then you are ready to go.


## API

To retreive the geo-info of an IP, we can simply implement an HTTP GET to the address ``http://myurl.com/IP-ADDRESS``. You will receive a Json response with the format:
 
    {
        status: 200,
        geoip: {
            region: "Piemonte",
            city: "Torino",
            country: "Italy",
            country_code: "IT",
            zipcode: "10133",
            longitude: "7.686820",
            latitude: "45.070490",
            timezone: "+02:00"
        }
    }

If you call in a bad way the API you will receive a response with the format:

    {
        status: 500,
        error: "We need a valid IP!"
    }
        