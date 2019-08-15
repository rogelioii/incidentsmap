from django.db import models

class Parcel(models.Model):
    '''
    parcel enrichment
    '''
    parcel_owner_name = models.CharField(max_length=100)
    parcel_mail_address = models.TextField()
    parcel_land_value = models.FloatField()
    parcel_land_sq_ft = models.FloatField()
    

class Incident(models.Model):
    '''
    I'm taking the most interesting parts of the incidents to show
    and mapping them to a field in the db.
    '''
    incident_number = models.CharField(max_length=12)

    # taken from address
    incident_latitude = models.FloatField()
    incident_longitude = models.FloatField()

    # concatted value for display.
    incident_address_string = models.CharField(max_length=200)

    # TODO: change to enums
    incident_type = models.CharField(max_length=100)
    incident_sub_type = models.CharField(max_length=100)
    incident_day_of_week = models.CharField(max_length=8)

    incident_event_opened = models.DateTimeField(auto_now_add=False) 
    incident_event_closed = models.DateTimeField(auto_now_add=False) 
    incident_response_zone = models.CharField(max_length=10)
    incident_parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    
    # TODO: change to array
    incident_units_involved = models.CharField(max_length=200)

    '''
    there are others we can add here, like all the different 
    units that responded.
    '''

    # Enrichment
    # -- Weather
    incident_weather_description = models.TextField()



