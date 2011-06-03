help_text = {
    # 'Class_Name' : 'Help Text'

    'Start_Page' :
        """This is the first step to running the FleetRoute/C2RouteApp interface.  You may choose to export your data from FleetRoute to C2RouteApp for routing, or if you have already done so, you may select to import the C2RouteApp results back into FleetRoute.""",
        
    'Choose_Export_Files_Page' :
        """Prior to sending data to the C2RouteApp for routing, you must have created a shapefile with just the stops that you want to route.  Using the entire stops shapefile will not give you the proper results.

You will need to select the .dbf file from your facilities, vehicles and stops layers.  Each shapefile has several components that make up the entire shapefile, of which is a .dbf file.  Click on browse and go to 
the data_facilities folder to select the facility layer, the data_vehicles folder to select the vehicles layer and the data_stops folder to select your stops layer.  You will notice that when you go to these folders 
it will only show the .dbf file from the actual layers.""", 

    'RA_Params_Page' :
        """In this step we will select the type of routing to be performed, set the processing time, and enter your email for notification that the optimization has completed.

Select the type of routing.  There are two options for this setting:
    
    Update Sequence Existing Routes - This is used for when you have created routes in FleetRoute or have existing routes that were imported from RouteWare. This option will NOT create new routes but rather it will adjust the sequence for existing routes using the C2RouteApp point-to-point algorithm.

    Create New Routes - This is used if you have stops that you want to create new routes from scratch using the C2RouteApp point-to-point algorithm.

    Select the process run time.  The C2RouteApp can run for an extended amount of time in order to find the ultimate optimization.  In order to control or limit the time that the application will continue to look for alternative options, we have created three different settings:

    Run Until Nearly Done - C2RouteApp will run until it has achieved a set level of optimization.  At this point routes will be nearly optimized and suitable for use.

    Run Until Its Done - C2RoutApp will continue to run until it has exhausted all possibilities for optimization.

    Time Limit - Using Time Limit, you can enter a maximum amount of time to optimize your routes.  Generally speaking when you route smaller sets of data, they are mostly optimized after a five minute run time.  When using Time Limit you must enter the time in HH:MM:SS format.  Failure to do so will result in an error message.""",


    'Monitor_Optimization_Page' :
        """This page monitors the optimization process.  The elapsed time will show the running time at 5 second intervals.

Once the optimization has started the status will show 'running'.  To cancel the optimization at any time, click on 'Cancel Optimization.'  After the optimization has completed, the status will show 'terminated'.""",

    'Update_Sequence_Page' :
        """ The optimization results have downloaded.  The next step is to create a new stops shapfile with the optimization results.  Click "Finish" to complete the process.""",  

    'Download_Page' :
        """download""",
    
    'End_Page':
        """The optimization process has completed.  In the window it shows your new stops shapefile name and location, updated with the results from the optimization.""",
    
    'Start_Download_Page' :
        """start download""",
  
    'Progress' :
        """The interface is currently running.  Please wait until the next step.""",
    }
