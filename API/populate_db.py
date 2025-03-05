from app import app, get_db
import os

def add_sample_jokes():
    sample_jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Did you hear about the mathematician who’s afraid of negative numbers? He'll stop at nothing to avoid them.",
        "Why don’t scientists trust atoms? Because they make up everything!"
    ]
    
    db = get_db()
    
    try:
        for joke in sample_jokes:
            db.execute("INSERT INTO jokes (joke, user_id, upvotes, downvotes) VALUES (?, NULL, 0, 0)", (joke,))
        db.commit()
        print("✅ Sample jokes added successfully!")
    except Exception as e:
        print(f"⚠️ Error adding jokes: {e}")

if __name__ == '__main__':
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    with app.app_context():
        add_sample_jokes()
