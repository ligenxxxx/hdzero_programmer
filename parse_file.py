import json
vtx_target_list = []
vtx_version_list = []

class parse:
    def __init__(self):
        self.vtx_releases_path = "vtx_releases"
        self.vtx_common_path = "vtx_common"
        
        self.vtx_version_list = []
        self.vtx_target_list = [[]]
        self.vtx_id_list = {}
        self.vtx_fw_url = {}

    def parse_vtx_releases(self):
        try:
            with open(self.vtx_releases_path) as f:
                data = json.load(f)
            # print()
            for i in range(len(data)):
                # parser version number
                self.vtx_version_list.append(data[i]['tag_name'])
                self.vtx_fw_url.update({data[i]['tag_name']: {}})

                # parser firmware link and target name
                link_list = []
                name_list = []
                for j in range(len(data[i]['assets'])):
                    link_list.append(data[i]['assets'][j]['browser_download_url'])
                    name_start = link_list[j].rfind('/') + len('/')
                    name_end = link_list[j].index(".zip", name_start)
                    name_list.append(link_list[j][name_start:name_end])

                for j in range(1, len(name_list)):
                    self.vtx_fw_url[data[i]['tag_name']].update(
                        {name_list[j]: link_list[j - 1]})
                self.vtx_target_list.append(name_list)
            a = 1

        except:
            a = 1
            print()
            print("something error")
            
    def parse_vtx_common(self):
        try:
            with open(self.vtx_common_path) as file:
                lines = file.readlines()
                start = 0
                id_list = []
                for i in range(len(lines)):
                    if start == 1:
                        words = lines[i].split()
                        for j in range(len(words)):
                            if words[j] == "defined":
                                self.vtx_target_list[0].append(words[j+1].lower())
                            if words[j] == "VTX_ID":
                                if words[j+1] != "0x00":
                                    word = words[j+1].strip("0x")
                                    id_list.append(int(words[j+1].strip("0x"), 16))
                    if lines[i] == "/* define VTX ID start */\n":
                        start = 1
                    elif lines[i] == "/* define VTX ID end */\n":
                        start = 0

                for i in range(1, len(self.vtx_target_list[0])):
                    self.vtx_id_list.update({self.vtx_target_list[0][i]: id_list[i-1]})
                self.vtx_target_list[0][1:] = sorted(self.vtx_target_list[0][1:])
            a = 1
        except:
            a = 1
            # print("Cant't find common")
            
my_parse = parse()