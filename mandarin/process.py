import json
import os

# load ../zh_dict.json
with open('../zh_dict.json', 'r') as f:
    zh_dict = json.load(f)

words = zh_dict.keys()

audio_dict = {}
# traverse recursively and collect all the audio files into audio_dict
def traverse(path: str):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            traverse(os.path.join(path, file))
        else:
            name = file.split('.')[0] # strip extension
            if name.startswith('cmn-'):
                name = name[4:] # strip 'cmn-' prefix
            fullpath = os.path.join(path, file)
            if name not in audio_dict:
                audio_dict[name] = [fullpath]
            else:
                audio_dict[name].append(fullpath)
traverse('.')


word_audio_dict = {}
words_with_no_audio = []
for word in words:
    if word not in audio_dict:
        word_audio_dict[word] = []
        words_with_no_audio.append(word)
    else:
        word_audio_dict[word] = audio_dict[word]

# write audio_dict.json
with open('audio_dict.json', 'w', encoding='utf-8') as f:
    json.dump(word_audio_dict, f, ensure_ascii=False, indent=2)

# write words_with_no_audio.txt
with open('words_with_no_audio.txt', 'w', encoding='utf-8') as f:
    for word in words_with_no_audio:
        f.write(word + '\n')
