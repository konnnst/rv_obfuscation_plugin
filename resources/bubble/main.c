#include <stdio.h>
#include <stdlib.h>
#include "bubble.h"

void main()
{
    int count;
    printf("Count: ");
    scanf("%i"  , &count);
    int *mas;
    mas = malloc(sizeof(int) * count);
    for (int i = 0; i < count; ++i)
    {
        mas[i] = rand() % 50;
    }

    print_mas(mas, count);
    bubble_sort(mas, count);
    print_mas(mas, count);

    getchar();
    getchar();
}