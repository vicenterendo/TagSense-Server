# TagSense Server

TagSense is a service that allows for external processing of aircraft tags in the `VATSIM` network.

**This is the server part of the project. For the plugin, which provides the server with the actual flight data, go to https://github.com/vicenterendo/TagSense**

**If you would like to implement TagSense on your vACC, please contact me through my e-mail address vicente.rendo@gmail.com**

---

## 📲 Instalation

Download the latest release from the [releases page](https://github.com/vicenterendo/TagSense-Server/releases) and run main.py with the arguments explained below.
**If you would like to implement TagSense on your vACC, please contact me through my e-mail address vicente.rendo@gmail.com**

---

## 🔧 Settings

These are the available settings. They can be changed via command line arguments or environment variables.
Each setting has an environment variable `TAGSENSE_<setting>` and one or more command line arguments.
If a `.env` file exists, it's variables will be imported.

| Name            | Command line                                                 | Type     | Description                                                                                               |
| --------------- | ------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------- |
| HOSTNAME        | `-a <hostname>` `--addr <hostname>` `--hostname <hostname>`  | String   | Sets the bind hostname.                                                                                   |
| PORT            | `-p <port>` `--port <port>`                                  | Integer  | Sets the bind port.                                                                                       |
| DATABASE_URL    | `-db <url>` `--database-url <url>`                           | String   | URL for the cache SQL database.                                                                           |
| AIRPORT_PREFIX  | `-prfx <airport_prefix>` `--airport-prefix <airport_prefix>` | String   | This filters out any flights whose origin or destination airport's ICAO code doesn't start by that value. |
| REQUIRE_SQUAWK  | `-sqwk` `--require-squawk`                                   | Boolean  | If enabled, flights without a squawk code will be filtered out.                                           |
| AUTO_CLEAN      | `-c` `--auto-clean`                                          | Boolean  | Enables the auto-cleaner feature that for automatically delete invalid flights from the database.         |
| MAX_AGE         | `-ma <max_age>` `--max-age <max_age>`                        | Integer  | Max number of seconds allowed since last update for each flight.                                          |
| VALIDATE_STORE  | `--validate-store`                                           | Boolean  | If enabled, all new flights will be validated and are only stored if valid.                               |
| DB_MAX_ATTEMPTS | `--db-max-attempts <attempts>`                               | Integer  | Defines the max number of attempts to connect to the database.                                            |
| IGNORE_ARRIVED  | `--ignore-arrived`                                           | Boolean  | If enabled, flights that have touched down at their destination will be considered invalid.               |
| CORS            | `-crs` `--cors`                                              | String[] | Specified addresses will be whitelisted in the cors header sent with all requests                         |

---

## ⚠️ Alpha ⚠️

Still in alpha stage of development, so beware of potential bugs and/or missing features that you would assume exist.
Here is the current list of goals to achieve before officially releasing:

- [ ] Improved performance
- [ ] Better customizability
- [ ] More endpoints and features
