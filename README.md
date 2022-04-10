#Nearby Waste Collectors

A tool for finding the top-10 movies shot near your location. It requests 2 input parameters: Movie Release Year and Location. Using the database containing information about more than 1 million movies, the program determines the top-10 movies shot the nearest to the given location. The generation proccess may take up to 2 minutes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation proccess

You need to install two libraries: geopy and folium.

```
pip install geopy
```
```
pip install folium 
```

## Usage example

Here is an example of program usage

```
Please enter from below :
1.newspapers,old books,cardboard boxes 
2.kitchen waste
3.metal waste
4.glass items
5.plastic
6.e-waste
1
enter address: 
civil lines, new delhi, india
Input Location: India Delhi

Reading file. Wait for 5-7 seconds ...

Total of 72 collectors parsed

Too few collectors found in the area, starting deep search
-------------------------------------------------------
Found 12 collectors in 1 
 
Total collectors in Delhi: 3 
 
Total collectors in India: 9 

Finished. Please have look at the map map_2014_movies_map.html
```

This is the output file (map_2014_movies_map.html):

<img width="1280" alt="Movies Shot Near Bangui" src="https://user-images.githubusercontent.com/25267308/74776024-7b4ad180-529f-11ea-9527-f2dc642b1689.png">

## Main principles

The python code generates a HTML-file with a map using folium library. This library creates all the neccesary tags for displaying the map. The div container with folium-map class contains the map, whereas the JS code in <script> tag enables smooth user interaction. There are also some basic CSS styles applied.

## Author

**Dmytro Lopushanskyy**

## License

This project is licensed under the MIT License
