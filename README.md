#Team TYB

When you're buying a house, you want to make sure the neighborhood suits you. By using our website, you can see homes for sale in New York City, and learn more about what goes on in the area around these homes. 

When you open the website, you first see a google map with red and green points around the city. The green points represent a selection of houses on sale. We generated these points by using the nyc open data API to find the latitude and longitudinal borders for all 74 precincts in New York. After we found this data, we found the center of each precinct, and then found houses on sale near these precinct centers through the zillow API. 

Near each house, you can find plenty of red points. These points are from the crime database provided by NYC open data. When you click one of these points, you can find more information about the crime. These crime points can give potential home buyers an idea of what goes on in a neighborhood. 

If you find a house you are interested in, you can click its green point for more information. Clicking a green point will give you the option to go to a listing page. On the listing page you can find out more information about the house, like it's price, and even a few photos from the Zillow API. If you click the news button, you can find a list of recent news from the neighborhood to get a better feel for the neighborhood.  

With our app, you will be able to find the perfect house!


```run pip install Flask-googlemaps```
```run pip install html5lib```
```run pip install beautifulsoup4```

