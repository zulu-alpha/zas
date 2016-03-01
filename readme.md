# Installation
Copy the files *inside* `./config` to `./etc/zas/` and the *folder* `/log` to `/var/zas/`.
In a windows development environment, copy the `./config` and `./log` *folders* to `C:\Users\adam\zas\config`.

Edit the config files appropriately for the environments.
* For development, not much configuration needs to be done, except to enable debugging.
* For production, change the secrets where they appear, setup the backup FTP, and configure the nginx Config file.
  * Add in the domain name for the server and configure it for SSL, with the help of [this guide](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04).
  * Do the same for Mongo-Express and have it use a subdomain that goes to port 8081

To start in production, use `sudo docker-compose -f docker-compose.yml -f prod.yml up`
To start in development, use `docker-compose -f docker-compose.yml -f dev.yml up` for more debugging in the *web* app.
If the development environment is Linux, then you should change the paths to the config and log files in `dev.yml` to be something more meaningful.
Also if developing in linux, change the path in `dev.yml` to point to your *web* project folder.
Even in windows, if you aren't me, change instances of `adam` to your username, though that may require a lot of editing.

On production, run the `Let's Encrypt` docker image as described [here](http://letsencrypt.readthedocs.org/en/latest/using.html#running-with-docker).
Make sure to set it up for the site and for a different subdomain for Mongo-Express.
I haven't setup any mechanism for auto renewal as of yet.
You may have to set the owner and permissions of `/etc/letsencrypt/` to your user account with `sudo chown -R adam:adam /etc/letsencrypt` and 
`sudo chmod -R 755 /etc/letsencrypt` for nginx to be able to mount the certificates.

### Flask alerts and boot strap:
Use either  `success`, `info`, `warning`, `danger` for the category in `flash('message', 'category')`

### Backups
Backups are handled automatically at 4AM, however you can manually backup at any time without interrupting the schedule with the following command:
* `docker-compose -f backup.yml -f ./backup/prod.yml up`
  * or substitute `prod.yml` for `dev.yml` for a development environment
then once the backup container closes, stop the whole compose.

### Migrate
If any migrations need to be done, then modify the `migrate/migrate.py` file with your migration script and run it with:
* `docker-compose -f migrate.yml -f ./migrate/prod.yml up`
  * or substitute `prod.yml` for `dev.yml` for a development environment
then once the migration container closes, stop the whole compose.

### Restore 
To restore from backup, execute the following:
* `docker-compose -f restore.yml -f ./restore/prod.yml run restore FILE_NAME`
  * Where FILE_NAME is the name of the file on the FTP server.
  * Substitute `prod` for `dev` when in development.
  * If you are running on Windows, `-d` is required.
  
### Offices
Don't make an office with the short name `DYNAMIC`, as that is reserved by the permission system.
To add a new office, use: `/office/create`.

### Sub menus
Make certain handlers sub menus of other handlers (including dynamically generated ones) by adding
them to the MENUS list like in this example:
```python
MENUS.append({'parent_url': "url_for('office', office_name='HQ')",
              'url': "url_for('home')",
              'name': 'Home'})
```

### Ranks
To add a new rank, use: `/ranks/create`.

### Squad XML User attribute
`.xml_display` should either be `rank` or `za` to either display the user's rank or the ZA logo for
their squad xml.

### Slack
* To get a new token, go to `/slack/oauth/start`
* To force the linking of slack team members with the site, go to `/slack/sync/members`
