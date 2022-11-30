import numpy as np
import face_recognition as fr
import cv2
import sys
from time import perf_counter
from Engine import get_rostos



def Inicio(usuario,senha):
   
    rostos_conhecidos, nomes_dos_rostos = get_rostos(usuario,senha)

    video_capture = cv2.VideoCapture(0)
    nome = "Desconhecido"
    cont,start,stcont = perf_counter(),perf_counter(),0
    #while nome == "Desconhecido":
    while True:
        cont = perf_counter()-start
        
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        localizacao_dos_rostos = fr.face_locations(rgb_frame)
        rosto_desconhecidos = fr.face_encodings(rgb_frame, localizacao_dos_rostos)

        for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_dos_rostos, rosto_desconhecidos):
            resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)
            print(resultados)

            face_distances = fr.face_distance(rostos_conhecidos, rosto_desconhecido)
            
            melhor_id = np.argmin(face_distances)
            if resultados[melhor_id]:
                nome = nomes_dos_rostos[melhor_id]            
                if stcont == 0 :
                    start = perf_counter()
                    stcont = 1
            else:
                nome = "Desconhecido"
            
            # Ao redor do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Embaixo
            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX

            #Texto
            cv2.putText(frame, nome, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Webcam_facerecognition', frame)
        if nome != "Desconhecido" and cont>10 :
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()


    video_capture.release()
    cv2.destroyAllWindows()