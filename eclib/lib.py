#Import Libraries
import os, platform, json, logging,subprocess, time, signal;
from shutil import copyfile;

#Set Logger Format
FORMAT = '%(asctime)-0s : %(funcName)s() %(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO);
#Initialize Global Variable For ECAgent Process
proc = None;    
#Initialize Logger
logger = logging;
#Main Execution Command
_main_exec_command='$command -oa2 "$oa2" -hst "$hst" -csc "$csc" -cid "$cid" -aid "$aid" -tid "$tid" -mod "$mod" -pxy "$pxy" -lpt "$lpt" -hca 3999 -dbg -dur 300';
data = None;
_ver = 'v1.96_fukuoka';

def _getVersion():
        return _ver;
#Read User Properties
def _readSettings():
        global data;
        if(data==None):
                logger.info('%s'%('Attempting to read settings file.'));
                try:
                        with open('./data.json','r') as data_file:
                                data = json.load(data_file);
                        logger.info('%s'%('Copy to Json Object Complete.'));
                        _settings_json = json.dumps(data);
                        return data;
                except Exception as err:
                        data = None;
                        logger.error(err);
                        return null;
        else:
                return data;

def _checkNullString(stringValue):
        stringValue=str(stringValue).strip();
        if(stringValue==''):
                return False;
        else:
                return True;

#Verify settings
def _verifySettings():
        json_settings = _readSettings();
        flag = True;
        try:
                verificationParams = ('mode','agentid','lpt','tunnelid','proxy','gateway','hsc','uaa.url','cid','csc');
                for param in verificationParams:
                        if(param=='proxy'):
                                logger.info('%s parameter will be skipped.'%(param));
                                continue;
                        else:
                                if(_checkNullString(json_settings[param])==True):
                                        logger.info('%s parameter is valid.'%(param));
                                else:
                                        flag = False;
                                        logger.info('%s parameter is invalid.'%(param));
                                        break;
                #If flag is true, then we have all parameters and none of them are blank. 
                return flag;
        except ValueError as err:
                logger.error(err);
                return False;


#Get Execution Command
def _getExecCommand():
        return _settings_json

#Get User Environment
def _getenv():
        return os.name;

#Get User Platform
def _getPlatform():
        return platform.platform();

#Function for running the script file.
def _runBatFile():
        try:
                global proc;
                proc = subprocess.Popen('script.bat', shell=True, bufsize=1);
                #Give 5 seconds for the process to start up. 
                time.sleep(5);                
                #Retrieve PID.
                pid = proc.pid;
                return True;
        except Exception as err:
                logger.error(err);
                return False;

#Function for checking the status of ECAgent
def _checkStatus():
        if(proc!=None):
                if(proc.poll()==None):
                        flag = False;
                else:
                        flag = True;
        else:
                flag = False;
        return flag;

#Function for Killing ECAgent
def _killEC():
        #Use global version of proc
        global proc;
        if(proc!=None):
                #Check OS and accordingly kill. 
                if(platform.system() == "Windows"):
                        #Killing Windows Process For The ECAgent
                        subprocess.Popen("taskkill /F /T /PID %i" % (proc.pid) , shell=True);
                else :
                        #If any other OS then use os.kill
                        os.kill( proc.pid, signal.SIGKILL);
        #Return the status of ECAgent        
        return _checkStatus();

#Convert To String and Trim Spaces
def _convertTrim(data):
        data = str(data).strip();
        return data; 

#Function for creating script file. 
def _createFile():
        json_settings = _readSettings();
        '$command -oa2 "$oa2" -hst "$hst" -csc "$csc" -cid "$cid" -aid "$aid" -tid "$tid" -mod "$mod" -pxy "$pxy" -lpt "$lpt" -hca 3999 -dbg -dur 300';
        _run_command = _main_exec_command.replace('$command', _convertTrim('ecagent_windows_var.exe')).replace('$hst',_convertTrim(json_settings['gateway'])).replace('$oa2',_convertTrim(json_settings['uaa.url'])).replace('$csc',_convertTrim(json_settings['csc'])).replace('$cid',_convertTrim(json_settings['cid'])).replace('$aid',_convertTrim(json_settings['agentid'])).replace('$tid',_convertTrim(json_settings['tunnelid'])).replace('$mod',_convertTrim(json_settings['mode'])).replace('$pxy',_convertTrim(json_settings['proxy'])).replace('$lpt',_convertTrim(json_settings['lpt']));      
        try:
                copyfile('./eclib/ecagent_windows_var.exe','./ecagent_windows_var.exe')
                with open('script.bat', 'w+') as batFile:
                        #batFile.write('start cmd.exe /k');
                        batFile.write(_run_command);
                return _runBatFile();
        except Exception as err:
                print(err);
                return -1;

#Environment Check 
def _createCommand(env):
        if(platform.system().lower()== "Windows"):
                logger.info('%s'%('Found Windows Environment.'));
                print('%s'%_readSettings());        
