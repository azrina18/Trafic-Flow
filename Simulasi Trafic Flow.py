import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import numpy.random as random
import operator as op


def modelMobil(mobil):
    M = 100
    p = float(0.3)
    v = 0
    N = 20
    t_max = 1000
    v_max = 5
    D = 1
    movement = []
    antrian = [i for i in range(N)]
    waktu = 0
    density = {}
    car_max = [0 for i in range(t_max)]
    avg0 = 0

    # Program untuk iterasi pemodelan
    for x in range(t_max):
        x_row = []
        iterasi_car = 0

        for i in antrian:
            s_car = mobil[i]
            next_car = mobil[i + 1 if i + 1 < N else 0]
            v = np.min([v + 1, v_max])  # Update Kecepatan

            # mendapatkan jarak antar mobil
            if i == 0:
                d = D
            elif next_car[0] < s_car[0]:
                d = M - next_car[0]
            else:
                d = next_car[0] - s_car[0]

            # Peluang Kecenderungan pengemudi mengerem
            pr = random.rand()
            if pr < p:
                v = np.max([np.min([v + 1, v_max, d - 1]) - 1, 0])
            else:
                v = np.min([v + 1, v_max, d - 1])

            # Update Posisi mobil
            x = s_car[0]  # Mengambil nilai x dari mobil ke - i
            x = x + v

            # Pengecekan jika nilai x lebih dari M, maka kembali ke awal
            if x >= M:
                temp = []
                for i in range(N):
                    order = antrian[i] + N - 1
                    if order + N - 1 > N:
                        order = order - N
                    temp.append(order)
                antrian = temp
                x = x - M
                mobil[i][2] += 1
            x_row.append([x, s_car[1], mobil[i][2]])

            # Update Posisi mobil
            if x >= 80 and x <= 90:
                iterasi_car += 1

        # Menghitung kepadatan lalulintas
        density[waktu] = (iterasi_car / 10) * 100
        waktu += 1

        # Menyimpan dan menampung posisi terbaru dari mobil
        mobil = x_row
        movement.append(x_row)

    # Iterasi untuk Mencari nilai kepadatan pada tiap interval waktu, dengan ketentuan 5 unit posisi
    for i in range(len(movement)):
        for j in range(len(movement[0])):
            if j < N - 1:
                select = movement[i][j][0]
                next = movement[i][j + 1][0]
                if next - select <= 5 and next - select >= 0:
                    car_max[i] += 1

    # Menghitung nilai Rata-Rata mobil kembali ke posisi awal
    sum = 0
    for i in range(len(mobil)):
        sum += mobil[i][2]
    avg0 = sum / N / t_max * 100

    return movement, density, avg0, car_max


# Fungsi render membuat animasi
def animate(i):
    cars_p = perpindahan_car[i]
    car_marker.set_offsets(cars_p)
    return car_marker


# main
if __name__ == "__main__":
    # inisialisasi variabel pemodelan
    M = 100
    p = float(0.3)
    v = 0
    N = 20
    t_max = 1000
    v_max = 5
    d = 1

    # Set Visualisasi Jalan
    road_fig = np.array([[[0, M + 0.5], [3, 3]], [[0, M + 0.5], [7, 7]]])
    # Random Posisi Mobil
    mobil = np.array([[random.randint(1, M), 5, 0] for i in range(1, N + 1)])
    # Sorting Posisi mobil
    mobil = np.array(sorted(mobil, key=op.itemgetter(0)))
    perpindahan_car, density, average, car_max = modelMobil(mobil)

    # menampilkan figure titik semua mobil (SOAL NO 1)
    a = np.zeros(shape=(t_max, M))
    for i in range(t_max):
        index = 0
        for j in range(M):
            temp = np.array(sorted(perpindahan_car[i], key=op.itemgetter(0)))
            if j == temp[index][0] and index < N - 1:
                index += 1
                a[i, j] = 0
            else:
                a[i, j] = -1

    plt.figure(1, figsize=(15, 25))
    plt.xlabel("Posisi")
    plt.ylabel("Waktu")
    plt.imshow(a, cmap="Oranges", interpolation="nearest")

    # Menampilkan Figure kepadatan di posisi 80-90 (SOAL NO 2)
    print("Kepadatan Kendaraan di posisi X80 ~ X90:")
    for x in density:
        print(
            f"Kepadatan Kendaraan di waktu ke-{x+1} adalah sebesar {density[x]}"
        )

    plt.figure(2, figsize=(14, 6))
    plt.bar(range(len(density)), list(density.values()), width=0.6)
    plt.title("Kepadatan Kendaraan di posisi X80 - X90")
    plt.xlabel("Satuan Waktu")
    plt.ylabel("Banyak Kendaraan")

    # Menampilkan kepadatan Maksimum tiap interval dengan ketentuan 5 unit posisi (SOAL NO 3)
    print("kepadatan Maksimum ketentuan 5 Unit Posisi")
    for x in car_max:
        print(
            f"Kepadatan Kendaraan Maks di waktu ke-{x+1} adalah sebesar {car_max[x]}"
        )

    plt.figure(3, figsize=(14, 6))
    plt.bar(range(len(car_max)), car_max, width=0.6)
    plt.title("kepadatan Maksimum ketentuan 5 Unit Posisi")
    plt.xlabel("Satuan Waktu")
    plt.ylabel("Banyak Kendaraan")

    # Menampilkan Nilai Rata rata Mobil kembali ke posisi awal (SOAL NO 4)
    print("Waktu Rata Rata Kendaraan:")
    print(
        "Waktu rata-rata mobil kembali ke posisi awal:",
        format(average, ".3f"),
    )

    # Menampilkan Simulasi
    fig = plt.figure(4)
    plot_axes = plt.axes(ylim=(0, 10), xlim=(0, M + 0.5))
    plt.plot([90, 90], [3, 7], color="red")
    plt.plot([80, 80], [3, 7], color="red")
    plt.title("Simulasi Traffic Flow")
    for road in road_fig:
        plt.plot(road[0], road[1], color="black")
    car_marker = plot_axes.scatter([], [], s=75, marker="s")

    anim = animation.FuncAnimation(
        fig, animate, frames=len(perpindahan_car), interval=300, repeat=False
    )
    plt.show()
