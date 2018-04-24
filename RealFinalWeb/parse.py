dis={"168 Street Station": "112", "Van Cortlandt Park - 242 St": "101", "238th Street Station": "103",
"137 St - City College": "115", "103 St": "119", "96 St": "120", "66 St - Lincoln Center Subway Station": "124",
"Times Square-42 Street": "127", "Chambers St Subway Station": "137", "South Ferry": "142", "59 St - Columbus Circle Station": "125",
"241 Street Station": "201", "E 180 St": "213", "3 Av - 149 St": "221", "135 St": "224", "14 St": "132", "Atlantic Av-Barclays Ctr": "235",
"Franklin Av": "239", "Flatbush Av - Brooklyn College": "247"}

from datetime import datetime
import json
def parseStop(gmaps,start,end):
    global dis
    now = datetime.now()
    directions_result = gmaps.directions(start,
                                         end,
                                         mode="transit",
                                         departure_time=now,
                                         alternatives=True)
    route_step=[]
    d=directions_result
    route_number=len(d)
    for i in range(route_number):
        route_info=d[i]['legs'][0]
        #print("route",i,"step number:",len(route_info['steps']),"\n")
        route_step.append(len(route_info['steps']))

    print("All route:",route_step)
    print("\n"+"*************************")

    for i in range(len(route_step)):
        print("\n","route",i+1,"info:")
        for j in range(int(route_step[i])):
            transit_step=d[i]['legs'][0]['steps'][j]
            if transit_step['travel_mode']=='TRANSIT':
                transit_detail=transit_step['transit_details']
                line_object=transit_detail['line']
                if line_object['vehicle']['type']=='SUBWAY':

                    print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line number:",line_object['short_name'],"(5)direction:",transit_detail['headsign'])
                else:
                    print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line type:",line_object['vehicle']['type'])
                    route_step[i]=None
            else:

                print("(1)route:",i+1,"(2)step:",j+1,"Walk to transit stop")


    print("\n\nSubway route:",route_step)
    print("\n"+"*************************")

    transit_array=[]
    for i in range(len(route_step)):
        if route_step[i]!=None:
            print("\n","route",i+1,"info:")
            transit_array_element=[]
            route_line= []
            transit_dict_element={}
            arrival_time=d[i]['legs'][0]['arrival_time']['text']
            print("arrival_time:",arrival_time)
            for j in range(int(route_step[i])):
                transit_step=d[i]['legs'][0]['steps'][j]
                if transit_step['travel_mode']=='TRANSIT':
                    transit_detail=transit_step['transit_details']
                    line_object=transit_detail['line']
                    route_line.append(line_object['short_name'])
                    print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line number:",line_object['short_name'],"(5)direction:",transit_detail['headsign'])
                    if(transit_detail['departure_stop']['name'] in dis):
                        temp= dis[transit_detail['departure_stop']['name']]
                        if(line_object['short_name']=="1" and transit_detail['headsign']== "South Ferry"):
                            temp+= "S"
                        elif(line_object['short_name']=="1" and transit_detail['headsign']== "Van Cortlandt Park - 242 St"):
                            temp+= "N"
                        elif(line_object['short_name']=="2" and transit_detail['headsign']== "Wakefield - 241 St"):
                            temp+= "S"
                        elif(line_object['short_name']=="2" and transit_detail['headsign']== "Flatbush Av - Brooklyn College"):
                            temp+= "N"
                    else:
                        temp= transit_detail['departure_stop']['name']
                    transit_array_element.append(temp)
                else:
                    print("(1)route:",i+1,"(2)step:",j+1,"Walk to transit stop")
            transit_dict_element['Line']=route_line
            transit_dict_element['Direction']=transit_detail['headsign']
            transit_dict_element['Stops']=transit_array_element
            transit_dict_element['Route']=i
            transit_dict_element['arrival']=arrival_time
            transit_array.append(transit_dict_element)

    #print(transit_array)


    transit_array_result=[]
    for item in transit_array:
        item=json.dumps(item)
        transit_array_result.append(item)
    transit_array_result=set(transit_array_result)

    result=[]
    for item in transit_array_result:
        item=json.loads(item)
        result.append(item)

    print("\n","Routes to be predicted:",result)
    #return render_template('transit.html')
    finalResult=[]
    for item in result:
        lineFlag=True
        stopFlag=True
        for lineItem in item['Line']:
            if lineItem!='1' and lineItem!='2':
                lineFlag=False
                break
        for stopItem in item['Stops']:
            if len(stopItem)!=4:
                stopFlag=False
                break
        if lineFlag==True and stopFlag==True:
            route_num=item['Route']
            finalResult.append(item)
    return finalResult
