
import socket,sys,os,mimetypes,sys,re,subprocess,multiprocessing



class HTTPServer:
    def __init__(self,add,port):
        self.add=add
        self.port=port
   
    def run(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((self.add,self.port))
        sock.listen()
        print("server listening")
        count=0

        while True:
            connection,client_add=sock.accept()
            process=multiprocessing.Process(target=self.get_response,args=(connection, ))
            process.start()
            process.join()
            count+=1
            print(count)
        
            connection.close()
           
    def get_response(self,connection):
        # print("\n\nGET RESPONSE BLOCK\n\n")
        data=connection.recv(1024).decode()
        urlinfo=self.URLfunc(data)
        # print("#########",urlinfo)
        root=os.getcwd()
        # print("@@@@@@@",root)
        dirpath=os.path.join(root,urlinfo)
        # print("********@@@@@@@@",dirpath)
        if os.path.isdir(dirpath):
            response=self.Diplaydircontent(urlinfo,dirpath)
        elif os.path.isfile:
            response=self.DisplayFileContent(dirpath,connection)
        else:
            response=self.NotFoundMessage(connection)
        
       
        connection.sendall(response)


    def URLfunc(self,data):
        # print("\n\n URLFUNC \n\n")
        # print("\n", data)
        from_data=re.findall("GET\s(.*?)\sHTTP",data)[0]
        # print("from_data")
        return from_data[1:]
   
    def Diplaydircontent(self,dir_from_data,dirpath):
        # print("\n\n DISPLAY DIR CONTENT \n\n")
        listoffiles=os.listdir(dirpath)
        message=""
        for file in listoffiles:
            filepath=os.path.join(dir_from_data,file)
            message+=f'<h3 align="centre"><a href={filepath}>{file}</a></br></h1>'
            response_status= "'HTTP/1.1 200 OK\n"
            response_headers=f'Content-Type:text/html\nContent-Length:{len(message)}\nConnection:close\n\n'
            response=(response_status+response_headers+message).encode()
        return response
   
    def DisplayFileContent(self,dirpath,connection):
        # print("\n\n DISPAY FIlE CONTENT \n\n")
        if "bin" in dirpath:
            if 'test' in dirpath:
                f=open(dirpath,'r')
                content=f.read()
                f.close()
                result=subprocess.run([sys.executable,"-c",content],capture_output=True,text=True)
                file_content=result.stdout.encode()
            elif 'ls' in dirpath:
                process = subprocess.Popen("dir",shell=True, stdout=subprocess.PIPE)
                subprocess_return = process.stdout.read()    
                file_content=subprocess_return
            elif 'du' in dirpath:
                content = "<h1 align=\"center\"> windows doesnot support du command</h1>"
                response_status= "'HTTP/1.1 404 not found\n"
                response_headers=f'Content-Type:text/html\nContent-Length:{len(content)}\nConnection:close\n\n'
                response=response_status+response_headers+content
                print("sending data")
                #connection.sendall(response.encode()) 
                return response.encode()       
        else:
            f=open(dirpath,'rb')
            file_content=f.read()
            f.close()
        response_status= 'HTTP/1.1 200 \n'
        response_header=f'Content-Type:{mimetypes.guess_type(dirpath)}\nContent-Length:{len(file_content)}\nConnection:close\n\n'
        print(response_header)
        final_response= (response_status+response_header).encode()+file_content
        #connection.sendall(final_response)
        return final_response
   
    def NotFoundMessage(self,connection):
        # print("\n\n NOT  FOUND \n\n")
        content = "<h1 align=\"center\">Webserver Under construction</h1>"
        response_status= "'HTTP/1.1 200 OK\n"
        response_headers=f'Content-Type:text/html\nContent-Length:{len(content)}\nConnection:close\n\n'
        response=(response_status+response_headers+content).encode()
        print("sending data")
        #connection.sendall(response)
        return response



def main():
    obj=HTTPServer('127.0.0.1',8888)
    obj.run()
pass

if __name__ == "__main__":
    main()
