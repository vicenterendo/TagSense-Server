# TagSense Server

TagSense is a service that allows for external processing of aircraft tags in the `VATSIM` network.

**This is the server part of the project. For the plugin, which provides the server with the actual tag data, go to https://github.com/vicenterendo/TagSense**

**If you would like to implement TagSense on your vACC, please contact me through my e-mail address vicente.rendo@gmail.com**

---

## 📲 Instalation

Download the latest release from the [releases page](https://github.com/vicenterendo/TagSense-Server/releases) and run main.py with the arguments explained below.
**If you would like to implement TagSense on your vACC, please contact me through my e-mail address vicente.rendo@gmail.com**

---

## 💻 Command-line

These arguments customize the behavior of the server.

- `ARG` `--port <port>` Sets the port at which the server should listen.
- `ARG` `--hostname <addr>` Sets the hostname at which the server should listen.
- `ARG` `--pfx <prefix>` Sets the origin airport ICAO code filter for received flights. This filters out any flights whose origin airport's ICAO code doesn't start by the value. <sub>( "**LP**" means only fligths whose origin airport's ICAO code matches **LP**xx will be cached )</sub>
- `SWITCH` `-sqwk` Require received flights to have a valid squawk code.

---

## ⚠️ Alpha ⚠️

Still in alpha stage of development, so beware of potential bugs and/or missing features that you would assume exist.
Here is the current list of goals to achieve before officially releasing:

- [ ] Improved performance
- [ ] Better customizability
- [ ] More endpoints and features
