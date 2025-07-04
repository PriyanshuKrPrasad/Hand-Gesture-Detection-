

# gesture_utils.py
def is_open_hand(landmarks):
    return all(landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20])

def is_peace_sign(landmarks):
    return landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and \
           landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y

def is_three_fingers(landmarks):
    return landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and \
           landmarks[20].y > landmarks[18].y

def is_pinch(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    return distance < 0.03
