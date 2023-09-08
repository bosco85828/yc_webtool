from dotenv import load_dotenv
import os 
import requests
import re
import cdnw_client2
import json
from pprint import pprint
from datetime import datetime,timezone,timedelta
load_dotenv()
CDNW_ACCESSKEY=os.getenv('CDNW_ACCESSKEY')
CDNW_SECRETKEY=os.getenv('CDNW_SECRETKEY')
now=datetime.now().strftime("%Y-%m-%d")

global AccessKey, SecretKey
AccessKey = CDNW_ACCESSKEY
SecretKey = CDNW_SECRETKEY

goup_id = "168244"
def get_list():
    host='api.cdnetworks.com'
    http_method = 'GET'
    uri='/user/control-groups'
    post_request_body={}
    
    data=cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()
    return data

def set_domain(domains):
    host='api.cdnetworks.com'
    http_method = 'PUT'
    uri="/user/control-groups/ad7062dc-7438-4fb6-a5bd-bca4e1441bee"
    post_request_body={
        'domainList':domains
    }
    data=cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()
    return data

def get_domain_list():
    host='api.cdnetworks.com'
    http_method = 'GET'
    uri="/api/domain"
    post_request_body={}
    data=cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()
    return data
# print(get_list()['data'][0])
# print(set_domain())
row_domains=set(["kajidi.com",".kajidi.com","xinglinkejicc.com",".xinglinkejicc.com","msqhedu.com",".msqhedu.com","njydlzs.com",".njydlzs.com","sdjishuo.com",".sdjishuo.com","lingjingtz.com",".lingjingtz.com","604485.com",".604485.com","hnheiku.com",".hnheiku.com","0797gzyc.com",".0797gzyc.com","ampure-edi.com",".ampure-edi.com","gn-uep.com",".gn-uep.com","qz-pos.com",".qz-pos.com","cdxyyj.com",".cdxyyj.com","cdsdfj.com",".cdsdfj.com","kmhxsm.com",".kmhxsm.com","ngwsdq.com",".ngwsdq.com","shtonglu.com",".shtonglu.com","pz-yz.com",".pz-yz.com","huayuanintel.com",".huayuanintel.com","lsbgjj.com",".lsbgjj.com","bjskswkj.com",".bjskswkj.com","ybpgl.com",".ybpgl.com","196196.vip","fifa.196196.vip","196196.cc","fifa.196196.cc","196tiyu.net","www.196tiyu.net","196ty.net","www.196ty.net",".wajuejin.com",".qigame.cn",".zw3e.com","tcyhj.com",".tcyhj.com","mccenfi.com",".mccenfi.com","qdtaigu.com","www.qdtaigu.com",".u1e.cn","baike5.cn","www.baike5.cn","m.baike5.cn","chongzs.com","m.chongzs.com","www.chongzs.com","cnnedn.com","www.cnnedn.com","www.sanalmatbaa.com","sanalmatbaa.com","u1e.cn","www.u1e.cn","task.u1e.cn","www.zgcslp.com","zgcslp.com","dechangchun.com","www.dechangchun.com","weifangaoke.com","www.weifangaoke.com","","anjiazhejiang.com","jinmengled.cn","dmjds.cn","nciae.online","duila98.com","lumikko.com.cn","yl-world.com.cn","yl-coffee.net.cn","haokafei.net.cn","haokafei.net","spych.cn","dfzhuangshicl.com","babahaoche.com.cn","shumingkeji.cn","gzbamy.cn","guote.net","nzpckk.cn","nkvoqc.cn","gdkwkm.cn","biannve.com","miaonun.com","dingrunjy.cn","xingshuangs.cn","hardwarec.cn","wzwstudy.top","newsker.cn","xnzqara.cn","szgtg.cn","youke365.cn","liangshanguachechang.com","kalamailijinshicai.com","lyq2034.cn","hexiejiangsu.com","hingwah-auto.com","xirda.cn","gedaa.cn","lmcs.shop","whhrmy.cn","joy-zone.cn","ty930.top","zhanniuwang.com.cn","0532cy.cn","xtdswd.cn","mo-lan.cn","kmsqks.cn","liu11-lab.cn","aiwuweizhong.com","shouyhui.com","zzgmkj.cn","factofmoney.com","ledcs.com.cn","qinggan28.cn","nbliushi.cn","jfzqlcc.com","worldmusic.cn","xuexinjiaoyou.com","chinadayankj.com","kmnrqgp.cn","luomengde.cn","xyymq.cn","meimingsc.com","minkang07.cn","ggccxgzs.cn","jyskl.com","minkang08.cn","uketech.net","guanshiqiang.com","um200.com","xun46.cn","szfengshi.cn","forwardv.cn","tianliang185.cn","gongxiangsousuo.com.cn","gu816.cn","huaihuaxw.top","huchongba.com","dbiom.cn","liyaoyue.cn","tpconnex.com","lyliangyu.com","livejasminwebcams.com","kennedyjenson.com","covenantlandscaping.com","vaalnetwork.com","sweet-natural-girls.com","michellejaffearts.com","ylrxy.cn","baicaija.com","gamer-shamsdo.online","crete-travel-guide.com","tkgc.shop","atmajewels.com","naraycard.com","kmomocha.com","cinoong.com","88mtv.net","5dn4982g.cn","65lnh12.cn","laolailezj.cn","cqor.com","hnhyz.com","chaichufw.com","gelaierrhy.com","dhcc2022.cn","huangyeso.com","mabiseo.com","huikai123.com","lzldlvshi.com","ematch-tech.com","good4451.com","zskeshun.com","cgilent17.com","plussine.com","evartem.com","lychite.cn"])
cdnw_domains=set([ x['domain-name'] for x in get_domain_list() ])
# print(len(row_domains))
# print(len(cdnw_domains))
# print(list(row_domains & cdnw_domains))
add_domains=["www.policyjurygroup.org","policyjurygroup.org","www.atsac.org","atsac.org","39j3.com","2zv6.com","4vqu.com","yef8.com","7c4p.com","5liz.com","capefearedc.org","millionhomes.org","ccpachina.org","henanstbc.org","xiangrong.org","thriftology.org","neohiorealestate.org","taopianyi.com","wac-project.com","jscxst.com","devol-cn.com","bjhongdake.com","web759.com","baitazhen.com","ncwfjj.com","crcgash.com","3iq4.com","www.39j3.com","www.2zv6.com","www.4vqu.com","www.yef8.com","www.7c4p.com","www.5liz.com","www.capefearedc.org","www.millionhomes.org","www.ccpachina.org","www.henanstbc.org","www.xiangrong.org","www.thriftology.org","www.neohiorealestate.org","www.taopianyi.com","www.wac-project.com","www.jscxst.com","www.devol-cn.com","www.bjhongdake.com","www.web759.com","www.baitazhen.com","www.ncwfjj.com","www.crcgash.com","www.3iq4.com"]


print(set_domain(list(row_domains & cdnw_domains)+add_domains))