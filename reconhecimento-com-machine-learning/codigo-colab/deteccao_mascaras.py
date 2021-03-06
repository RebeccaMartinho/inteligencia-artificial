# -*- coding: utf-8 -*-
"""deteccao_mascaras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HmPDMg1bMEgmRrpGqoeYVlDNWIQcKyEW
"""

import cv2 as cv #imports p/ processamento de img
import matplotlib.pyplot as plt 
import numpy as np

"""Importação pelo colab"""

from google.colab import files #importação pelo colab 
importados = files.upload()
print ("arquivos importados:")
print(*importados, sep="\n")

imagem = cv.imread("eu.jpeg") #lendo a imagem

def mostrar_imagem(imagem): #mostrar imagem com matplot
  imagem_rgb = cv.cvtColor(imagem, cv.COLOR_BGR2RGB) #padrão de cor do OpenCV é BGR, então convertemos
  plt.imshow(imagem_rgb)

mostrar_imagem(imagem)

"""Pré-processamento de imagens para 

---

diminuir os ruídos e reconhecer faces
"""

imagem_cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

mostrar_imagem(imagem_cinza)

"""Método cascade classifier - algoritmo viola jones para detectar faces"""

features_haar = "haarcascade_frontalface_alt2.xml" #Open CV -> coleção de arquivos xml -> detectar faces frontais

caminho = f"{cv.haarcascades}/{features_haar}" #caminho até a localização exata dos aqv features de haar

classificador = cv.CascadeClassifier(caminho) #modelo de classificação passando as features de haar como parâmetros

faces = classificador.detectMultiScale(imagem_cinza) #predição -> retorna um array de coordenadas com a locali dos rostos encontrados

imagem_copia = np.array(imagem) #cópia do array

for x,y,w,h in faces: 
  cv.rectangle(imagem_copia, (x,y), (x+w, y+h), (0,255,0), 2)

mostrar_imagem(imagem_copia)

"""Padronização"""

imagens_cortadas = list()

for x,y,w,h in faces: #percorrer array de faces encontradas
  face = imagem[y:y+h, x:x+w] #slice do ponto y até h e do x até w
  face = cv.resize(face, (160,160))
  imagens_cortadas.append(face)

len(imagens_cortadas)

for img in imagens_cortadas: 
  print(img.shape)

mostrar_imagem(imagens_cortadas[1])

"""Salvando as img em um diretório """

import os

def salvar_imagens(imagens, caminho):
  if not os.path.exists(caminho):
    os.mkdir(caminho)

  index = len(os.listdir(caminho)) #tamanho da lista de todos os arquivos no caminho

  for imagem in imagens:
    index +=1
    cv.imwrite(f"{caminho}/{index}.jpg", imagem) #escreve um caminho com a nossa imagem

salvar_imagens(imagens_cortadas, "/content/drive/MyDrive/IFC/IA/maskoff-teste")

"""treinamento do modelo (biblioteca sklearn e algoritmo knn)"""

import cv2 as cv
import numpy as np
import pandas as pd
import os 
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

import re

def carrega_dataframe(): 
  dados = { #criacao do dicionário dados
      "ARQUIVO": [],
      "ROTULO": [],
      "ALVO": [],
  }

  caminho_com_mascara = "/content/drive/MyDrive/IFC/IA/maskon" #ja recortado e padronizado
  caminho_sem_mascara = "/content/drive/MyDrive/IFC/IA/maskoff"

  com_mascara = os.listdir(caminho_com_mascara) #lista dos arquivos de cada diretório
  sem_mascara = os.listdir(caminho_sem_mascara)

  for arquivo in com_mascara: #percorrer todos os arquivo e salvar no dicionário
    aux1 = re.sub('[\s+]', '', f"{caminho_com_mascara}/{arquivo}")
    dados["ARQUIVO"].append(aux1) #salvando o caminho do arquivo
    dados["ROTULO"].append(f"Com mascara")
    dados["ALVO"].append(1)

  for arquivo in sem_mascara:
    aux2 = re.sub('[\s+]', '', f"{caminho_sem_mascara}/{arquivo}")
    dados["ARQUIVO"].append(aux2)
    dados["ROTULO"].append(f"Sem mascara")
    dados["ALVO"].append(0)

  dataframe = pd.DataFrame(dados) #criação de um dataframe do pandas passando os dados

  return dataframe

dados = carrega_dataframe()

dados.to_csv("/content/drive/MyDrive/IFC/IA/testandooo.csv") #salvar como csv

dados = pd.read_csv("/content/drive/MyDrive/IFC/IA/testandooo.csv")

dados.head()

def ler_imagens(dados):
  arquivos = dados["ARQUIVO"] #primeira coluna
  imagens = list()

  for arquivo in arquivos:
    image = cv.imread(arquivo)
    imagem_aa = cv.cvtColor(image, cv.COLOR_BGR2GRAY).flatten() #vetor
    imagens.append(imagem_aa)

  dados["IMAGEM"] = imagens #nova coluna com vetor das imagens lidas

ler_imagens(dados)

dados.head()

X = list(dados["IMAGEM"]) #característica
y = list(dados["ALVO"]) #classe para id.

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.99, random_state=13)

pca = PCA(n_components=30) #refinamento das características -> extrai as características mais notáveis
pca.fit(X_train)

X_train = pca.transform(X_train) #transforma as entradas em vetores de tamanho 30 filtrados a partir do modelo pca
X_test = pca.transform(X_test)

"""treinamento knn e estratégia grid search

"""

parametros = { #lista de opções
    "n_neighbors": [2,3,5,11,19,23,29], #ímpares para não haver empate de "votação"
    "weights": ["uniform", "distance"],
    "metric": ["eucliddean", "manhattam", "cosine", "l1", "l2"] #distâncias
}

knn = GridSearchCV(KNeighborsClassifier(), parametros) #instância de grid e modelo vazio knn e o parametro p/ escolher os melhores

knn.fit(X_train, y_train) #treinamento do knn

"""métricas de desempenho"""

knn.score(X=X_test, y=y_test) #precisão média nos dados de teste e rótulos fornecidos.

predicao = knn.predict(X_test)

verdadeiros_positivos, falsos_positivos, falsos_negativos, verdadeiros_negativos = confusion_matrix(y_test, predicao).ravel()

verdadeiros_positivos, verdadeiros_negativos

falsos_positivos, falsos_negativos

#matriz de confusão
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay 
cmx = confusion_matrix(y_test, predicao)
cmd = ConfusionMatrixDisplay(cmx, display_labels=['sem máscara','com máscara'])
cmd.plot(values_format='d')

acc = (verdadeiros_positivos + verdadeiros_negativos) / (verdadeiros_positivos + verdadeiros_negativos + falsos_positivos + falsos_negativos)

print(acc)

"""Testagem"""

from google.colab import files #importação pelo colab 
importados = files.upload()
print ("arquivos importados:")
print(*importados, sep="\n")

classificador = cv.CascadeClassifier(f"{cv.haarcascades}/haarcascade_frontalface_alt2.xml") #reconhecimento das faces

def processar_imagem(pca, classificador, imagem):
  img = cv.imread(imagem)
  imagem_cinza = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  faces = classificador.detectMultiScale(img) #id. faces
  vetores = list() #guardar images vetorizadas
  cont = 0
  fig = plt.figure(figsize=(10,10))
  for x,y,w,h in faces:
    face_cortada = imagem_cinza[y:y+h, x:x+w]
    fig.add_subplot(3, 3, cont+1) #mostrar as imagens no subplot
    plt.imshow(cv.cvtColor(face_cortada, cv.COLOR_BGR2RGB))
    cont+=1 #possivel adicionar um novo subplot na prox. iteração
    face_cortada = cv.resize(face_cortada, (160,160))
    vetor = face_cortada.flatten() #vetorizar a img e add.
    vetores.append(vetor)

  plt.show()
  return vetores

classes = { #dicionário com predições
    0: "Sem máscara",
    1: "Com máscara"
}

vetores = processar_imagem(pca, classificador, "p1.jpg")
c = knn.predict(pca.transform(vetores))

print(*[classes[e] for e in c], sep=" . ")

vetores = processar_imagem(pca, classificador, "p2.png")
c = knn.predict(pca.transform(vetores))

print(*[classes[e] for e in c], sep=" . ")

vetores = processar_imagem(pca, classificador, "p5.jpg")
c = knn.predict(pca.transform(vetores))

print(*[classes[e] for e in c], sep=" . ")

vetores = processar_imagem(pca, classificador, "p7.jpg")
c = knn.predict(pca.transform(vetores))

print(*[classes[e] for e in c], sep=" . ")

vetores = processar_imagem(pca, classificador, "p11.jpg")
c = knn.predict(pca.transform(vetores))

print(*[classes[e] for e in c], sep=" . ")

vetores = processar_imagem(pca, classificador, "p12.jpg")
c = knn.predict(pca.transform(vetores))

print(*[classes[e] for e in c], sep=" . ")