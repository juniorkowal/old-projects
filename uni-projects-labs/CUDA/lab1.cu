#include <bits/stdc++.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <iostream>
#include <math.h>

using namespace std;

__global__ void sprawdzanie_gpu(char * d, unsigned long long int pierwiastek, unsigned long long int liczba) {
  unsigned long long int i = blockDim.x * blockIdx.x + threadIdx.x;

  if (i <= pierwiastek && liczba % (i * 2 + 3) == 0) {
    * d = 1;
  }
  __syncthreads();
}

bool pierwsza(long long int p) {
  bool nie_pierwsza = 0;
  if (p < 3) {
    nie_pierwsza = 0;
    return nie_pierwsza;
  }
  if (p % 2 == 0) {
    nie_pierwsza = 1;
    return nie_pierwsza;
  } else {
    for (int i = 3; i <= int(ceil(sqrt(p))); i += 2) {
      if (p % i == 0) {
        nie_pierwsza = 1;
        break;
      }

    }
    return nie_pierwsza;
  }
}

int main(void) {
  unsigned long long int liczba;
  bool czy_pierwsza;
  unsigned long long int pierwiastek;

  int watki;
  long long int bloki;

  clock_t start, end;

  cudaEvent_t startGPU, stopGPU;
  cudaEventCreate( & startGPU);
  cudaEventCreate( & stopGPU);

  cout << "Podaj liczbe:" << endl;
  cin >> liczba;

  pierwiastek = int(ceil(sqrt(liczba)));

  size_t size = sizeof(char);
  char * wyjscie = (char * ) malloc(size);

  * wyjscie = 0;

  char * dev_a;
  cudaMalloc( & dev_a, size);

  cudaMemcpy(dev_a, wyjscie, size, cudaMemcpyHostToDevice);

  if (pierwiastek <= 1024) {
    bloki = 1;
    watki = pierwiastek;
  } else {
    watki = 1024;
    bloki = int(ceil(pierwiastek / watki));
  }

  cudaEventRecord(startGPU);
  sprawdzanie_gpu << < bloki, watki >>> (dev_a, pierwiastek, liczba);
  cudaEventRecord(stopGPU);

  cudaMemcpy(wyjscie, dev_a, size, cudaMemcpyDeviceToHost);

  if (liczba <= 3) {
    * wyjscie = 0;
  }
  if (liczba % 2 == 0 && liczba != 2) {
    * wyjscie = 1;
  }

  cudaEventSynchronize(stopGPU);
  float milliseconds = 0;
  cudaEventElapsedTime( & milliseconds, startGPU, stopGPU);
  double czas_GPU = milliseconds / 1000;

  if ( * wyjscie == 1) {
    cout << "GPU: " << liczba << " to liczba zlozona" << endl;
  } else {
    cout << "GPU" << liczba << " to liczba pierwsza" << endl;
  }

  cout << "Czas na GPU: " << czas_GPU << " s " << endl;

  cudaFree(dev_a);

  start = clock();
  czy_pierwsza = pierwsza(liczba);
  end = clock();
  if (czy_pierwsza == 0) {
    cout << "CPU: liczba pierwsza" << endl;
    cout << czy_pierwsza << endl;
  } else {
    cout << "CPU: liczba zlozona" << endl;
    cout << czy_pierwsza << endl;
  }

  float czas_CPU = float(end - start) / float(CLOCKS_PER_SEC);
  cout << "Czas na CPU: " << czas_CPU;
  cout << " s " << endl;

  float przyspieszenie = czas_CPU / czas_GPU;

  cout << "GPU jest " << przyspieszenie << " szybsze niż CPU." << endl;

  return 0;
}