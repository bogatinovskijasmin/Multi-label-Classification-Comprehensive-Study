import os
import time

score = "trainTime"
os.system("java -jar StatTests.jar Friedman " + score + ".csv 1 0 >> " + score + ".stat")
time.sleep(2)
os.system("python3.5 ranks2pdf.py results="+score+".05.ranks out="+score+".pdf")
