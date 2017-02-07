#!/bin/sh

echo "-----"
echo "Avorion Server Deploy"
echo "-----"
echo ""
rm -rf /srv/avorion
unset GIT_DIR
git clone /srv/repo/avorion-server.git /srv/avorion


### Setup HTTP Server

# Setup Folders
rsync -rv /srv/avorion/http-server/ /var/www

# Start simpleHttpServer
/srv/avorion/bin/boot_http.sh




# rsync -rv /tmp/wp-content/ /srv/www/wordpress-live/wp-content

# printf "\n....clean up..."
# rm -rf /tmp/wp-content
# printf "\n...fixing permissions on wp_content..."
# chown -R nginx:nginx /srv/www/wordpress-live/wp-content


echo ""
echo "-----"
echo "deploy successful"
echo "------"




#!/bin/sh
git --work-tree=/srv/avorion --git-dir=/var/git/avorion-server.git checkout -f