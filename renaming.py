import os

pliki = os.listdir(".")
print(pliki)


jpgi = []

for x in pliki:
    if x.endswith(".jpg"):
        jpgi.append(x)
        
print(jpgi)

for i, z in enumerate(jpgi):
    os.rename(z, str(i)+'.jpg')