import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import wavio
import matplotlib.pyplot as plt 
import math 
import cmath


def fourier_transform (data):
    real=[]
    img=[]
    n=0
    l=len(data)

    for n in range(int(-l/2),int(l/2)):
        img_data=0
        real_data=0

        for w in range(l):
            theta=2*math.pi*n*w/l
            img_data=img_data-math.sin(theta)*data[w]
            real_data=real_data+math.cos(theta)*data[w]

        img=img+[img_data]
        real=real+[real_data]

    return (real,img) 

def inverse_fourier(imaginary, real ):
    n=0
    img1=[]
    real1=[]
    l=len(real)

    for n in range(l):
        real_data=0
        img_data=0

        for w in range(l):
            theta=2*math.pi*w*n/l
            real_data+=(real[w]*math.cos(theta)-imaginary[w]*math.sin(theta))
            img_data+=(imaginary[w]*math.cos(theta)+real[w]*math.sin(theta))

        real1=real1+[real_data]
        img1=img1+[img_data]

    for i in range(len(real1)):
        real1[i]=real1[i]/((2*math.pi)*l);
    return real1


from scipy.io.wavfile import write

fs = 6000    # Sample rate
seconds = 1 # Duration of recording

# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
# sd.wait()  # Wait until recording is finished
# plt.plot(myrecording)
# plt.show()
# write('6000.wav', fs, myrecording)  # Save as WAV file 


rate, aa = scipy.io.wavfile.read('6000.wav')
time=[]
for i in range(6000):
    time.append(i)
ff=61
data=[]
for i in range(len(aa)):
    data.append(aa[i][1])

# print(data[5300],data[5400],data[5900])

plt.figure();
plt.subplot(5,1,1)
plt.plot(time, data) 
plt.xlabel('x - axis') 
plt.ylabel('y - axis') 
plt.title('Sampled voice') 
# plt.show() 


mag,imaginary=fourier_transform(data)
magnitude=[]
for i in range(len(mag)):
    magnitude.append(mag[i])

absol=[]
for i in range(len(magnitude)):
    absol.append(abs(magnitude[i]))



w=[]
for i in range(len(time)):
    w.append(2*math.pi*(time[i]-3000))

plt.subplot(5,1,2)
plt.plot(w, absol) 
plt.xlabel('x - axis') 
plt.ylabel('y - axis') 
plt.title('FT voice') 


peak=0
for i in range(len(absol)):
    if(absol[i]>peak):
        peak=absol[i]
threshold=peak/4
for j in range(len(absol)):
    if(absol[j]>threshold):
        break
bw=math.ceil(abs(w[j]))+ff
# print(abs(w[j]))

bw_nice=math.floor((bw*0.8)/(2*math.pi))
print("Bandwidth is- ",bw_nice)




daddy=inverse_fourier(imaginary,magnitude)

for i in range(len(daddy)):
    daddy[i]*=6.28318

plt.subplot(5,1,3)
plt.plot(time, daddy) 
plt.xlabel('x - axis') 
plt.ylabel('y - axis') 
plt.title('IDTFT voice') 






zero=[]
for i in range(6000):
    zero.append(0)

magnitude_80 =[]
imaginary_80 =[]

for i in range(6000):
    if (i>(3000-bw_nice) and i<(3000+bw_nice)): #the explanation for this is in the reprt, if the voice signal changes, the bandwidth changes and we cant predict it or put a threshold on the value so it is hard coded, I can explicitly explain you why this was done though.
        magnitude_80.append(magnitude[i])
        imaginary_80.append(imaginary[i])
    else:
        magnitude_80.append(0)
        imaginary_80.append(0)
 
real_80=inverse_fourier(imaginary_80,magnitude_80)
real_0=inverse_fourier(zero,magnitude)

# for i in range(len(real_0)):
#     real_0[i]*=6.28318

plt.subplot(5,1,4)
plt.plot(time,real_80) 
plt.xlabel('x-axis') 
plt.ylabel('y-axis') 
plt.title('IDTFT 80% Bw voice') 

plt.subplot(5,1,5)
plt.plot(time,real_0) 
plt.xlabel('x-axis') 
plt.ylabel('y-axis') 
plt.title('IDTFT 0 phase') 
plt.show()


INV1=np.asarray(daddy,dtype='f')
wavio.write("OUTPUT1.wav", INV1, 6000, sampwidth=2)

INV2=np.asarray(real_80,dtype='f')
wavio.write("OUTPUT2.wav", INV2, 6000, sampwidth=2)

INV3=np.asarray(real_0,dtype='f')
wavio.write("OUTPUT3.wav", INV3, 6000, sampwidth=2)

