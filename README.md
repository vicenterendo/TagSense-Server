# TagSense Server

TagSense is a service that allows for external processing of aircraft tags in the `VATSIM` network.

**This is the server part of the project. For the plugin, which provides the server with the actual flight data, go to https://github.com/vicenterendo/TagSense**

**If you would like to implement TagSense on your vACC, please contact me through my e-mail address vicente.rendo@gmail.com**

---

## 📲 Instalation

Download the latest release from the [releases page](https://github.com/vicenterendo/TagSense-Server/releases) and run main.py with the arguments explained below.
**If you would like to implement TagSense on your vACC, please contact me through my e-mail address vicente.rendo@gmail.com**

---

## 💾 Environment Variables

Environment variables are used for defining settings. If a `.env` file exists, it's variables will be imported.

| Name                    | Parsed to         | Description                                                                               |
| ----------------------- | ----------------- | ----------------------------------------------------------------------------------------- |
| TAGSENSE_HOSTNAME       | String            | Sets the bind hostname.                                                                   |
| TAGSENSE_PORT           | Integer           | Sets the bind port.                                                                       |
| TAGSENSE_DATABASE_URL   | String            | URL for the cache SQL database.                                                           |
| TAGSENSE_ORIGIN_PREFIX  | String            | This filters out any flights whose origin airport's ICAO code doesn't start by the value. |
| TAGSENSE_REQUIRE_SQUAWK | Boolean (`0`/`1`) | If enabled, flights without a squawk code will be filtered out.                           |

---

## ⚠️ Alpha ⚠️

Still in alpha stage of development, so beware of potential bugs and/or missing features that you would assume exist.
Here is the current list of goals to achieve before officially releasing:

- [ ] Improved performance
- [ ] Better customizability
- [ ] More endpoints and features
