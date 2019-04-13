import cognitive_face as CF

class BotMicrosoft():

    def indentificarFaceImagem(self,imgURL, key, location):
        CF.Key.set(key)

        BASE_URL = 'https://{}.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,smile,glasses,emotion,hair&recognitionModel=recognition_01&returnRecognitionModel=true'.format(location)  # Replace with your regional Base URL
        CF.BaseUrl.set(BASE_URL)

        img_url = '{}'.format(imgURL)
        result = CF.face.detect(img_url)
        result = result[0]['faceAttributes']
        response = ["{}% de chances de você estar sorrindo".format((result['smile'] * 100))]
        if (result['gender'] == 'male'):
            response.append("Você é do sexo Masculino")
        elif (result['gender'] == 'female'):
            response.append("Você é do sexo Feminino")
        if (result['glasses'] == 'NoGlasses'):
            response.append("Não usa óculos")
        else:
            response.append("Usa óculos")
        response.append("Tem por volta de {} anos".format(result['age']))
        return response