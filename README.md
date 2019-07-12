# visualizing-real-world-data

## Where is the best place to place my office?

On this project, we aim to locate a proper place to develop our business finding the best environment for it. The goal is to place the **new company offices** in the best place for the company to grow. For this, we define the criteria we are following, a brand-new company in the gaming industry.

The main points to consider are:
    **Team**
    - 20 Designers
    - 5 UI/UX Engineers
    - 10 Frontend Developers
    - 15 Data Engineers
    - 5 Backend Developers
    - 20 Account Managers
    - 1 Maintenance guy that loves basketball
    - 10 Executives
    - 1 CEO/President
  
   **employees preferences**
    - Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
    - 30% of the company have at least 1 child.
    - Developers like to be near successful tech startups with that have raised at least 1 Million dollars.
    - Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
    - Account managers need to travel a lot
    - All people in the company have between 25 and 40 years, give them some place to go to party.
    - Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
    - The CEO is Vegan
    
    
## What have I done?

### Main files
 - main_1_cleaning.ipynb
 - main_2_geo.ipynb
 - main_3_api_maps.ipynb

As there are several approaches to be taken, I am sure that this procedure can be enhanced. However, so far I did the following:

#### 1 Filtering dataset through MongoDB query
#### 2 Cleaning data using pandas
#### 3 Transform latitude and longitude of the selected locations into geopoints
#### 4 Load the cleaned dataset into MongoDB (with geopoints) and create an index to make geoqueries
#### 5 Use Pymongo to make geoqueries regarding the geographical proximity between each location
#### 6 Rank the best locations and pick an area

## To be done

#### 1 Improve the data analysis and data normalization
#### 2 Improve graphical representation



## Links & Resources

- https://docs.mongodb.com/manual/geospatial-queries/
- https://developers.google.com/maps/documentation/geocoding/intro
- https://data.crunchbase.com/docs
- https://developers.google.com/places/web-service/search
- https://www.youtube.com/watch?v=PtV-ZnwCjT0