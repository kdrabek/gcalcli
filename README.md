## Google calendar CLI

This is a simple cli that uses google calendar api to list and create calendar
events from command line.

### Examples:

```
    $ gcalcli configure  // one-time step to configure the cli
    $ gcalcli ls -s "01-01-2018" -e "31-12-2018"
    $ gcalcli add -s "06-12-2018 15:00" -e "06-12-2018 16:00" -t "Title"
```

### Installation

    To do.

    If `gcc` complains about missing `Python.h`, please make sure to install `python3-devel`
