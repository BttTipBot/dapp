from datetime import datetime
from datetime import timedelta

from db.firebase import db

# Create a function that gets 1h,2h,.. or 1d,2d,.. or 1w,2w,.. or 1m,2m,.. or 1y,2y,.. or all and compute the timeback from now
def get_timeback(timeback):
    timeback = timeback.lower()
    if timeback.endswith('m'):
        minutes = int(timeback[:-1])
        return datetime.now() - timedelta(minutes=minutes)
    if timeback.endswith('h'):
        hours = int(timeback[:-1])
        return datetime.now() - timedelta(hours=hours)
    elif timeback.endswith('d'):
        days = int(timeback[:-1])
        return datetime.now() - timedelta(days=days)
    elif timeback.endswith('w'):
        weeks = int(timeback[:-1])
        return datetime.now() - timedelta(weeks=weeks)
    elif timeback.endswith('m'):
        months = int(timeback[:-1])
        return datetime.now() - timedelta(months=months)
    elif timeback.endswith('y'):
        years = int(timeback[:-1])
        return datetime.now() - timedelta(years=years)
    elif timeback == 'all':
        return datetime.now() - timedelta(days=365*10)
    else:
        return datetime.now()

def record_activity(t_username, chat_id):
    #If the user ends in bot, do not record the activity
    if t_username.lower().endswith('bot'):
        return

    # Record the transaction in the HISTORY collection
    print(f"Recording activity for {t_username} in chat_id: {chat_id}")

    date_recorded = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if the user has a chat_id in the ACTIVITY collection
    activity_ref = db.collection('ACTIVITY').where('t_username', '==', t_username).where('chat_id', '==', chat_id).limit(1)

    # Update the points in the ACTIVITY collection
    activity_data = activity_ref.get()
    if activity_data:
        points = activity_data[0].get('points')
        print(f"Updating points for {t_username} in chat_id: {chat_id} to {points + 1}")
       
       # Update the points
        activity_ref = db.collection('ACTIVITY').document(activity_data[0].id)
        activity_ref.update({
            'points': points + 1,
            'last_activity': date_recorded
        })
    else:
        history_ref = db.collection('ACTIVITY')
        history_ref.add({
            't_username': t_username,
            'chat_id': chat_id,
            'points': 1,
            'date_recorded': date_recorded,
            'last_activity': date_recorded
        })

# Get group activity
def get_activity_by_chat_id(chat_id, count=10):
    activity_ref = db.collection('ACTIVITY').where('chat_id', '==', chat_id).order_by('points', direction='DESCENDING').limit(count)
    activity_data = activity_ref.get()
    if activity_data:
        users = []
        for act in activity_data:
            user_id = act.get('t_username')
            points = act.get('points')

            # Add to users
            user = {'t_username': user_id, 'points': points}
            users.append(user)
        return users
    else:
        return []
    
def get_activity_by_t_username(t_username):
    activity_ref = db.collection('ACTIVITY').where('t_username', '==', t_username).limit(1)
    activity_data = activity_ref.get()
    if activity_data:
        return activity_data[0].get('points')
    else:
        return 0

def get_activity_by_chat_id_timeback(chat_id, timeback = '1h'):
    timeback = get_timeback(timeback)
    print(f"Timeback: {timeback}")
    activity_ref = db.collection('ACTIVITY').where('chat_id', '==', chat_id)
    activity_data = activity_ref.get()
    if activity_data:
        users = []
        for act in activity_data:
            last_activity = act.get('last_activity')
            last_activity = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
            if last_activity < timeback:
                continue
            user_id = act.get('t_username')
            points = act.get('points')

            # Add to users
            user = {'t_username': user_id, 'points': points, 'last_activity': last_activity}
            users.append(user)
        return users
    else:
        return []
   
