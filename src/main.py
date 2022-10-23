from urllib import response
from flask import Flask, request,jsonify,Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util
from bson.objectid import ObjectId 
app = Flask(__name__)

#Conexion DB
app.config['MONGO_URI']='mongodb://localhost/nosql'
mongo = PyMongo(app)


#TRAER SESSION
@app.route('/session/<id>',methods=['GET'])
def get_session(id):
    sessiones = mongo.db.sessiones.find_one({"_id":ObjectId(id)})
    datosJson = json_util.dumps(sessiones)
    return Response(datosJson,mimetype='application/json')

#CREAR SESSION
@app.route('/session',methods=['POST'])
def crear_session():
    jsonDatos = request.json

    if jsonDatos['ip'] and jsonDatos['pais'] and jsonDatos['inicioSession'] :
        datos = jsonDatos
        # datos['ip'] = jsonDatos['ip']
        # datos['pais'] = jsonDatos['pais']
        # datos['inicioSession'] = jsonDatos['inicioSession']
        # if jsonDatos['finSession']:
        #   datos['finSession'] = jsonDatos['finSession']

        idDato = mongo.db.sessiones.insert_one(datos)
        datos['id']=idDato.inserted_id
        respuesta= json_util.dumps(datos)
        return Response(respuesta,mimetype='application/json')
    else:
        respuesta= json_util.dumps({
            'estado':'Error'
        })
        return  Response(respuesta,mimetype='application/json')

#BORRAR SESSION
@app.route('/session/<id>',methods=['DELETE'])
def delete_session(id):
    borrado = mongo.db.sessiones.delete_one({"_id":ObjectId(id)})
    datosJson = json_util.dumps(borrado)
    return Response(datosJson,mimetype='application/json')

#ACTUALIZAR SESSION
@app.route('/session/<id>',methods=['PUT'])
def update_session(id):
    jsonDatos = request.json

    #if jsonDatos['ip'] or jsonDatos['pais'] or jsonDatos['inicioSession'] or jsonDatos['finSession'] :
    if jsonDatos:    
        # datos ={}
        # if jsonDatos['ip']:
        #   datos['ip'] = jsonDatos['ip']
        # if jsonDatos['pais']:
        #   datos['pais'] = jsonDatos['pais']
        # if jsonDatos['ip']:
        #   datos['inicioSession'] = jsonDatos['inicioSession']
        # if jsonDatos['finSession']:
        #   datos['finSession'] = jsonDatos['finSession']

        datos =jsonDatos

        mongo.db.sessiones.update_one({"_id":ObjectId(id)},{'$set':datos})
        respuesta= json_util.dumps({
            'msg':'Actualizado correctamente'
        })
        
        return Response(respuesta,mimetype='application/json')
    else:
        return {}


@app.route('/sessiones',methods=['GET'])
def get_sessiones():
    sessiones = mongo.db.sessiones.find()
    datosJson = json_util.dumps(sessiones)
    return Response(datosJson,mimetype='application/json')


@app.route('/sessiones_con_inicio/<desde>/<hasta>',methods=['GET'])
def get_sessiones_con_inicio(desde=None,hasta=None):
    if desde or hasta:
        dato ={}
        if desde:
            dato['$gte']=desde
        if hasta:
            dato['$lte']=hasta
        sessiones = mongo.db.sessiones.find({'inicioSession':dato})
        datosJson = json_util.dumps(sessiones)
        return Response(datosJson,mimetype='application/json')

@app.route('/sessiones_con_fin/<desde>/<hasta>',methods=['GET'])
def get_sessiones_con_fin(desde=None,hasta=None):
    if desde or hasta:
        dato ={}
        if desde:
            dato['$gte']=desde
        if hasta:
            dato['$lte']=hasta
        sessiones = mongo.db.sessiones.find({'finSession':dato})
        datosJson = json_util.dumps(sessiones)
        return Response(datosJson,mimetype='application/json')



@app.errorhandler(404)
def not_found(error=None):
    mensaje = {"estado":404,"msg":"Recurso no encontrado "+request
    .url}
    return mensaje

if __name__ == "__main__":
    app.run(debug=True)
