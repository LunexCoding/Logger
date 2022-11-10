The module can be useful for those who do not want to fiddle with constant logging settings, or use some kind of format on a permanent basis with the ability to change settings if necessary. Written using the `logging` module.

Representing the `logger` instance and the `Logger` class

# The difference between the tools provided

As previously discovered, the `logger` instance and class `Logger`.

## logger

It is an instance of the `Logger` class. Provided with [default-parameters](#default-options), with the ability to [change](#change-settings)

## Logger

The class that will be initialized using the passed or default parameters.

# Usage

1. Clone the Logger into the project directory:

    `git clone https://github.com/LunexCoding/Logger.git`

2. Import:

    ```python
    from Logger import Logger, logger
    ```

    > For the difference between `Logger` and `logger`, see [this section](#the-difference-between-the-tools-provided)

3. If necessary, configure the logger.

# Setting

## Default options

`DEFAULT_LOG_DIR_PATH` - working directory of the logger, where logs will be created. Default `logs`

`DEFAULT_LOG_FILENAME` - the name of the log file. Default `app.log`
    
`DEFAULT_DATE_FORMAT` - date format. Default `%d-%b-%y %H:%M`
    
`DEFAULT_LOG_FORMAT` - log entry format. Default `[%(asctime)s] -> %(name)s -> [%(levelname)s]: %(message)s`

`DEFAULT_LOG_MODE` - file mode. Default `a`:
  * `w` and `w+` - If the file exists, it truncates the file.
  * `a` - Open file in append mode.

## Change settings

The `logger` object is provided with the following methods for changing parameters:

```python
logger.setLogFile(filename) # change log file name
logger.setDateFormat(dateFormat) # change date format
logger.setLogFormat(logFormat) # change log format
logger.setLogMode(mode) # change log file mode
```

> The above methods apply to a customizable logger from scratch, section below.
 
 ## Logger setup from scratch
 
 1. Import:
 
    ```python
    from Logger import Logger
    ```
    
 2. Create an object of class `Logger`:
 
 ```python
 logger = logger()
 ```
 
 ```python
 logger = Logger(dateFormat, logFormat, mode)
 ```
 
 The class constructor can take arguments:
 * `dateFormat`
 * `logFormat`
 * `mode`
 
 If they are absent, [default-parameters](#default-options) will be used.
 
 
3. Initialization of the workspace of the logger:

```python
logger.createLog()
```

```python
logger.createLog(dir, filename)
```

The `createLog` method takes arguments:
* `dir` - directory where the log file will be created.
* `filename`

If none are present, <default values> will be used.

4. Creating a registrar:

```python
log = logger.getLogger(__name__)
```

The `getLogger` method takes an argument: `name`.

5. Use [logging](https://docs.python.org/3/library/logging.html) methods

> If necessary [settings can be changed](#change-settings)

# Centralization of logging

When writing programs in a modular way using Logger, logging can be centralized. To do this, you need a new module.

1. Create a new module `logger.py` (you can use any name):

   ```python
   from Logger import Logger


   logger = logger()
   logger.createLog()
   ```

2. Adding a registrar to the required module:

    ```python
    from logger import logger

    
    log = logger.getLogger(__name__)
    ```