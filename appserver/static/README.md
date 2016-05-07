## Custom Alert Action Search Results to IFTTT 

Author: George Starcher (starcher)
Email: george@georgestarcher.com

## Overview

This is a Splunk Modular Alert used to send the search results to the IFTTT Maker Channel. It expects your search results have a column for Value1, Value2, and/or Value3. This matches what is expected from the IFTTT Maker Channel trigger.

The IFTTT Maker Channel information can be found at https://ifttt.com/maker

IFTTT is a trademark of IFTTT Inc., ifttt.com. Use of their API/Sytem is subject to their terms of service.

**All materials in this project are provided under the MIT software license. See license.txt for details.**

## Dependencies

* Splunk 6.3+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX
* An IFTTT Account
* Setup of a Maker Channel recipie

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk


## Using

Perform a search in Splunk and then navigate to : Save As -> Alert -> Trigger Actions -> Add Actions -> Send to IFTTT 

On this dialogue you can enter the event name and API key that matches the IFTTT Trigger recipie.

Keep in mind that credentials stored in a Modular Alert are NOT encrypted. And users with permissions to the saved alert can view them.

## Logging

Browse to : Settings -> Alert Actions -> Send to IFTTT -> View Log Events

Or you can search directly in Splunk : index=_internal sourcetype=splunkd component=sendmodalert action="sendtoifttt"



