from ncclient import manager
import xml.dom.minidom
import socket

node = "127.0.0.1"

def connect(node):
    try:
        device_connection = manager.connect(host = node, port = '2222', username = 'admin', password = 'Cisco!123', hostkey_verify = False, device_params={'name':'nexus'})
        return device_connection
    except:
        print("Unable to connect " + node)

def getVersion(node):
    device_connection = connect(node)
    version = """
               <show xmlns="http://www.cisco.com/nxos:1.0">
                   <version>
                   </version>
               </show>
               """
    netconf_output = device_connection.get(('subtree', version))
    xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
    version = xml_doc.getElementsByTagName("mod:nxos_ver_str") 
    return "Version: "+str(version[0].firstChild.nodeValue)
    
def getHostname(node):
    device_connection = connect(node)
    hostname = """
               <show xmlns="http://www.cisco.com/nxos:1.0">
                   <hostname>
                   </hostname>
               </show>
               """
    netconf_output = device_connection.get(('subtree', hostname))
    xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
    hostname = xml_doc.getElementsByTagName("mod:hostname")
    return "Hostname: "+str(hostname[0].firstChild.nodeValue)
    
def setHostname(node,name):
    device_connection = connect(node)
    update_hostname_config_string = """
	<configure xmlns="http://www.cisco.com/nxos:1.0">
        	<__XML__MODE__exec_configure>
            		<hostname><name>%s</name></hostname>
        	</__XML__MODE__exec_configure>
    	</configure>
               """
    configuration = '<config>' + update_hostname_config_string % (name) + '</config>'
    device_connection.edit_config(target='running', config=configuration)
    return "Hostname changed to " + str(name)

def Main():
    host = "127.0.0.1"
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(5)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        message = conn.recv(1024).decode()
        if message == "show version":
            try:
                message = getVersion(node)
            except:
                message = 'Unable to get this node version'
        elif message.startswith('hostname'):
            try:
                list = message.split(' ')
                message = setHostname(node,list[1])
            except:
                message = 'Unable to change this node hostname'
        elif message == "show hostname":
            try:
                message = getHostname(node)
            except:
                message = 'Unable to get this node hostname'
        else:
                message = "I do not understand"
        conn.send(message.encode())
    conn.close()

if __name__ == '__main__':
        Main()