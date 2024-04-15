from libs.firebase import db

def get_risk_reward(localId):
    data = db.child("risk_reward").child(localId).get().val()

    if data:
        stoploss = data.get("stoploss")
        target = data.get("target")
    else:
        stoploss = 500
        target = 1000
    
    return stoploss, target