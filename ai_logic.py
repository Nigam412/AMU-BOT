from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Query
from thefuzz import fuzz # <-- Nayi library import karein

engine = create_engine('sqlite:///queries.db')
Session = sessionmaker(bind=engine)
session = Session()

def generate_reply(user_msg):
    msg = user_msg.lower()
    
    best_match_response = None
    highest_score = 0
    
    # Database ke har keyword se user ke message ko compare karein
    for query in session.query(Query).all():
        
        # fuzz.token_set_ratio spelling mistakes aur extra shabdon ko handle karta hai
        # Yeh query.keyword ("mechanics tutorial") aur msg ("mechanic tutorial bhej")
        # ke beech ka similarity score dega (0 se 100 tak)
        score = fuzz.token_set_ratio(query.keyword, msg)
        
        
        # toh ise "best match" maan lo
        if score > highest_score:
            highest_score = score
            best_match_response = query.response


    # Agar sabse achha match bhi 80% se kam similar hai, toh "samajh nahi aaya" bolein
    if highest_score > 80:
        return best_match_response
    else:
        # Agar koi bhi keyword 80% se zyada match nahi hua
        return "❓ Mujhe samajh nahi aaya. Try 'physics notes' ya 'mechanics tutorial'."