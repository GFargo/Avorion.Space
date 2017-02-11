# Custom Server Script


Brazzers240p - https://steamid.io/lookup/STEAM_0:0:21426119
Griffeo - https://steamid.io/lookup/76561197989153725



## Setup

First we have to purchase and spin up our own VPS on one of the following providers.  I have chosen to host [avorion.space](http://avorion.space) with [Linode.com](http://linode.com) for the time being.


##### Options:

- [Linode](https://www.linode.com/pricing)
 - [Linode CLI](https://github.com/linode/cli)
- [Digital Ocean](https://www.digitalocean.com/pricing/#droplet)
- [Lightsail](https://amazonlightsail.com/pricing/)
- [Reliable Site](http://www.reliablesite.net/dedicated-servers/)
- [1and1](https://www.1and1.com/game-server-hosting)
- [NFOServers](https://www.nfoservers.com/order-virtual-dedicated-server.php)
- [WholeSale Internet](https://www.wholesaleinternet.net/dedicated/)

[Benchmark of Linode v.s. Digital Ocean v.s. Ligthsail](https://joshtronic.com/2016/12/01/ten-dollar-showdown-linode-vs-digitalocean-vs-lightsail/)

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


Update permissions on `/srv` for steam user;
`usermod -a -G steam steam` followed by `chmod g+w /srv/`

#### Sever Optimization

https://www.linux.com/blog/5-commands-check-memory-usage-linux

https://www.linuxbabe.com/ubuntu/4-tips-speed-up-ubuntu-16-04

https://sites.google.com/site/easylinuxtipsproject/speed

https://www.linode.com/docs/applications/game-servers/create-an-ark-survival-evolved-server-on-ubuntu-16-04

The following command will show the list of top processes ordered by RAM and CPU use in descendant form (remove the pipeline and head if you want to see the full list): `ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head`


Clear cached memory on Ubuntu;
`sync; sudo echo 3 > /proc/sys/vm/drop_caches`''

#### Running Server via Screen

1. Ensure `screen` package is currently installed
2. Enter `$ screen` to open up a new screen
3. Navigate to the Avorion install directory
4. Boot up server with `./server.sh` command
5. Detach current screen by entering `ctr + a` followed `d`.

You can see all screens currently running via the `$ screen -ls` command, if you wish to re-attach a screen simply use the `screen -r {screen_ID}` command.


### Backing Up Galaxies

All galaxy information is stored in the `~/.avorion/` directory in the current user's home directory.  Currently things are setup to backup directly to dropbox via the `dropbox-uploader.sh` script.

##### Restoring Backups

Unzipping a gzipped tar file is done via the `tar -xvzf community_images.tar.gz` command.


### Setting Up HTTP Server

1. Create new user via `useradd http`
2. Run `mkdir /var/www/` to create the directory for page
3. Now we need to make sure python is installed `apt-get install python`



### Custom Services

Service files on linux located `/lib/systemd/system/`

Update systemd to apply your changes: `systemctl daemon-reload`
Enable your new systemd unit and start your ARK server: `systemctl enable ark.service` & `systemctl start ark`



# Parse arugments
```
while getopts f:t: opts; do
   case ${opts} in
      n) FROM_VAL=${OPTARG} ;;
      t) TO_VAL=${OPTARG} ;;
   esac
done
```