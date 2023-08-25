# Volttron IoT Demo

To start Volttron platform
``` txt
source ~/volttron/env/bin/activate
volttron-ctl shutdown --platform  # if Volttron session already starts
volttron --bind-web-address http://0.0.0.0:8282 -vv -l ~/volttron/volttron.log&
```
