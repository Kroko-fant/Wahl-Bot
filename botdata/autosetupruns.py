import io
import json
import os

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


# Server-Verzeichnis erstellen
def newserv(guild):
    newdir = './data/servers/' + str(guild.id)
    os.mkdir(newdir)


def jsonerstellen(data, newdir):
    with io.open(newdir, 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))

    # Read JSON file
    with open(newdir) as data_file:
        data_loaded = json.load(data_file)


def verifyerstellen(guild):
    data = {
    }
    newdir = './data/servers/' + str(guild.id) + '/verified.json'
    jsonerstellen(data, newdir)


def prefixzuweisen(guild):
    # Prefix zuweisen
    with open('./data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('./data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


def lastdataerstellen(guild):
    data = {
    }
    newdir = './data/servers/' + str(guild.id) + '/lastdata.json'
    jsonerstellen(data, newdir)
