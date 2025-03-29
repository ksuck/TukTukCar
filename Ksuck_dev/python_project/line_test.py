import requests

def linenotify(message):
  url = 'https://notify-api.line.me/api/notify'
  token = 'il0qsfUabxa9EpkE3u9OBo28wGofV1adhF256BWBQAf' # Line Notify Token เอามาจาก line api
  img = {'imageFile': open('image.png','rb')} #Local picture File
  data = {'message': message}
  headers = {'Authorization':'Bearer ' + token}
  session = requests.Session()
  session_post = session.post(url, headers=headers, files=img, data =data) #<--- files รูป ต้องใส่ data ให้มีพื้นที่หรือเว้นช่องถึงจะส่งไป
  print(session_post.text) 
  
message = 'Hello Python' #Set your message here!
linenotify(message)