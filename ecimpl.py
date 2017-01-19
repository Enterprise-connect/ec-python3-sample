import cherrypy, json;
from cherrypy import expose;
import eclib.lib;

class ECAgentImpl:
    @expose
    def ec_version(self):        
        return eclib.lib._getVersion();

    @expose
    def get_ec_settings(self):
        try:
            if(eclib.lib._verifySettings()==True): 
                return json.dumps(eclib.lib._readSettings(),sort_keys=False);
            else:
                return 'Invalid Data File';
        except Exception as err:
            return 'Missing Configuration Parameters. Please check data.json.'

    @expose
    def start_ec_agent(self):
        if(eclib.lib._createFile()==True):
            return 'EC Agent has been successfully started.';
        else:
            return 'EC Agent failed to start.';

    @expose
    def kill_ec_agent(self):
        if(eclib.lib._killEC()==True):
            return 'EC Agent is not running.';
        else:
            return 'EC Agent successfully terminated.';

    @expose
    def check_ec_agent(self):
        flag = eclib.lib._checkStatus();
        if(flag==True):
            return 'Stil Active';
        else:
            return 'Inactive';

cherrypy.config.update({'server.socket_port': 8500, 'tools.gzip.on': True})
cherrypy.quickstart(ECAgentImpl())