import os
import sys
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs


def fetch_additional(class_id: str):
    url = "https://sylabusy.agh.edu.pl/en/document/" + class_id + ".jsonHtml"
    r = requests.get(url)
    soup = bs(r.json()["html"], "lxml")
    
    additional_info = {}
    additional_info["subject_coordinator"] = [x.strip() for x in soup.find("div", {"class": "head-author-right"}).text.strip().split(",")]
    additional_info["lecturers"] = [x.strip() for x in soup.find("div", {"class": "head-teachers-right"}).text.strip().split(",")]
    additional_info["class_code"] = soup.find_all("div", {"class": "head-body-cell-content"})[7].text.strip()
    additional_info["lecture_languages"] = soup.find_all("div", {"class": "head-body-cell-content"})[8].text.strip()
    additional_info["mandatory"] = soup.find_all("div", {"class": "head-body-cell-content"})[9].text.strip()

    return additional_info


def parse_class(htlm_piece):
    try:
        class_dict = {}
        class_id = htlm_piece.find("div", {"class": "syl-get-document syl-pointer"}).get('id')
        class_name = htlm_piece.find("div", {"class": "syl-get-document syl-pointer"}).text.strip()
        class_info = htlm_piece.find_all("td")        
    
        class_types = [x.strip() for x in class_info[1].text.strip().splitlines()]
        class_dict["ects_points"] = class_info[2].text.strip()
        class_dict["form_of_verification"] = class_info[3].text.strip()
        
        for class_type in class_types:
            class_type_name, hours = class_type.split(":")
            class_dict[class_type_name] = hours
            
        additional_info = fetch_additional(class_id)
        
        for key, value in additional_info.items():
            class_dict[key] = value
        
        return class_name, class_dict
    
    except Exception as e:
        print(f"Ups...\n{e}")


def fetch_link(url: str):
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    
    semester_selector = r"syl-grid-tab-content"
    data = soup.find_all("div", {"class": semester_selector})
    
    isi_data = dict()
    
    for semester_nr, semester in enumerate(data[1:]):
        isi_data[f"semester_{semester_nr+1}"] = {}
        
        class_selector = r"tbody > tr"
        classes = semester.select(class_selector)
        
        for studies_class in classes:
            try: 
                class_name, class_dict = parse_class(studies_class)
                isi_data[f"semester_{semester_nr+1}"][class_name] = class_dict
                
            except Exception as e:
                print(f"Ups...\n{e}")
                
    return isi_data


def save_json(data: dict, filename: str):
    json_obj = json.dumps(data, indent=4)
    Path("./data").mkdir(parents=True, exist_ok=True)
    filename = os.path.join("./data", filename)

    with open(filename, "w") as file:
        file.write(json_obj)


if __name__ == "__main__":
    isi_bsc_url = r"https://sylabusy.agh.edu.pl/en/1/2/18/1/4/16/140"
    data = fetch_link(isi_bsc_url)
    save_json(data=data, filename="isi_bcs.json")
    
    isi_ms_url = r"https://sylabusy.agh.edu.pl/en/1/2/18/1/5/16/140"
    data = fetch_link(isi_ms_url)
    save_json(data=data, filename="isi_ms.json")
