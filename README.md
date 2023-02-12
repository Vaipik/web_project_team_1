### RESTful api
Api performed by using `FastAPI` framework.

#### About
Postgres is used as the database. User are able to do following things:

* Registation user using `POST` method.
* Obtain `JWT` authentication token.
* Operations with articles:
  * obtain all stored articles
  * obtain single article
  * `Only for authenticated:`
    * create new article.
    * edit existing article.
    * delete existing article.

`black` was used to format code

### Visit `/doc` or `/redoc` to see how to operate with this api

## Steps how to start project

1. Python 3.10
2. Install poetry
3. Run `poetry install` in `project_name_directory`
4. In `config` create `.env` file where you need to you need to specify following:
   * SECRET_KEY=`your secret_key`
   * SECRET_KEY=django-insecure-1lmyor=$cql0*e50_kbg6+z1k$du2g^-@fqdgf3%2e#p-7yvc=
   * DB_NAME=postgres
   * DB_USER=postgres
   * DB_PASSWORD=postgres
   * DB_PORT=5432
   * DROPBOX_APP_KEY=f2f9n89cnfrsd92
   * DROPBOX_APP_SECRET=ocfqxjt4drg0rda
   * DROPBOX_OAUTH2_REFRESH_TOKEN=R7n6o5G8dHgAAAAAAAAAAayq5ls6uMKzGuVJxYO6vLRRG6DTpam_0t3nAIVoWPo3
   * DROPBOX_ROOT_PATH=/uploads
5. And finally run `app.py` and visit `/doc` to see further information
