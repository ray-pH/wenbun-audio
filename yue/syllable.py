import json
import os
from pyjyutping import jyutping

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
            # remove './' prefix from the fullpath
            fullpath = fullpath[2:]
            jytp = jyutping.convert(name)
            syllables = jytp.split(' ')
            if len(syllables) > 1:
                continue
            syl = syllables[0]
            if syl not in audio_dict:
                audio_dict[syl] = [fullpath]
            else:
                audio_dict[syl].append(fullpath)
traverse('.')

# -------------

# write audio_dict.json
with open('syllable_audio_dict.json', 'w', encoding='utf-8') as f:
    json.dump(audio_dict, f, ensure_ascii=False, indent=2)

# check for missing syllables
# missing_syllables = []
# for word in words:
#     jyutping = zh_dict[word]['jyutping']
#     syllables = jyutping.split(' ')
#     for syllable in syllables:
#         if syllable not in jyutping_syllable_to_word:
#             missing_syllables.append(syllable)

# write missing_syllables.txt
# with open('missing_syllables.txt', 'w', encoding='utf-8') as f:
#     for syllable in missing_syllables:
#         f.write(syllable + '\n')
