import asyncio
from flask import Flask,request,json,jsonify
from flask_cors import CORS, cross_origin
import datetime
from dateutil.parser import parse
from deta import Deta
import os

key = os.environ.get('detaKey')
deta = Deta(key)
db = deta.Base('main')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



nameItem = {
    'Barcelona Helicopter Flight 7 Minutes':'BCNHEL06',
    'Montserrat Hot-Air Balloon Experience & Optional Monastery Visit':'BCNBALAM',
    'Montserrat Monastery & Hiking Experience':'BCNMOHAM',
    'Montserrat Monastery & Horse Riding Experience':'BCNMORAM',
    'Wine & Cava with Tapas & 4WD Vineyards Experience':'BCNPENAM',
    '360º Barcelona SkyWalk: Helicopter Flight, Walking Tour, & Boat Cruise Premium Small Group':'BCNSKYAM',
    '360º Barcelona eBike: city ride on eBike with Cable Car ticket & Sailing trip':'BCNEBIAM',
    'eBike Highlights Tour & Parc Guell skip the line ticket':'BCNHSPARK',
    'Gaudí Art Works Tour on Luxury Minibus -Sagrada Familia & Park Guell included':'BCNGAUAM',
    'Sailing Adventure from Barcelona to the vineyards, winery tour and wine tasting':'BCNALESA',
    'From Barcelona: Montserrat Monastery visit and lunch at farmhouse':'BCNMOOIL',
    'Barcelona: Markets Food Tour with a Local Chef & Tapas Workshop':'BCNMKTAPA',
    'Barcelona Market Tour & Paella Cooking Workshop with a Professional Chef':'BCNMKTCO',
    'Barcelona Paella Cooking Workshop with a Professional Chef & Lunch':'BCNCOOAM',
    'Barcelona Old Town Walking Tour, Flamenco Show & Tapas Tour Dinner in the Born District':'BCNBOFLA',
    'Barcelona Luxury Sunset Open Sailing Experience':'BCNLUIPM',
    'Three Cities in one day: Segovia, Ávila & Toledo from Madrid':'MADTRESC',
    'Toledo Premium Guided Tour: Cathedral & 8 Main Monuments with Hotel pick-up from Madrid (max 8 pax)':'MADTOLFD',
    'Toledo City Tour & Winery Experience with Wine Tasting from Madrid':'MADTOWIN',
    'Segovia Hot Air Balloon & Guided City Tour with Transfer from Madrid':'MADSEBAL',
    "Premium Winery Day Tour: Two of the Best Ribera del Duero's Wineries":"MADDUERO",
    'Madrid eBike City Tour: Highlights & Parks':'MADEBIAM',
    'Madrid eBike City Experience & Highlights Walking Guided Tour':'MADEBIWALK',
    'Madrid Segway Fun Tour: Old Town highlights (1h30m)':'MADSEG1H',
    'Madrid Segway TOP Highlights & Parque del Retiro':'MADSEG2H',
    'Madrid Local Tapas & Wine tour with Drinks & Views from Rooftop':'MADBITES',
    'Madrid Local Tapas Walking Tour & Flamenco Show':'MADTAFLA',
    'The Best of Madrid & Toledo in One Day (Prado Museum included)':'MADTOPRA',
    'Lisboa 360, bike, walk & boat':'LISEBIAM',
    '360º Lisboa SkyWalk: Old Town Walking, Helicopter flight & Sailing Waterfront':'LISSKYAM',
    'From Lisbon: Three Cities in One Day: Porto, Nazaré & Coimbra':'LISTRESC',
    'Sintra & Cabo da Roca by 4WD from Lisboa':'LISSICRO',
    'From Lisbon: Sintra with Pena Palace & Cascais with Optional Sailing Trip':'LISSICAS',
    'Sailing trip from Lisboa to Cascais and city visit':'LISCASSA',
    'Lisboa Wine tour with 4WD vineyards experience':'LISWINES',
    'Sintra with Pena Palace and Winery Experience from Lisbon':'LISSIWIN',
    'Setúbal & Beach Horse Riding from Lisbon':'LISCOHOR'
}
@app.route('/')
def hello():
    return 'Webhooks with Python'

def put_item(item, key):
    async_db = deta.Base("main")
    bookingEntry = db.put(item,key)
    return bookingEntry

@app.route('/fh-test',methods=['POST'])
def fhWebhooks():
    data = request.json
    print(data)
    bookingID = data['booking']['pk']
    item = nameItem[data['booking']['availability']['item']['name']]
    try:
        affiliate = data['booking']['affiliate_company']['name']
    except:
        affiliate = ''
    fecha = parse(data['booking']['availability']['start_at']).strftime("%Y-%m-%d")
    hora = parse(data['booking']['availability']['start_at']).strftime("%H:%M%p").lower()
    bruto = data['booking']['receipt_total_display']
    neto = data['booking']['invoice_price_display']
    pax = data['booking']['customer_count']
    ciStatus = data['booking']['customers']
    status = data['booking']['status']
    checkedin = 0
    noshow = 0
    none = 0
    try:
        for x in range(0, len(ciStatus)):
            status =  data['booking']['customers'][x]["checkin_status"]["name"]
            if status == "checked in":
                checkedin += 1
            elif status == "no-show":
                noshow += 1
            else:
                none += 1
    except:
        none = pax

    if status == 'rebooked' or status == 'cancelled':
        db.delete(str(bookingID))
        return jsonify('Booking cancelado', 201)
    else:
        booking = {'BOOKING ID':str(bookingID), 'HORA':str(hora), 'FECHA':str(fecha),'PAX':int(pax), 'TOTAL BRUTO':float(bruto),
        'TOTAL NETO':float(neto), 'AFILIADO':str(affiliate), 'PRODUCTO':str(item), 'CHECKED-IN':int(checkedin), 'NO-SHOW':int(noshow), 
        'NONE':int(none),  'COSTES FIJOS': '','COSTES VARIABLES': '','EXTRA NUMERICO': '', 'EXTRA NUMERICO TOTAL': '','EXTRA TEXTO': '',
        'PROVEEDORES FIJOS': '', 'PROVEEDORES VARIABLES': '', 'REAV': '', 'RESULTADO': '', 'EDITADO':False
        }
        print(booking)
        put_item(booking, str(bookingID))
        return jsonify(booking, 201)

if __name__ == '__main__':
    app.run(debug=True)
