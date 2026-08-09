#!/usr/bin/env python3
"""
XLRI AIS Data Scraper
Scrapes complete student directory and detailed profiles from XLRI Academic Information System.
"""

import os
import json
import time
import ssl
import urllib.request
import urllib.parse
import http.cookiejar
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Target Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_CSV = os.path.join(BASE_DIR, 'xlri_students_directory.csv')
DIR_JSON = os.path.join(BASE_DIR, 'xlri_students_directory.json')
PROFILES_JSON = os.path.join(BASE_DIR, 'xlri_all_students_full.json')
PROFILES_CSV = os.path.join(BASE_DIR, 'xlri_all_students_full.csv')
CACHE_FILE = os.path.join(BASE_DIR, 'xlri_scraped_cache.json')

# Credentials
USERNAME = 'B25019'
PASSWORD = 'zPWwRLn8@'

def setup_opener():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('DEFAULT@SECLEVEL=0')

    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPCookieProcessor(cookie_jar)
    )
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    ]
    return opener

def login(opener):
    print("Logging into XLRI AIS...")
    login_url = 'https://acad.xlri.ac.in/ais/login/Pwd_valid.php?app='
    post_data = urllib.parse.urlencode({
        'uid': USERNAME,
        'pwd': PASSWORD,
        'attempt': '2'
    }).encode('utf-8')
    
    res = opener.open(login_url, data=post_data)
    print("Login complete. Final URL:", res.geturl())

def fetch_directory(opener):
    print("Fetching master student directory (Show All)...")
    url = 'https://acad.xlri.ac.in/ais/internet/StuList.php?Stu=&Query=Show+All'
    html = opener.open(url).read().decode('utf-8', errors='ignore')
    
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    
    directory = []
    base_url = 'https://acad.xlri.ac.in/ais/internet/'
    
    for tr in rows:
        cells = tr.find_all(['td', 'th'])
        if len(cells) >= 4:
            sno = cells[0].get_text(strip=True)
            sid = cells[1].get_text(strip=True)
            name_cell = cells[2]
            name = name_cell.get_text(strip=True)
            
            a_tag = name_cell.find('a')
            detail_link = base_url + a_tag.get('href') if (a_tag and a_tag.get('href')) else ''
            program = cells[3].get_text(strip=True)
            
            directory.append({
                'sno': sno,
                'student_id': sid,
                'name': name,
                'program': program,
                'detail_url': detail_link
            })
            
    df = pd.DataFrame(directory)
    df.to_csv(DIR_CSV, index=False)
    df.to_json(DIR_JSON, orient='records', indent=2)
    print(f"Saved directory: {len(directory)} records to {DIR_CSV}")
    return directory

def parse_profile(opener, student_info):
    sid = student_info['student_id']
    url = f'https://acad.xlri.ac.in/ais/internet/StuDetails.php?sid={sid}'
    
    profile = {
        'sno': student_info.get('sno', ''),
        'student_id': sid,
        'name': student_info.get('name', ''),
        'program': student_info.get('program', ''),
        'detail_url': url,
        'email': '',
        'mobile': '',
        'phone': '',
        'dob': '',
        'work_exp_months': '',
        'education': '',
        'hostel_room': '',
        'address': '',
        'sop': '',
        'achievements': '',
        'hobbies': '',
        'photo_url': ''
    }
    
    try:
        resp = opener.open(url, timeout=12).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Name inside modal header if name was missing or incomplete
        modal_title = soup.find('h4', class_='modal-title')
        if modal_title and modal_title.get_text(strip=True):
            profile['name'] = modal_title.get_text(strip=True)
            
        field_map = {
            'Email': 'email',
            'Mobile': 'mobile',
            'Phone/ Mobile': 'phone',
            'DOB': 'dob',
            'Work Exp(in Months)': 'work_exp_months',
            'Educational Qualifications': 'education',
            'Room No. & Hostel Name': 'hostel_room',
            'Permanent Address': 'address',
            'Statement of Purpose': 'sop',
            'Achievements': 'achievements',
            'Hobbies': 'hobbies'
        }
        
        for group in soup.find_all('div', class_='form-group'):
            lbl = group.find('label')
            if lbl:
                lbl_txt = lbl.get_text(strip=True)
                full_txt = group.get_text(separator=' ', strip=True)
                val = full_txt.replace(lbl_txt, '', 1).strip()
                
                if lbl_txt in field_map:
                    profile[field_map[lbl_txt]] = val
                elif lbl_txt and lbl_txt not in ['Statement of Purpose', 'Achievements', 'Hobbies']:
                    profile[lbl_txt] = val
                    
        photo_div = soup.find('div', id='stuPhoto')
        if photo_div and photo_div.find('img'):
            src = photo_div.find('img').get('src')
            if src:
                profile['photo_url'] = 'https://acad.xlri.ac.in' + src if src.startswith('/') else src
                
        return profile
    except Exception as e:
        profile['error'] = str(e)
        return profile

def main():
    opener = setup_opener()
    login(opener)
    
    if os.path.exists(DIR_CSV):
        print(f"Loading existing directory from {DIR_CSV}...")
        df_dir = pd.read_csv(DIR_CSV)
        directory = df_dir.to_dict('records')
    else:
        directory = fetch_directory(opener)
        
    print(f"Total students to scrape: {len(directory)}")
    
    # Load cache if available
    scraped_cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                scraped_cache = json.load(f)
            print(f"Loaded {len(scraped_cache)} cached profile records.")
        except Exception as e:
            print("Could not load cache:", e)
            
    to_scrape = [item for item in directory if item['student_id'] not in scraped_cache]
    print(f"Remaining profiles to scrape: {len(to_scrape)}")
    
    completed_count = len(scraped_cache)
    start_time = time.time()
    
    max_workers = 25
    batch_size = 200
    
    for i in range(0, len(to_scrape), batch_size):
        batch = to_scrape[i:i + batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(to_scrape)-1)//batch_size + 1} ({len(batch)} items)...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(parse_profile, opener, item): item['student_id'] for item in batch}
            for future in as_completed(futures):
                sid = futures[future]
                res = future.result()
                scraped_cache[sid] = res
                completed_count += 1
                
        # Periodic save
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(scraped_cache, f, ensure_ascii=False, indent=2)
            
        elapsed = time.time() - start_time
        rate = (completed_count - len(scraped_cache) + len(batch)) / elapsed if elapsed > 0 else 0
        print(f"Progress: {completed_count}/{len(directory)} profiles scraped ({completed_count*100/len(directory):.1f}%). Cache saved.")

    # Final export
    final_list = list(scraped_cache.values())
    df_final = pd.DataFrame(final_list)
    
    df_final.to_csv(PROFILES_CSV, index=False)
    df_final.to_json(PROFILES_JSON, orient='records', indent=2)
    
    print("\n" + "="*60)
    print(f"SUCCESS! Scraped {len(final_list)} full student profiles.")
    print(f"CSV saved to: {PROFILES_CSV}")
    print(f"JSON saved to: {PROFILES_JSON}")
    print("="*60)

if __name__ == '__main__':
    main()
