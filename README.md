
#Nearby Waste Collectors

A tool for finding waste collectors near your location. It requests 2 input parameters: type of waste you want to dispose off and Location. Using the database containing information about local waste collectors, the program determines the  collectors nearest to the given addresss. The generation proccess may take up to 2 minutes.

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

Finished. Please have look at the map https://user-images.githubusercontent.com/103133951/162619708-175c0908-4133-47a3-8a0a-7bf6ec199599.png
```

This is the output file (https://user-images.githubusercontent.com/103133951/162619708-175c0908-4133-47a3-8a0a-7bf6ec199599.png):

<img width="1007" alt="Screenshot 2022-04-10 at 6 27 11 PM" src="https://user-images.githubusercontent.com/103133951/162619708-175c0908-4133-47a3-8a0a-7bf6ec199599.png">

## Main principles

The python code generates a HTML-file with a map using folium library. This library creates all the neccesary tags for displaying the map. The div container with folium-map class contains the map, whereas the JS code in <script> tag enables smooth user interaction. There are also some basic CSS styles applied.

## Author

**Anjali Kedia, Anushka Agarwal, Pritika Kannapiran, Srijena Guin**

## License

This project is licensed under the MIT License
