                 +-----------------------------+
                 |      Scheduler / Trigger     |
                 | (Cron / EventBridge / Manual)|
                 +--------------+---------------+
                                |
                                v
                 +-----------------------------+
                 |      Python Application      |
                 | (Fetch, Transform, Upload)   |
                 +--------------+---------------+
                                |
                 | (1) HTTPS Request to API
                                |
                                v
                 +-----------------------------+
                 |       OpenWeather API        |
                 +-----------------------------+
                                |
                 | (2) JSON Weather Response
                                |
                                v
                 +-----------------------------+
                 |  Data Processing & Timestamp |
                 |  - Temp (°F)                 |
                 |  - Humidity                  |
                 |  - Conditions                |
                 |  - ISO Timestamp             |
                 +---------
