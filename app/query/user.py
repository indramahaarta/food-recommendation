from collections import OrderedDict

async def save_or_get_user_from_firestore(db: any, user: dict) -> dict:
    """Save user information to Firestore if not already exists"""
    users_ref = db.collection("User")
    user_doc = users_ref.document(user["uid"]).get()
    
    if not user_doc.exists:
        user_data = {
            "email": user.get("email"),
            "email_verified": user.get("email_verified"),
        }
        users_ref.document(user["uid"]).set(user_data)
    else:
        user_data = user_doc.to_dict()
        
    ordered_user_data = OrderedDict()
    ordered_user_data["uid"] = user["uid"]
    ordered_user_data.update(user_data)
    
    return ordered_user_data