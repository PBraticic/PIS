## Music Catalog
The project would show about music.
The table would display the album title, artist, year of release, genre and track list.


## Features
- Add new music in track list
- Edit or delete existing music
- Filter music by track list

## Running the Backend
Application is run by docker

#### Creating a docker image
```sh
cd PIS
docker build -t musiccatalog -f ./Dockerfile .
```

#### Running the docker image
```sh
docker run -p 5000:5000 filmlist
```

## Running the frontend
Open and navigate to the frontend folder and run *index.html* with browser.