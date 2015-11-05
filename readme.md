# NagMe

Simple notification-center based to-do tracker with a `launchd` integration for polling.

## Install

```
python setup.py install
```

## Usage

There are 4 pieces of the system:

### addnag Service

This is a OSX Service that will take selected text, and create a new nag using that text.

To use OSX services (in most applications) right click on a piece of text, click "Services", and then click "addnag"; alternatively, you can click the application menu and "Services" > "addnag".

Firefox notably does not support services; sorry!

### nagme

Scans `~/.naglist` for the first item that has no date/time or has a date/time in the past, and sends an OSX notification about it. You can click on the notification to launch a new terminal window which will run the next command.

### nagupdate

This script is an interactive updater for your naglist. You can mark a nag as completed (ending nagging about it), or set a nag date for the item.

#### Usage:

No arguments:


```console
$ nagupdate
Select nag to update:
(0) Do a thing
(1) A different task
(4) An uncompleted task
Index: 0
Do you want to complete this nag, or update the date?
c/U: c
Completing "Do a thing"
```

Provided index (which is how the notifications trigger it):

```console
$ nagupdate 4
Do you want to complete this nag, or update the date?
c/U: u
When do you want to be nagged about 'An uncompleted task'?
10/17
You'll be nagged about 'An uncompleted task' starting 10/17/2015 at 12:00:00 AM
```

### nagfreq

The last part is managing the frequency the script is run. `nagfreq` just asks how frequently you want to be nagged (in minutes) and configures a `launchd` script to do so. You can also pass in an argument to it and skip the interactive part.

```console
$ nagcron
How frequently do you want to be reminded (in minutes)?
Minutes: 15
We'll nag you every 15 minutes
```

```console
$ nagcron 120
We'll nag you every 2 hours
```
