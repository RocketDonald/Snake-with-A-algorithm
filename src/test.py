import pygame

run = True
done = False

clock = pygame.time.Clock()

time_1 = []
time_2 = []

for i in range(100):
    j = 0
    time_first = 0
    time_second = 0

    while run:
        j += 1
        time_first += clock.get_rawtime() / 1000
        clock.tick()

        if j == 100:
            run = False
            time_1.append(time_first)

    j = 0

    while not done:
        j += 1
        time_second += clock.get_rawtime() / 1000
        clock.tick()

        if j == 100:
            done = True
            time_2.append(time_second)

average_1 = 0
average_2 = 0

for time in time_1:
    average_1 += time

average_1 = average_1 // 100

for time in time_2:
    average_2 += time

average_2 = average_2 // 100

print("Average 1: " + str(average_1) + " | Average 2: " + str(average_2))