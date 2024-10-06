#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <bits/stdc++.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

using namespace std;

void dodawanie_macierzy_cpu(double ** M, double ** N, double ** W, int size) {
  int i, j;

  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      W[i][j] = M[i][j] + N[i][j];
    }
  }
}

void mnozenie_macierzy_cpu(double ** M, double ** N, double ** W, int size) {
  int i, j, k, a, b = 1;

  for (i = 0; i < size; i++) {
    a = 1;
    b--;
    for (j = 0; j < size; j++) {
      a--;
      for (k = 0; k < size; k++) {
        W[i][j] += M[i][j + a + k] * N[i + b + k][j];
      }
    }
  }
}

void mnozenie_liczba_cpu(double ** M, int liczba, double ** W, int size) {
  int i, j;

  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      W[i][j] = M[i][j] * liczba;
    }
  }
}

void transpose_cpu(double ** M, double ** W, int size) {
  int i, j;

  for (i = 0; i < size; i++) {
    for (j = 0; j < size; j++) {
      W[i][j] = M[j][i];
    }
  }
}

__global__ void mnozenie_gpu(double * M, double * N, double * W, int size) {
  int wiersz = blockIdx.y * blockDim.y + threadIdx.y;
  int kolumna = blockIdx.x * blockDim.x + threadIdx.x;
  double tmpSum = 0;

  for (int i = 0; i < size; i++) {
    tmpSum += M[wiersz * size + i] * N[i * size + kolumna];
  }
  W[wiersz * size + kolumna] = tmpSum;
  __syncthreads();
}

__global__ void dodawanie_gpu(double * M, double * N, double * W, int size) {
  int wiersz = blockIdx.y * blockDim.y + threadIdx.y;
  int kolumna = blockIdx.x * blockDim.x + threadIdx.x;

  W[wiersz * size + kolumna] = M[wiersz * size + kolumna] + N[wiersz * size + kolumna];
  __syncthreads();
}

__global__ void transpose_gpu(double * M, double * W, int size) {
  int wiersz = blockIdx.y * blockDim.y + threadIdx.y;
  int kolumna = blockIdx.x * blockDim.x + threadIdx.x;

  W[wiersz * size + kolumna] = M[kolumna * size + wiersz];
  __syncthreads();
}

__global__ void mnozenie_przez_liczbe_gpu_kernel(double * M, int liczba, double * W, int size) {
  int wiersz = blockIdx.y * blockDim.y + threadIdx.y;
  int kolumna = blockIdx.x * blockDim.x + threadIdx.x;

  W[wiersz * size + kolumna] = M[wiersz * size + kolumna] * liczba;
  __syncthreads();
}

void macierz_gpu(double * A, double * B, double * wynik, double * X, int u, int w, int size) {
  dim3 threadsPerBlock(size, size);
  dim3 blocksPerGrid(1, 1);
  if (size * size > 512) {
    threadsPerBlock.x = 512;
    threadsPerBlock.y = 512;
    blocksPerGrid.x = ceil(double(size) / double(threadsPerBlock.x));
    blocksPerGrid.y = ceil(double(size) / double(threadsPerBlock.y));
  }
  mnozenie_gpu << < blocksPerGrid, threadsPerBlock >>> (A, B, wynik, size);
  dodawanie_gpu << < blocksPerGrid, threadsPerBlock >>> (A, wynik, X, size);
  transpose_gpu << < blocksPerGrid, threadsPerBlock >>> (A, wynik, size);
  mnozenie_przez_liczbe_gpu_kernel << < blocksPerGrid, threadsPerBlock >>> (wynik, u, wynik, size);
  dodawanie_gpu << < blocksPerGrid, threadsPerBlock >>> (X, wynik, X, size);
  w = -w;
  mnozenie_przez_liczbe_gpu_kernel << < blocksPerGrid, threadsPerBlock >>> (B, w, wynik, size);
  dodawanie_gpu << < blocksPerGrid, threadsPerBlock >>> (X, wynik, X, size);
}

double blad_wynikow(double ** X_cpu, double * X_gpu, int size) {
  double tmpMaxCPU = 0;
  double tmpMaxDIFF = 0;
  double error = 0;

  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      if ((X_cpu[i][j] - X_gpu[i * size + j]) > tmpMaxDIFF) {
        tmpMaxDIFF = X_cpu[i][j] - X_gpu[i * size + j];
      }
      if (X_cpu[i][j] > tmpMaxCPU) {
        tmpMaxCPU = X_cpu[i][j];
      }
    }
  }

  error = tmpMaxDIFF / tmpMaxCPU;
  return error;
}

int main() {
  srand(time(NULL));

  int czy_wyswietlac, size, u = 5, w = 0;

  printf("Podaj size macierzy:");
  scanf("%d", & size);
  printf("0 - nie wyswietlaj wynikow; 1 - wyswietlaj wyniki:");
  scanf("%d", & czy_wyswietlac);

  double ** wynik = new double * [size];
  double ** X = new double * [size];
  double ** A = new double * [size];
  double ** B = new double * [size];

  for (int i = 0; i < size; ++i) {
    wynik[i] = new double[size];
  }

  for (int i = 0; i < size; ++i) {
    X[i] = new double[size];
  }

  for (int i = 0; i < size; ++i) {
    A[i] = new double[size];
  }

  for (int i = 0; i < size; ++i) {
    B[i] = new double[size];
  }

  printf("Macierz A:\n");
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      A[i][j] = rand() % 100;
      if (czy_wyswietlac == 1) {
        printf("%f\t", A[i][j]);
      }
    }
    if (czy_wyswietlac == 1) {
      printf("\n");
    }
  }
  if (czy_wyswietlac == 1) {
    printf("\n");
  }

  printf("Macierz B:\n");
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      B[i][j] = rand() % 100;
      if (czy_wyswietlac == 1) {
        printf("%f\t", B[i][j]);
      }
    }
    if (czy_wyswietlac == 1) {
      printf("\n");
    }
  }
  if (czy_wyswietlac == 1) {
    printf("\n");
  }

  clock_t cpu_start, cpu_end;
  cudaEvent_t gpu_start, gpu_end;
  cudaEventCreate( & gpu_start);
  cudaEventCreate( & gpu_end);

  cpu_start = clock();
  mnozenie_macierzy_cpu(A, B, X, size);
  dodawanie_macierzy_cpu(X, A, X, size);
  transpose_cpu(A, wynik, size);
  mnozenie_liczba_cpu(wynik, u, wynik, size);
  dodawanie_macierzy_cpu(wynik, X, X, size);
  w = -w;
  mnozenie_liczba_cpu(B, w, wynik, size);
  dodawanie_macierzy_cpu(wynik, X, X, size);
  cpu_end = clock();

  printf("Macierz X_cpu:\n");
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      if (czy_wyswietlac == 1) {
        printf("%f\t", X[i][j]);
      }
    }
    if (czy_wyswietlac == 1) {
      printf("\n");
    }
  }
  if (czy_wyswietlac == 1) {
    printf("\n");
  }

  static
  const int n_el = size * size;
  static
  const size_t size = n_el * sizeof(double);

  double * h_A = (double * ) malloc(size);
  double * h_B = (double * ) malloc(size);
  double * h_C = (double * ) malloc(size);
  double * h_D = (double * ) malloc(size);

  double * d_A, * d_B, * d_C, * d_D;

  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      h_A[i * size + j] = A[i][j];
      h_B[i * size + j] = B[i][j];
    }
  }

  cudaMalloc( & d_A, size);
  cudaMalloc( & d_B, size);
  cudaMalloc( & d_C, size);
  cudaMalloc( & d_D, size);
  cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
  cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

  cudaEventRecord(gpu_start);
  macierz_gpu(d_A, d_B, d_C, d_D, u, w, size);
  cudaEventRecord(gpu_end);

  cudaMemcpy(h_D, d_D, size, cudaMemcpyDeviceToHost);

  printf("Macierz X_gpu:\n");
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      if (czy_wyswietlac == 1) {
        printf("%f\t", h_D[i * size + j]);
      }
    }
    if (czy_wyswietlac == 1) {
      printf("\n");
    }
  }
  if (czy_wyswietlac == 1) {
    printf("\n");
  }

  double blad = 0;
  blad = blad_wynikow(X, h_D, size);
  printf("Bląd wyniku miedzy CPU a GPU wynosi: %f\t", blad);
  printf("\n");

  cudaFree(d_A);
  cudaFree(d_B);
  cudaFree(d_C);
  cudaFree(d_D);

  delete[] h_A;
  delete[] h_B;
  delete[] h_C;
  delete[] h_D;

  cudaEventSynchronize(gpu_end);
  float czas = 0;
  cudaEventElapsedTime( & czas, gpu_start, gpu_end);
  double czas_gpu = czas / 1000;
  cout << "Czas na GPU: " << czas_gpu << " sekund" << endl;
  float czas_cpu = float(cpu_end - cpu_start) / float(CLOCKS_PER_SEC);
  cout << "Czas CPU : " << czas_cpu << " sekund " << endl;
  float ile_razy_szybsze = czas_cpu / czas_gpu;
  cout << "GPU było " << ile_razy_szybsze << " razy szybsze niż CPU" << endl;
  return 0;
}