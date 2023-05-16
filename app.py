from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 
import geopandas 
import os 
import contextily 
import matplotlib.pyplot as plt
from shapely.geometry import Point

quartieri = geopandas.read_file("Quartieri/NIL_WM.dbf")
quartieri3857 = quartieri.to_crs(epsg=3857)

df = pd.read_csv("https://raw.githubusercontent.com/BernasconiLorenzo06/colonnine/main/ricarica_colonnine%20(1).csv",sep = ";")
gdf_colonnine = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.LONG_X_4326, df.LAT_Y_4326), crs="EPSG:4326")
gdf_colonnine3857 = gdf_colonnine.to_crs(epsg=3857)

@app.route('/')
def home():
   
    quartier = list(quartieri3857["NIL"])
    quartier.sort()
    return render_template("home.html",lista = quartier)

@app.route('/esercizio1', methods = ["GET"])
def esercizio():
   
    
    quartiereInput = request.args.get("quartiereInput")
    quart = quartieri3857[quartieri3857["NIL"]== quartiereInput]
    colonnine_in_quartieri = gdf_colonnine3857[gdf_colonnine3857.intersects(quart.unary_union)]
    ax = quart.plot(edgecolor =  "k", facecolor = "None",figsize=(12,6))
    colonnine_in_quartieri.plot(ax=ax, edgecolor =  "blue", facecolor = "None",figsize=(12,6))
    contextily.add_basemap(ax)
        
    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio1.html")

@app.route('/esercizio2', methods = ["GET"])
def esercizio2():
    
    
    latitudine = float(request.args.get("latitudine"))
    longitudine = float(request.args.get("longitudine"))
    punto= geopandas.GeoSeries([Point(longitudine,latitudine)], crs = 4326)
    punto3857 = punto.to_crs(3857)
    colonnine_meno_500 = gdf_colonnine3857[gdf_colonnine3857.distance(punto3857.unary_union)<500]
    ax = colonnine_meno_500.plot(edgecolor =  "k", facecolor = "red",figsize=(12,6))
    punto3857.plot(ax=ax, edgecolor =  "blue", facecolor = "blue",figsize=(12,6))
    contextily.add_basemap(ax)
    dir = "static/images"
    file_name = "es2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("esercizio2.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)