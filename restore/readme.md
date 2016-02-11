Restores the data from the given file name. 
The filename must exist on the DB that is specified in the config file for restore.
The file is then fetched, extracted, then the data in the data container is deleted and replaced
with the extracted data, then the temporary archive files are deleted.

Requires one argument and that is the filename of the file to Restore from the FTP.

Usage example:
*  `docker-compose -f restore.yml -f ./restore/dev.yml run -d restore 2016-02-10_02-00-02__dbdata.gz`
  *  Substitute `prod` for `dev` when in development
  *  You can omit `-d` in linux, but is required for windows.