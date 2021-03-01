
wget "https://depositonce.tu-berlin.de/bitstream/11303/9429/3/HRIRs.zip"
wget "https://depositonce.tu-berlin.de/bitstream/11303/9429/4/Antrhopometric%20measures.zip"
wget "https://depositonce.tu-berlin.de/bitstream/11303/9429/5/HpIRs.zip"
wget "https://depositonce.tu-berlin.de/bitstream/11303/9429/6/3D%20head%20meshes.zip"
mkdir HUTUBS
unzip HRIRs.zip
unzip HpIRs.zip
unzip "Antrhopometric measures.zip"
unzip "3D head meshes.zip"
mv HRIRs HUTUBS
mv HpIRs HUTUBS
mv "Antrhopometric measures" HUTUBS
mv "3D head meshes" HUTUBS
rm *.zip
