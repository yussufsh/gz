from cloudant.client import Cloudant

username = "b6b0c959-2764-4eee-91f8-a2728aa81dcf-bluemix"
password = "8447e121b3b3a45198f72b5d0f670acb0d60e4be69adb6da93b5af6acfff9a96"
url = "https://b6b0c959-2764-4eee-91f8-a2728aa81dcf-bluemix.cloudant.com"

cloudant = Cloudant(username, password, url=url, connect=True, auto_renew=True)

def createdb(dbname):
    db = cloudant.create_database(dbname, throw_on_exists=False)
    if db.exists():
        print('DB exist')
    return db
    
def createdoc(db,data):
    doc = db.create_document(data)
    if doc.exists():
        print('SUCCESS!!')
    return doc
    
def getresults(db,name,keyname,gl=None):
    result = ''
    if gl:
        result = db.get_view_result('_design/'+name,name+'_view', key=keyname, raw_result=True, group_level=2)
    else:
        result = db.get_view_result('_design/'+name,name+'_view', key=keyname, raw_result=True)
    return result

def getres(db,id):
    doc = db[id]
    return doc

def updateres(doc):
    doc.save()
    return doc
    
def disconnect():
    cloudant.disconnect