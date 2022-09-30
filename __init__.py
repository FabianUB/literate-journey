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

@app.route('/fh-test',methods=['POST'])
def fhWebhooks():
    data = request.json
    bookingID = data['booking']['pk']
    item = nameItem[data['booking']['availability']['item']['name']]
    affiliate = data['booking']['affiliate_company']['name']
    fecha = parse(data['booking']['availability']['start_at']).strftime("%Y-%m-%d")
    hora = parse(data['booking']['availability']['start_at']).strftime("%H:%M%p").lower()
    bruto = data['booking']['receipt_total_display']
    neto = data['booking']['invoice_price_display']
    pax = data['booking']['customer_count']

    booking = {'BOOKING ID':bookingID, 'HORA':hora, 'FECHA':fecha,'PAX':pax, 'TOTAL BRUTO':bruto,
    'TOTAL NETO':neto, 'AFILIADO':affiliate, 'PRODUCTO':item}
    print(booking)
    bookingEntry = db.put(booking, bookingID)
    return jsonify(bookingEntry, 201)

if __name__ == '__main__':
    app.run()
