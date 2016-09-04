# android-signage-server

This is a quick and dirty server for the [Android digital signage client][c], written in [Django][d] because I needed a decent back-office and have a deadline to keep.

## Core Functionality

* Devices poll the server every few seconds
* Server returns playlists (i.e., URL/duration tuples) that clients iterate through
* Special "alert" playlists can be "pushed" to devices to playback with higher priority than current assets

## Design Constraints

Time. Also, for a number of reasons (including historical ones) HTTP polling has been the preferred mechanism to do this. In the future, however, I would love to have the time to reimplement signalling atop MQTT.

[c]: https://github.com/rcarmo/android-signage-client
[d]: https://www.djangoproject.com
