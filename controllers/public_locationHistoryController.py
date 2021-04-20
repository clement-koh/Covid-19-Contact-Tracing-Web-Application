from ..entities import Location, LocationHistory
from flask import session
from datetime import datetime

class public_locationHistoryController:
    @staticmethod
    def getLocationHistory():
        # Get result from entity
        results = LocationHistory.getLocationHistory(session['user'])
        
        # List to store results after processing
        processed_results = []
        
        # Process all results in the format to be displayed
        for result in results:
            new_result = {}
            new_result['locationID'] = Location.getName(result.location_visited)
            new_result['date'] = result.time_in.strftime('%d %b %Y') 
            new_result['time_in'] = '{:02d}:{:02d}'.format(result.time_in.hour,result.time_in.minute)
            new_result['time_out'] = '{:02d}:{:02d}'.format(result.time_out.hour,result.time_out.minute)
            
            # Add each result to the list
            processed_results.append(new_result)

        return processed_results