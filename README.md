## Steps how to start project

1. Python 3.10
2. Install poetry
3. Run `poetry install` in `project_name_directory`
4. In `maindir` create `.env` file where you need to you need to specify following:
   * SECRET_KEY=`your secret key`
   * DB_NAME=`db name`
   * DB_USER=`db user`
   * DB_PASSWORD=`db password`
   * DB_PORT=`db port`
   * DROPBOX_APP_KEY=`dropbox app key`
   * DROPBOX_APP_SECRET=`dropbox app secret`
   * DROPBOX_OAUTH2_REFRESH_TOKEN=`dropbox refresh token`
   * DROPBOX_ROOT_PATH=`dropbox root path where files will be uploaded`
5. Run `docker-compose up -d --build` and visit `127.0.0.1:8000` to start using


Py7WebProject

https://www.dropbox.com/oauth2/authorize?client_id=619zg49xua7barp&token_access_type=offline&response_type=code

curl https://api.dropbox.com/oauth2/token -d code=tqLkjb6TzhAAAAAAAAAAPXWI_xEXt9ZLd5o_L59BABE -d grant_type=authorization_code -u 619zg49xua7barp:d5elt0ogmef68rf

