import time
import os

folder = 'FM1/'
os.chdir(folder)

while True:

    one_minute_ago = time.time() - 300 
    for somefile in os.listdir('.'):
        st=os.stat(somefile)
        mtime=st.st_mtime
        if mtime < one_minute_ago:
            print('remove %s'%somefile)
            os.unlink(somefile) # uncomment only if you are sure

    time.sleep(10)