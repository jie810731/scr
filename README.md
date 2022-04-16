## how to build

```
docker build -t scr .
```

## how to run

```
docker run -i -t --rm \
    -e BOOK_DATE='YYYY-MM-DD' \
    -e BOOK_TIME='HH,HH' \
    -e COURT_NUMBER='1' \
    -e ID='' \
    -e PASSWORD='' \
    -v "$PWD":/app
   --name scr_container scr
```

multiple account
set .env first

```
docker-compose build
```

```
docker-compose up -d
```
