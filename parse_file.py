import json


class parse:
    def __init__(self):
        self.vtx_releases_path = "vtx_releases"
        self.vtx_common_path = "vtx_common"

        self.vtx_info = {}

    def parse_vtx_common(self):
        try:
            with open(self.vtx_common_path) as file:
                lines = file.readlines()
                start = 0
                for i in range(len(lines)):
                    if start == 1:
                        words = lines[i].split()
                        for j in range(len(words)):
                            if words[j] == "defined":
                                name = words[j+1].lower()
                            if words[j] == "VTX_ID":
                                if words[j+1] != "0x00":
                                    word = words[j+1].strip("0x")
                                    self.vtx_info[name] = {"id": int(word, 16)}
                    if lines[i] == "/* define VTX ID start */\n":
                        start = 1
                    elif lines[i] == "/* define VTX ID end */\n":
                        start = 0
            a = 1
        except:
            a = 1
            print("Cant't find common")

    def parse_vtx_releases(self):
        try:
            with open(self.vtx_releases_path) as f:
                data = json.load(f)

            for i in range(len(data)):
                link_list = []
                name_list = []
                for j in range(len(data[i]['assets'])):
                    link_list.append(data[i]['assets'][j]
                                     ['browser_download_url'])

                    name_start = link_list[j].rfind('/') + len('/')
                    name_end = link_list[j].index(".zip", name_start)
                    name_list.append(link_list[j][name_start:name_end])
                    name = link_list[j][name_start:name_end]
                    if name == "hdzero_freestyle":
                        name = "hdzero_freestyle_v1"

                    version = data[i]['tag_name']
                    url = data[i]['assets'][j]['browser_download_url']
                    self.vtx_info[name][version] = url

        except:
            print()
            print("something error")


my_parse = parse()
