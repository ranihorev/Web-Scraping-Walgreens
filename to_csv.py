from tinydb import TinyDB
import csv


def flattenjson(b, delim):
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flattenjson(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


def cities_to_csv():
    db = TinyDB('./db.json')
    f = open('./stores.csv', 'w')
    csv_writer = csv.writer(f)
    stores_table = db.table('stores_raw')
    stores = stores_table.all()

    write_headers = True
    for store in stores:
        address = f"{store['store']['address'].get('street')}, {store['store']['address'].get('city')}, {store['store']['address'].get('state')}, {store['store']['address'].get('zip')}"
        pharmacyOpenTime = store['store'].get('pharmacyOpenTime')
        pharmacyCloseTime = store['store'].get('pharmacyCloseTime')
        phoneNumber = f"{store['store']['phone']['areaCode']}-{store['store']['phone']['number']}"
        data = dict(id=store.get('storeNumber'), latitude=store.get('latitude'),
                    longitude=store.get('longitude'), mapUrl=store.get('mapUrl'), phoneNumber=phoneNumber,
                    address=address, pharmacyOpenTime=pharmacyOpenTime, pharmacyCloseTime=pharmacyCloseTime,
                    )

        if write_headers:
            # Writing headers of CSV file
            header = data.keys()
            csv_writer.writerow(header)
            write_headers = False

        csv_writer.writerow(data.values())  # ← changed
    f.close()


if __name__ == "__main__":
    cities_to_csv()
