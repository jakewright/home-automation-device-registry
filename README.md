# Home Automation Device Registry

## Development

### Running
You can start the device registry by typing `make start`. The service will be available at port 5001.

### Testing
You can run the test suite by typing `make test`.

## Usage
All responses will have the form:
```
{
    'message': 'Description of what happened',
    'value': 'Mixed type holding the content of the response'
}
```
Subsequent response definitions will only detail the expected value of the `value` field.

### List all devices
**Definition**

`GET /devices`

**Response**

If there are no registered devices, status code 204 will be returned.
Otherwise 200 and the payload will be a list of dictionary objects.

```
[
    {
        'identifier': 'id1',
        'name': 'Device 1',
        'deviceType': 'switch',
        'controllerGateway': '192.168.99.100:5010'
    },
    {
        'identifier': 'id2',
        'name': 'Device 2',
        'deviceType': 'bulb',
        'controllerGateway': '192.168.99.100:5011'
    }
]
```


### Register a new device
**Definition**

`POST /devices` 

**Arguments**

- `"identifier":string` a globally unique identifier for this device
- `"name":string` a friendly name for the device
- `"device-type":string` the type of the device as understood by the client
- `"controller-gateway":string` IP address of the device's controller

**Response**

If the device identifier already exists, status code 409 will be returned. 
Otherwise code 201 and the identifier will be returned as the payload.

### Lookup device details
**Definition**

`GET /device/<identifier>`

Identifier is the globally unique identifier of the device.

**Response**

Will return status 404 if the device was not found. Otherwise 200.

```
{
    'identifier': 'id1',
    'name': 'Device 1',
    'deviceType': 'switch',
    'controllerGateway': '192.168.99.100:5010'
}
```

### Delete a device
**Definition**

`DELETE /device/<identifier>`

**Response**

Will return status 400 if the device was not found. Otherwise 200. The data returned will be `True`.