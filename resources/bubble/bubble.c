#include <stdio.h>
#include <stdlib.h>

void swap(int *a, int* b)
{
    int tmp;
    tmp = *a;
    *a = *b;
    *b = tmp;
}

void bubble_sort(int* mas, int count)
{
    for (int i = 0; i < count; ++i)
    {
        for (int k = 0; k < count - 1; ++k)
        {
            if (mas[k] > mas[k + 1])
            {
                swap(mas + k, mas + k + 1);
            }
        }
    }
}

void print_mas(int* mas, int count)
{
    for (int i = 0; i < count; ++i)
    {
        printf("%i ", mas[i]);
    }
    printf("\n");
}

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
