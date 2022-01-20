# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

try:
    import pip 
except:
    print "########################################################"
    print "##        PLEASE INSTALL PIP PACKAGE FOR PYTHON       ##"
    print "########################################################"
import os

try:
    from zk import ZK
    import eventlet
    from datetime import datetime
    from eventlet import wsgi, listen, kill
    import json
    import tempfile
    from cgi import parse_qs
    #import wx
except:
    pip.main(['install', 'pyzk ', 'install' ,'eventlet', 'install' , 'wxPython==4.1.0'])
    from zk import ZK
    import eventlet
    from datetime import datetime
    from eventlet import wsgi, listen, kill
    import json
    import tempfile
    from cgi import parse_qs
    #import wx
#import tray
#tray.main()
TRAY_TOOLTIP = 'Name'
TRAY_ICON = 'icon.png'
tempdir = tempfile.gettempdir()

DEVNULL = FNULL = open(os.devnull, 'w')
PIPE = open(tempdir + '/main.pid','w+')  
clear = lambda :''#lambda:os.system('cls')
conn = None
class pointeuse(object):
    
    def __init__(self):
        global conn
        #os.system('cls')
        print "##########                 %s               ###########\n\n\n" % 'ODOO ZKTECO SYNC'
        ip = raw_input("Saisir l'adresse ip de la pointeuse [192.168.1.201] : ") or '192.168.1.201'
        #ip = int(raw_input("Saisir le No de Port de la pointeuse [4370] : ") or '4370')
        print ip
        self.zk = ZK(ip,port=4370,verbose=True,password=1)
        try:
            conn = self.zk.connect()
            #os.system('cls')
            print u"Connexion Réussie\n Vous pouvez commencer la synchronisation sur Odoo"
            #conn.test_voice(10)
        except Exception as e:
            print e
            self.__init__()
            
    
    def Connect(self):
        global conn
        conn = res = self.zk.connect()
        return res

    def import_logeee(self,date_start,date_end=str(datetime.now())):
        #TODO: A refaire avec la lib zk.ZK
        self.Connect()
        start = datetime.strptime(date_start, "%Y-%m-%dT%H:%M")
        end   = datetime.strptime(date_end, "%Y-%m-%dT%H:%M")
       # try:
        #temp=self.zk.ReadAllGLogData(1) # <=> zk.ZK.get_attandance()
        c=[]
        while 1:    
            print "while"
            done=self.zk.SSR_GetGeneralLogData(1)   
            if done and isinstance(done,tuple) and not done[0]:
                break
            if not done[3]:
                x="sign_in"
            else:
                x="sign_out"      
            tup=done[4],"-",done[5],"-",done[6]       
            date=''.join(str(i) for i in tup)       
            tup1=done[7],":",done[8],":",done[9]       
            time1=''.join(str(i) for i in tup1)    
            dt = date + " " + time1
            a = []
            a.append(done[1])
            a.append(x)
            a.append(dt)
            
            if datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") >= start and datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") <= end:
                c.append(a) 
            
        return c  # [[matricule:str, type:str, datetime], []]
    
    def import_log(self,date_start,date_end=str(datetime.now())):
        global conn
        start = datetime.strptime(date_start, "%Y-%m-%dT%H:%M")
        end   = datetime.strptime(date_end, "%Y-%m-%dT%H:%M")
        
        #pt = pointeuse()
        zk = conn
        att = zk.get_attendance()
        #print att
        res =[]
        #print dir(att[0])
        for v in att:
            a = [ v.user_id ,'',v.timestamp.strftime('%Y-%m-%d %H:%M:%S')]  
            pass
            res.append(a)
            print 'Matricule : ', ' - '.join(a)
        
        return res or []


    def set_employee(self,emp):
        
        global conn
        
        
        #emp =  parse_qs(emp)
        try:
            p = conn
            p.disable_device()
            users = p.get_users()
            uid_list = dict([(x.user_id,x.uid) for x in users])
            p.set_user(uid_list.get(emp['matricule'],None), user_id = emp['matricule'],name=emp['name'])
            p.enable_device()
            print 'succes\t:', emp.get('name')
        except Exception as e:
            print 'Error\t:', emp.get('name') ,e
            p.test_voice(10)
            #print "Except" ,e

        return True

class Ozk(object): # servive HTTP /socket
    def __init__(self, *args, **kwargs):
        super(Ozk, self).__init__(*args, **kwargs)
        self.zk = pointeuse()

    def bridge(self, env, start_response):
        global conn
        start_response('200 OK', [("Access-Control-Allow-Origin", "*"), ('Content-Type', "application/json")])
       
        if env.get('PATH_INFO') == '/test':
            #res = self.zk.import_log_test()
            #res = json.dumps(res)
            #start_response('200 OK', [("Access-Control-Allow-Origin", "*"), ('Content-Type', "application/json")])
            return 'ok'
            #TODO: pour test seulement

        if env.get('PATH_INFO') == '/sync_att':
            
            clear()
            global conn
            if not conn:
                print "Connexion encours"
                conn.connect()
            clear()
            print u"Connecté"
            conn.test_voice(10)


            
            
            res = {}
            try:
                p = parse_qs(env['wsgi.input'].read())
                res = self.zk.import_log(p['date_start'][0], p['date_end'][0])
            
            except Exception as e:
                print u"Exception d'importation des pointages" , e
            
            finally:
                return json.dumps(res)           

        if env.get('PATH_INFO') == '/sync_employees' :
            clear()
             
            global conn
            if not conn:
                print "Connexion encours"
                conn.connect()
            clear()
            print u"Connecté"
            conn.test_voice(10)
            emps = json.loads(env['wsgi.input'].read())
            print u"##################  Syncronisation des utilisateurs  ###################"
            print emps
            return 'ok'
            for emp in  emps:
                #print emp
                self.zk.set_employee(emp)
            print u"##################  Syncronisation des utilisateurs terminée  ###################"
            
            conn.test_voice(0)

            return 'OK'

        #start_response('200 OK', [("Access-Control-Allow-Origin", "*"),('Content-Type', 'text/plain')])
        return ['\n'.join(['%s-->%s' % (e.ljust(20, ' '), v) for e, v in env.iteritems()])]

    def run(self):
        self.worker_pool = eventlet.GreenPool(20)
        self.sock = listen(('', 8100))
        try:
            pass          
        except Exception as e:
            print e
        finally:
            wsgi.server(self.sock, self.bridge,
                        custom_pool=self.worker_pool, log_output=False)
            wsgi.server(list)

    def stop(self):
        # TODO :  à tester et developper
        print "sss"
        self.worker_pool.resize(0)
        print "gggg"
        self.sock.close()
        print ("Shutting down. Requests left: %s", self.worker_pool.running())
        # self.worker_pool.waitall()
        print ("Exiting.")
        print ("Exiting.")
        return True

app = Ozk()
app.run()
    

