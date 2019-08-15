# incidentsmap
Enrich 911 emergency incident data to provide better analytics for a fire department.

  - This is a Django project that uses leaflet.js.
  - Minimal UI, some bootstrap is used.

# Setup (on *nix systems)
* Clone this repo
* Install Virtual Environment using python 3 (I used 3.7)
    * virtualenv --python=<your_python_3_path> env
* Activate your virtual environment
    * source env/bin/activate
* Install Python Dependencies
    * pip install -r requirements.txt
* Installing on Windows?
    * https://docs.djangoproject.com/en/2.2/howto/windows/   

# Running the Server
* cd $GIT_CLONE_DIR/incidentsmap/incidentsmap
* python ./manage.py runserver
    * I've left some debugging on the console, especially the request/response to gis data as I had trouble with it.

# Interacting with the UI
* go to http://localhost:8000
* Upload a test file. Can be found in $GIT_CLONE_DIR/incidentsmap/incidentsmap
* Design choices
     * I FAKED UP THE GIS API as I was getting a 200 OK, but a body that seemed worthless. So instead of the bounding box around the actual parcel, I took a polygon based on the incident lat/long + all deployed emergency crew's arrival lat/long.  Soooo.... This will look weird.... Sorry :(
    * Upload 1 File at a time and view the map and data.
    * If File has previously been uploaded and successfully displayed. It's saved to the database, any subsequent upload will defer to the existing record in the database.  Easiest thing to do is change the incident_number in the input json file.
    * Whenever possible, prefer to display map and data even if not all data is available.
    * If there's any notable error, it will be displayed as a text just below the upload form.


# Testing
* This project uses standard test scaffolding/framework supplied by django
    * 15 Automated Test Cases covering Sanity and missing fields within the Models.
    * python manage.py test cad (pardon the extraneous sysout logs. I didn't hook it up to a logging library).


# Other things asked for...
* Did I complete the project?
    * Mostly... See the "faked up GIS API" as mentioned above.
* How much time did I spend?
    * Not counting the 2.5 hours I was trying to debug the GIS api, I spent about 8-9 hours
* Screenshots
    * Screenshots can be found in the screenshots directory.  The filenames describe the usage.
    * PLEASE scroll to the right if viewing on github.  The screenshots are rather big, and you will miss the right half of the UI if you don't scroll.

