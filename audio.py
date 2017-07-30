import speech_recognition as sr

def _transcribe(file):
  r = sr.Recognizer()
  with sr.AudioFile(file) as source:
    audio = r.record(source)
  try:
    return r.recognize_google(audio)
  except sr.UnknownValueError:
    return ''

def _detect_speakers(result, speakers, id_):
  words = []
  for res in result['results']:
    words.extend(res['alternatives'][0]['timestamps'])

  output = []
  index = 0

  current_speaker = None

  for segment in result['speaker_labels']:
    words = []
    end = segment['to']

    while index < len(words) and words[index][-1] <= end:
      words.append(words[index][0])
      index += 1

    if words:
      output.append({
        'new': segment['speaker'] != current_speaker,
        'speaker': speakers.get(current_speaker, 'SPEAKER_{}'.format(current_speaker)),
        'transcript': words,
        'final': segment['final'],
        'id': id_,
      })

    current_speaker = segment['speaker']

  return output

def transcribe_all(file, watson, speakers):
  result, id_ = watson.recognize(file)
  return _detect_speakers(result, speakers, id_)

def train(file, watson):
  result, id_ = watson.recognize(file)
  return map(lambda l: l['speaker'], result['speaker_labels'])
