import requests

url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
headers = {
            'Host': 'www.52pojie.cn',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '_uab_collina=154461446152307655890437; htVD_2132_saltkey=ALi0U0cu; htVD_2132_lastvisit=1547880514; htVD_2132_client_created=1547905673; htVD_2132_client_token=D8A0A6B376D7932896C9D94AE7EEAF72; htVD_2132_auth=d3c1NblfSA%2FQbT1G7hbA35YcYgr7v8VlPaieHmQVa%2Bmi2R%2FbCdi6ePLc8jXpsHQwuXyJA7s2v3%2FShZJLl2%2FQ3n7ocwg; htVD_2132_connect_login=1; htVD_2132_connect_is_bind=1; htVD_2132_connect_uin=D8A0A6B376D7932896C9D94AE7EEAF72; htVD_2132_nofavfid=1; htVD_2132_smile=1D1; htVD_2132_visitedfid=16D8D37; htVD_2132_pc_size_c=0; htVD_2132_ulastactivity=1548031223%7C0; htVD_2132_lastact=1548031224%09home.php%09spacecp; htVD_2132_checkpm=1; htVD_2132_lastcheckfeed=358052%7C1548031224; Hm_lvt_46d556462595ed05e05f009cdafff31a=1547806148,1547878988,1547905666,1548031228; Hm_lpvt_46d556462595ed05e05f009cdafff31a=1548031228',
}


response = requests.get(url=url, headers=headers)
print(response.text)
print(response.status_code)
