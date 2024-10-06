import matplotlib.pyplot as plt




def lista_reakcji_pliki(plik):
    test = open(plik, "r")

    lista_reakcji=[]
    for czas in test:
        czas=czas.strip()
        lista_reakcji.append(int(czas))

    test.close()
    return lista_reakcji

lista_reakcji1=lista_reakcji_pliki('optic1.txt')
lista_reakcji2=lista_reakcji_pliki('optic2.txt')
lista_reakcji3=lista_reakcji_pliki('acoustic1.txt')
lista_reakcji4=lista_reakcji_pliki('acoustic2.txt')

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(lista_reakcji1)
axs[0, 0].set_title('Optyczny 1, czas reakcji: \n'+str(round(sum(lista_reakcji1)/len(lista_reakcji1),2))+' ms')
axs[0, 1].plot(lista_reakcji2, 'tab:orange')
axs[0, 1].set_title('Optyczny 2, czas reakcji: \n'+str(round(sum(lista_reakcji2)/len(lista_reakcji2),2))+' ms')
axs[1, 0].plot(lista_reakcji3, 'tab:green')
axs[1, 0].set_title('Akustyczny 1, czas reakcji: \n'+str(round(sum(lista_reakcji3)/len(lista_reakcji3),2))+' ms')
axs[1, 1].plot(lista_reakcji4, 'tab:red')
axs[1, 1].set_title('Akustyczny 2, czas reakcji: \n'+str(round(sum(lista_reakcji4)/len(lista_reakcji4),2))+' ms')

axs[0, 0].set_xticks(range(0,len(lista_reakcji1)+1, 1))
axs[0, 1].set_xticks(range(0,len(lista_reakcji2)+1, 1))
axs[1, 0].set_xticks(range(0,len(lista_reakcji3)+1, 1))
axs[1, 1].set_xticks(range(0,len(lista_reakcji4)+1, 1))
for ax in axs.flat:
    ax.set(xlabel='podejście', ylabel='wynik (ms)')
fig.tight_layout()
plt.show()