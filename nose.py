import cv2
import face_recognition
from playsound import playsound

play = False
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    face_landmarks = face_recognition.face_landmarks(frame)
    
    for landmarks in face_landmarks:
        nose_landmark = landmarks.get('nose_tip', landmarks.get('nose_bridge', None))
        
        if nose_landmark is not None:
            nose_center_x = sum([x[0] for x in nose_landmark]) // len(nose_landmark)
            frame_width = frame.shape[1]
            
            neutral_space_width = frame_width // 5
            if nose_center_x < (frame_width // 2 - neutral_space_width // 2):
                cv2.putText(frame, '* Yes *', (50, 500), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 0, 255), 3)
                if not play:
                    playsound('sii.mp3')
                    play = True
            elif nose_center_x > (frame_width // 2 + neutral_space_width // 2):
                cv2.putText(frame, '* No *', (1600, 500), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 255, 0), 3)
                if not play:
                    playsound('no.mp3')
                    play = True
            else:
                play = False
                cv2.putText(frame, '* Middle *', (frame_width // 2 - 150, 200), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 255), 3)
    
    cv2.imshow('Yes or No', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
