# Avorion Dedicated Server

This guide takes you through the steps required to setup your own dedicated server for [Avorion](http://store.steampowered.com/app/445220/).

[Join us on Discord](https://discord.gg/WafqdAH)

### Requirements

First we have to purchase and spin up our own VPS on one of the following providers.

- Linode
- Digital Ocean
- Lightsail

https://joshtronic.com/2016/12/01/ten-dollar-showdown-linode-vs-digitalocean-vs-lightsail/

### Mods

- [Out of Sector Production](http://www.avorion.net/forum/index.php/topic,1322.0.html)



## Setup

These steps assume you have already spun up a fresh Ubuntu instance using one of the VPS providers above.


1. Run `apt-get update && apt-get upgrade` to upgrade installed packages.
2. Follow this [getting started guide](https://www.linode.com/docs/getting-started) to prepare server
3. Follow this [sercuring your server](https://www.linode.com/docs/security/securing-your-server) guide, **skip firewall configuration**.
4. Run `sudo dpkg --add-architecture i386`
5. Run `sudo apt-get install lib32gcc1 lib32stdc++6 libc6-i386 libcurl4-gnutls-dev:i386 screen`
6. Run `sudo apt-get install steamcmd`
7. You should now have access to the `steamcmd` command, try running it in the console.  Should result
8. Once in SteamCMD, enter `login anonymous`
9. Now that we are logged in we need to install Avorion.
10. Type in `force_install_dir /your/custom/path/`
11. Next we need to download server files via `app_update 565060 validate`
12. After this is complete we can leave SteamCMD via `quit` command
13. Navigate to `/your/custom/path`
14. Start the server via `./server.sh`


#### Server Mods


- [TOOL - Mods Patch Generate & Apply](http://www.avorion.net/forum/index.php/topic,1304.0.html)

- [Out of Sector Production](http://www.avorion.net/forum/index.php/topic,1322.0.html)
- [Highlight Players in Sector](http://www.avorion.net/forum/index.php/topic,1286.0.html)
- [/sethome /inventory commands](http://www.avorion.net/forum/index.php/topic,830.0.html)
- [Wreckage Cleanup](http://www.avorion.net/forum/index.php/topic,1034.msg4628.html#msg4628)


#### Running Server via Screen


#### Backing Up Galaxies


#### Setting Up HTTP Server

1. Create new user via `useradd http`
2. Run `mkdir /var/www/` to create the directory for page
3. Now we need to make sure python is installed `apt-get install python`

#### Custom Services

Service files on linux located `/lib/systemd/system/`

Update systemd to apply your changes: `systemctl daemon-reload`
Enable your new systemd unit and start your ARK server: `systemctl enable ark.service` & `systemctl start ark`


### FAQ

* Q: How do I keep the server running after I close Terminal?
	* Using Screens, check the section above on "Running Server via Screen" for more info.

* Q:


### Resources:

- [Avorion Forums](http://www.avorion.net/forum/index.php)
- [How to Setup your Linode](http://feross.org/how-to-setup-your-linode/)
- [Avorion API Documentation for Mods](http://stonelegion.com/Avorion/Documentation/)
- [Mods List - Avorion Wiki](http://www.avorion.net/forum/index.php/topic,1100.0.html)
- [Avorion Server Console Commands](http://steamcommunity.com/app/445220/discussions/4/135508031950687754/)
- [SteamCMD - Steam Wiki](https://developer.valvesoftware.com/wiki/SteamCMD)
- [Server Setup - Avorion Wiki](http://wiki.avorion.net/index.php?title=Setting_up_a_server)
- [Upcoming Features - Avorion Wiki](http://wiki.avorion.net/index.php?title=Upcoming_Features)
- [Linode - Securing Your Server](https://www.linode.com/docs/security/securing-your-server)
- [Linode - Install SteamCMD for Steam Game Server](https://www.linode.com/docs/applications/game-servers/install-steamcmd-for-a-steam-game-server)
- [Complete Guide to Avorion](http://steamcommunity.com/sharedfiles/filedetails/?id=850693471) - A guide made with contributions from various people on the Avorion Unofficial Public Test Server.


