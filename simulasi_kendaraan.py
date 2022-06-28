from cProfile import label
import random as rand
from turtle import *
import matplotlib.pyplot as plt
import numpy as np

M = 100     # Panjang Lintasan
p = 0.3     # Probabilitas Berhenti
V0 = 0      # Kecepatan Awal
d = 2       # Jarak Aman Mobil
N = 20      # Jumlah Mobil
tmax = 1000 # Waktu Maksimal
Vmax = 5    # Kecepatan Maksimal
v = 0       # Menyimpan nilai v

# TAMBAHAN
n = 0       # Menghitung perputaran mobil  
ncar = 0    # Untuk menyimpan jumlah mobil
arrx = []   # Untuk menyimpan kepadatan mobil pada x80 - x90
arrt = []   # Untuk menyimpan interval waktu
t_avg = []  # Menyimpan waktu rata-rata
skala = 10  # Untuk skala perjalanan mobil
spd = 100    # Kecepatan pergerakan animasi

# Fungsi mencari nilai maksimum
def nilaimax(data):
    temp = 0
    for i in range(0, len(data)):
        if data[i-1] < data[i] :
            temp = i
    return [temp, data[temp]]

# Mengubah posissi awal mobil
def posisi(nama, x,y):
    nama.penup()
    nama.goto(x-M*5,y)
    nama.pendown()

#  Membuat lintasan Animasi bergerak
garis = Turtle()
garis.pensize(5)
garis.speed(spd)
posisi(garis, -10, 20)
garis.forward(M*skala+10)
posisi(garis, -10, -20)
garis.forward(M*skala+10)
posisi(garis, 1000,1000)
rand.seed()

# Mendefinisikan warna yang akan digunakan 
Colors = ['#6CC4A1', '#F15412', '#4B5D67', '#590696', '#C70A80', '#FBCB0A', 
          '#F47C7C', '#BABD42', '#112B3C', '#FF7700', '#53BF9D', '#F94C66', '#BD4291', 
          '#FFC54D', '#1B2430', '#51557E', '#816797', '#D6D5A8', '#DF7861', '#1363DF']

# Membuat animasi mobil
def defMobil():
    # Array berisi 20 kendaraan dengan keterangan X random dan V0 = 0
    rand.seed()
    arrMobil = [[rand.randint(0,M), V0, 0] for i in range(N)]
    arrMobil.sort()

    # Animasi posisi mobil
    anim = [i for i in range(N)]
    for i in range(N):
        anim[i] = Turtle()
        anim[i].shapesize(1.2)
        anim[i].speed(spd)
        anim[i].color(Colors[i])
        posisi(anim[i], arrMobil[i][0]*skala, 0)
    return arrMobil, anim

def posisiAwal(mobil):
    pAwal = []
    for i in mobil:
        pAwal.append(i[0])
    return pAwal

# ALGORITMA
cars, mobil = defMobil()
xAwal = posisiAwal(cars)
for i in range(0,tmax,1):
    ncar = 0
    arr = [0 for i in range(int(M/5))]
    
    for j in range(N):
        next = (j+1 if j+1 < N else 0)

        xn = cars[next][0] # Posisi mobil di depannya
        Vn = cars[next][1] # Kecepatan mobil di depannya

        x = cars[j][0]  # Posisi mobil
        Vt = cars[j][1]  # Kecepatan mobil saat itu 
        n = cars[j][2] # Putaran setiap mobil

        dist = (xn - x if xn > x else (M-x)+xn) # Jarak dengan mobil didepan
        v = min([Vt+1, Vmax, dist-1])
        
        if dist <= d and Vn < d-1:
            Vt = v
            Vn = d-1
        elif rand.randint(0,10) < 3 :
            Vt = max([v-1, 0])
        else : 
            Vt = v

        # Update jarak
        x += Vt 
        if x >= xAwal[j] and x <= xAwal[j]+(Vmax-1) and i > Vmax and n == 1:
            t_avg.append(i)
        if x >= M :
            x -= (M)
            n += 1
 
        arr[int(x/5)] += 1
        ncar = (ncar+1 if x >= 80 and x<= 90 else ncar)

        cars[j] = [x, Vt, n] # Update informasi kendaraan
        cars[next][1] = Vn # Update jarak kendaraan di depan

        # Akan memberikan animasi selama 10 detik pertama
        if i < 10:
            posisi(mobil[j], x*skala, 0)
            posisi(mobil[next], cars[next][0]*skala, 0)

    arrt.append(nilaimax(arr))
    arrx.append(ncar)

# Animasi posisi akhir mobil
for i in range(N):
    posisi(mobil[i], cars[i][0]*skala, 0)

# Membuat pembatas jalan
roads = np.array( [ [[-0.5,M+0.5], [0.8,0.8]], [[-0.5,M+0.5], [1.2,1.2]] ] )
plt.figure(figsize=(10,3))
for road in roads:
    plt.plot(road[0], road[1], c="red")

# Menggambarkan posisi akhir mobil
car = []
for i in cars:
    car.append(i[0])
y = [1 for i in range(N)]
plt.scatter(car, y, c=Colors[:N], marker='.', s=100, edgecolors='black')
plt.show()

# Menampilkan grafik kepadatan mobil persatuan waktu di x80 - x90
plt.figure(figsize=(15,5))
plt.plot(arrx)
plt.show()

# Menampilkan kepadatan setiap 5 satuan posisi
count = []
posisi = []
for i in arrt :
    count.append(i[1])
    posisi.append(i[0])

plt.figure(figsize=(15,10))
plt.plot(posisi, c='blue', label='Satuan posisi')
plt.plot(count, c='orange', label='Kepadatan')
plt.show()

# Informasi Mobil
print("Waktu rata-rata: ", (sum(t_avg)/len(t_avg)))

