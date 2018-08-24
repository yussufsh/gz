import json
from watson_developer_cloud import LanguageTranslatorV3

language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_api_key='nJaQPa0o-NFEoMDp28vtgBb5vQNIpjlxH1301ruyk45U')


def convert(text,language):
    translation = language_translator.translate(text=text, model_id=language)
    data = (json.dumps(translation, indent=2, ensure_ascii=False))
    data = json.loads(data)
    data = data['translations'][0]['translation']
#    print(data['translations'])
    print(data)
    return data

#output= convert('Dies ist eine gute Art zu essen','de-en')
#print (output)




#models = language_translator.list_models()
#print(json.dumps(models, indent=2))
