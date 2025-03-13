import arcpy


def intersect(layer_list, input_lyr_name):

    # Run a intersect analysis between the two buffer layers (needs to be a list of layers to intersect)
    arcpy.Intersect_analysis(layer_list, input_lyr_name)



def buffer_layer(input_gdb, input_layer, dist):
    # Run a buffer analysis on the input_layer with a user specified distance

    # Distance units are always miles
    units = " miles"
    dist = str(dist) + units
    # Output layer will always be named input layer + "_buf
    output_layer = input_gdb + input_layer + "_buf"
    # Always use buffer parameters FULL, ROUND, ALL
    buf_layer = input_gdb + input_layer
    arcpy.Buffer_analysis(buf_layer, output_layer,
                          dist, "FULL", "ROUND", "ALL")
    return output_layer


def main():
    # Define your workspace and point it at the modelbuilder.gdb
    gdb = "C:\\Users\\micha\\Desktop\\School\\GIS_305_Programming_forGIS\\Assignment 8\\Assignment 8\\Assignment 8.gdb\\"
    arcpy.env.workspace = gdb
    arcpy.env.overwriteOutput = True

    # Buffer cities
    input_gdb = gdb

    # Change me this next line below to use GetParamters!!
    #dist = input("What buffer distance do you want to use?")
    dist = float(arcpy.GetParameterAsText(0))

    buf_cities = buffer_layer(input_gdb, "cities", dist)


    # Change me this next line below to use GetParamters!!
    #print("Buffer layer " + buf_cities + " created.")
    arcpy.AddMessage("Buffer layer " + buf_cities + " created.")


    # Buffer rivers
    # Change me this next line below to use GetParamters!!
    #dist = input("What buffer distance do you want to use?")
    dist = float(arcpy.GetParameterAsText(1))
    buf_rivers = buffer_layer(input_gdb, "us_rivers", dist)
    #print("Buffer layer " + buf_rivers + " created.")
    arcpy.AddMessage("Buffer layer " + buf_rivers + " created.")

    # Define lyr_list variable
    # with names of input layers to intersect
    # Ask the user to define an output layer name
    # Change me this next line below to use GetParamters!!
    # intersect_lyr_name = input("What is the name for your output layer resulting from the intersect analysis? ")
    intersect_lyr_name  = arcpy.GetParameterAsText(2)
    lyr_list = [buf_rivers, buf_cities]
    intersect(lyr_list, intersect_lyr_name)
    #print(f"New intersect layer generated called: {intersect_lyr_name}")
    arcpy.AddMessage(f"New intersect layer generated called: {intersect_lyr_name}")

    # Get the project
    aprx = arcpy.mp.ArcGISProject(
        r"C:\Users\micha\Desktop\School\GIS_305_Programming_forGIS\Assignment 8\Assignment 8\Assignment 8.aprx")
    map_doc = aprx.listMaps()[0]
    map_doc.addDataFromPath(f"C:\\Users\\micha\\Desktop\\School\\GIS_305_Programming_forGIS\\Assignment 8\\Assignment 8\\Assignment 8.gdb\\{intersect_lyr_name}")

    # Get the first available map
    map_doc = aprx.listMaps()[0]

    # Define full path to the feature class
    intersect_full_path = f"{gdb}{intersect_lyr_name}"

    # Ensure the feature class exists before adding it
    if arcpy.Exists(intersect_full_path):
        # Create a feature layer in memory
        arcpy.management.MakeFeatureLayer(intersect_full_path, intersect_lyr_name)

        # Add the feature class from the GDB to the map
        map_doc.addDataFromPath(intersect_full_path)
        arcpy.AddMessage(f"Layer {intersect_lyr_name} added using addDataFromPath().")
    else:
        arcpy.AddError(f"Error: Layer {intersect_lyr_name} does NOT exist.")

    #aprx.save()


if __name__ == '__main__':
    main()