## Music Catalog
The project would show about music.
The table would display the album title, artist, year of release, genre and track list.
![image](https://github.com/PBraticic/PIS/assets/115488426/b9a092f0-403e-4f25-832f-4d4381edb47d)


## Features
- Add new music in track list
- Edit or delete existing music
- Filter music by track list

## Running the Backend
Application is run by docker

#### Creating a docker image
```sh
cd PIS
docker build -t musicatalog -f ./Dockerfile .
```

#### Running the docker image
```sh
docker run -p 5000:5000 musicatalog
```

## Running the frontend
Open and navigate to the frontend folder and run *index.html* with browser.
